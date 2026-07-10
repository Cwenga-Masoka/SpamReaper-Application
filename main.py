import threading
import platform
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from review_screen import ReviewScreen
from settings_screen import SettingsScreen
from history_screen import HistoryScreen
from tracker_db import initialize_db
from scheduler import start_scheduler
from gmail_auth import load_token

class HomeScreen(Screen):
    """
    A simple status screen shown while we check/complete login.
    Once login succeeds, we switch away from this to the ReviewScreen.
    """
    def set_status(self, text):
        self.ids.status_label.text = text

def check_internet() -> bool:
    """Quick check for internet connectivity."""
    import socket
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            ("8.8.8.8", 53)
        )
        return True
    except Exception:
        return False

class SpamReaperApp(MDApp):
    """
    Main Kivy application class.
    """
    kv_file = ''  # Disable MDApp's auto kv loading — we load manually in build()

    def build(self):
        self.title = "SpamReaper"

        # 1. Register Fonts
        LabelBase.register(name="HankenGrotesk", fn_regular="fonts/HankenGrotesk-Regular.ttf")
        LabelBase.register(name="JetBrainsMono", fn_regular="fonts/JetBrainsMono-Medium.ttf")

        # 2. Inject Custom Hex Colors into KivyMD's Palette Map
        # Overwrites the default "800" shade of BlueGray with your custom dark slate color
        colors["BlueGray"]["800"] = "2e434c"  # Note: hex string without the '#' symbol

        # 3. Configure KivyMD Theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray" 
        self.theme_cls.primary_hue = "800"   # Safely triggers your #2e434c primary color

        # 4. Load the UI layout file safely
        Builder.unload_file("spamreaper.kv")
        return Builder.load_file("spamreaper.kv")

    def navigate_to(self, screen_name):
        if self.root.has_screen(screen_name):
            self.root.current = screen_name

    def start_app_logic(self, dt):
        if not check_internet():
            self.root.current = 'no_internet'
            return

        if load_token() is not None:
            print("Existing login found.")
            self._start_scheduler_and_show_review()
        else:
            self.root.current = 'connect'

    def start_gmail_connect(self):
        self.root.ids.connect_btn.text = "Requesting code..."
        self.root.ids.connect_btn.disabled = True
        self.root.ids.connect_status_label.text = "Contacting Google..."
        threading.Thread(target=self._run_device_login_flow, daemon=True).start()

    def _run_device_login_flow(self):
        try:
            from gmail_auth import (
                start_device_login_flow,
                complete_device_login_flow,
                open_url_natively,
            )

            device_data = start_device_login_flow()
            user_code = device_data['user_code']
            verification_url = device_data.get('verification_url') or device_data.get('verification_uri')

            Clock.schedule_once(lambda dt: self._show_device_code(user_code, verification_url))

            complete_device_login_flow(device_data)
            Clock.schedule_once(lambda dt: self._start_scheduler_and_show_review())

        except Exception as e:
            error_msg = str(e)
            print(f"Login failed: {error_msg}")
            Clock.schedule_once(lambda dt: self._reset_connect_screen(error_msg))

    def _show_device_code(self, user_code, verification_url):
        self.root.ids.connect_status_label.text = (
            f"Go to {verification_url} and enter this code:\n\n{user_code}"
        )
        self.root.ids.connect_btn.text = "Waiting for approval..."

        # Open the browser automatically as a convenience — the user still
        # has to type the code, but at least they don't have to type the URL
        from gmail_auth import open_url_natively
        if verification_url:
            open_url_natively(verification_url)

    def _reset_connect_screen(self, error_msg=""):
        self.root.ids.connect_btn.text = "Connect with Google"
        self.root.ids.connect_btn.disabled = False
        self.root.ids.connect_status_label.text = error_msg

    def _request_notification_permission(self):
        """
        Android 13+ requires POST_NOTIFICATIONS to be granted at runtime,
        not just declared in the manifest — without this, notifier.py's
        calls will silently do nothing on newer devices.
        """
        if platform.system() != 'Linux':
            return
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.POST_NOTIFICATIONS])
            print("Requested POST_NOTIFICATIONS permission.")
        except Exception as e:
            print(f"Could not request notification permission: {e}")

    def _start_scheduler_and_show_review(self):
        try:
            start_scheduler()
            print("Scheduler started.")
        except Exception as e:
            print(f"Could not start scheduler: {e}")

        self.root.current = 'main_app'
        Clock.schedule_once(self._show_inbox_loading, 0.3)

    def _force_inbox_refresh(self):
        for widget in self.root.walk():
            from review_screen import ReviewScreen
            if isinstance(widget, ReviewScreen):
                if widget._scan_running:
                    Clock.schedule_once(
                        lambda dt: self._force_inbox_refresh(), 2
                    )
                elif not widget._scan_error:
                    widget.refresh_list()
                break

    def _show_inbox_loading(self, dt):
        """Shows the scanning animation on first entry."""
        for widget in self.root.walk():
            from review_screen import ReviewScreen
            if isinstance(widget, ReviewScreen):
                widget._show_loading_state()
                widget._scan_running = True
                break

    def sync_data(self):
        """Routes the top bar sync action safely by walking the widget tree."""
        # Using walk() guarantees we find the widget even if it's buried in a bottom nav
        for widget in self.root.walk():
            if isinstance(widget, ReviewScreen):
                widget.handle_scan_now()
                break

    def on_start(self):
        print("SpamReaper started successfully.")
        initialize_db()
        self._request_notification_permission()
        Clock.schedule_once(self.start_app_logic, 0.5)

    def retry_connection(self):
        """Called when user taps Retry on the no internet screen."""
        if check_internet():
            self.root.current = 'home'
            Clock.schedule_once(self.start_app_logic, 0.3)
        else:
            from kivymd.toast import toast
            toast("Still no internet connection — please check your network")

    def on_stop(self):
        print("SpamReaper closed.")


if __name__ == "__main__":
    SpamReaperApp().run()
