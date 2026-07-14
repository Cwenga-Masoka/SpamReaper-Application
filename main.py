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
from gmail_auth import start_login_flow, finish_login_flow, load_token

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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(("8.8.8.8", 53))
        sock.close()
        return True
    except Exception:
        return False
class SpamReaperApp(MDApp):
    """
    Main Kivy application class.
    """
    kv_file = ''  # Disable MDApp's auto kv loading — we load manually in build()
    pending_auth_code = None  # Holds the auth code received via Android intent
    awaiting_login = False  # True if we're waiting for the user to complete login 

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
        self.root.ids.connect_btn.text = "Authorizing..."
        self.root.ids.connect_btn.disabled = True
        self.root.ids.connect_status_label.text = "Opening browser for Gmail login..."
        self.awaiting_login = True
        threading.Thread(target=self._run_stage_one_login, daemon=True).start()

    def _run_stage_one_login(self):
        try:
            auth_code = start_login_flow()

            if auth_code == "ANDROID_PENDING":
                print("[OAuth] Android: browser opened, waiting for redirect intent...")
                return

            # Desktop path — we already have the code, finish immediately
            self._run_stage_two_login(auth_code)

        except Exception as e:
            error_msg = str(e)
            print(f"[OAuth] Stage 1 login failed: {error_msg}")
            self.awaiting_login = False
            Clock.schedule_once(lambda dt: self._reset_connect_screen(error_msg))

    def _run_stage_two_login(self, auth_code):
        try:
            finish_login_flow(auth_code)
            print("[OAuth] Login fully completed.")
            Clock.schedule_once(lambda dt: self._start_scheduler_and_show_review())
        except Exception as e:
            error_msg = str(e)
            print(f"[OAuth] Stage 2 login failed: {error_msg}")
            Clock.schedule_once(lambda dt: self._reset_connect_screen(error_msg))
 
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
        """Shows the scanning animation on first entry — but only if the
        initial scan genuinely hasn't finished yet. Without this check, a
        fast scan (e.g. the 'skip, already scanned recently' path) can
        complete before this delayed callback fires, and this would then
        incorrectly re-lock the sync button in a permanent scanning state
        with nothing left running to ever clear it."""
        for widget in self.root.walk():
            from review_screen import ReviewScreen
            if isinstance(widget, ReviewScreen):
                if widget._initial_scan_done:
                    # The real scan already finished — just show results,
                    # don't fake a loading state on top of it.
                    widget.refresh_list()
                else:
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

        if platform.system() == "Linux":
            self._register_intent_listener()

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

    def _register_intent_listener(self):
        """
        Uses p4a's built-in android.activity module to listen for
        new intents.
        """
        try:
            from android import activity
            activity.bind(on_new_intent=self._handle_android_intent)
            print("[OAuth] Intent listener registered via android.activity")
        except Exception as e:
            print(f"[OAuth] Failed to register intent listener: {e}")

    def _handle_android_intent(self, intent):
        """Callback fired by android.activity when a new intent arrives."""
        print("[OAuth] _handle_android_intent FIRED — on_new_intent received something")
        Clock.schedule_once(lambda dt: self._handle_new_intent(intent))

    def _handle_new_intent(self, intent):
        """Handles the OAuth redirect intent on the main thread."""
        print(f"[OAuth] _handle_new_intent called, awaiting_login={self.awaiting_login}")
        if not self.awaiting_login:
            print("[OAuth] Not awaiting login, ignoring this intent")
            return

        try:
            data = intent.getData()
            if data is None:
                print("[OAuth] Intent had no data payload")
                return

            url = data.toString()
            print(f"[OAuth] Intent URL received: {url}")

            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            params = parse_qs(parsed.query)

            if 'code' not in params:
                print(f"[OAuth] No auth code in intent URL — params were: {params}")
                return

            auth_code = params['code'][0]
            self.awaiting_login = False
            self.pending_auth_code = auth_code

            print("[OAuth] Auth code captured. Completing login...")
            self.root.ids.connect_status_label.text = "Completing login..."

            threading.Thread(
                target=self._run_stage_two_login,
                args=(auth_code,),
                daemon=True
            ).start()

        except Exception as e:
            print(f"[OAuth] _handle_new_intent error: {e}")
            self._reset_connect_screen(f"Login failed: {e}")


if __name__ == "__main__":
    SpamReaperApp().run()
