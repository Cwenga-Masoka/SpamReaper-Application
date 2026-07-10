import threading
from itertools import groupby
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivy.uix.label import Label
from kivymd.app import MDApp
import re
from config_manager import get_setting
from email_deleter import trash_email, trash_multiple_emails
from scheduler import run_daily_scan
from theme import (
    COLOR_ON_SURFACE,
    COLOR_ON_SURFACE_VARIANT,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_SURFACE_CONTAINER_LOW,
    FONT_BODY,
    FONT_MONO,
    FONT_HEADING,
    get_urgency_color,
    get_urgency_label,
)
from tracker_db import get_all_flagged_messages, mark_keep, log_action

SYNC_ICON_IDS = ("sync_icon_inbox", "sync_icon_history", "sync_icon_settings")

class CleanInboxWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.padding = [dp(20), dp(60), dp(20), dp(60)]
        self.spacing = dp(8)

        self.headline = Label(
            text="Inbox Clean",
            font_name=FONT_HEADING,
            font_size="22sp",
            bold=True,
            color=get_color_from_hex(COLOR_ON_SURFACE),
            halign="center",
            valign="center",
            size_hint_y=None,
            height=dp(32)
        )
        self.headline.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        self.subtitle = Label(
            text="No spam detected. Your inbox is secure.",
            font_name=FONT_BODY,
            font_size="15sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="center",
            valign="center",
            size_hint_y=None,
            height=dp(24)
        )
        self.subtitle.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        self.add_widget(self.headline)
        self.add_widget(self.subtitle)

class SectionHeader(MDBoxLayout):
    """
    Groups cards by urgency thresholds and handles bulk category updates.
    """
    def __init__(self, days_left, message_ids, messages, on_clear_complete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "40dp"
        self.padding = ["4dp", "8dp", "4dp", "4dp"]
        self.spacing = "12dp"

        self.message_ids = message_ids
        self.messages = messages
        self.on_clear_complete = on_clear_complete

        label_text = f"Expiring in {days_left} Days" if days_left > 1 else "Expiring Today"
        urgency_color = get_color_from_hex(get_urgency_color(days_left))

        self.title_label = Label(
            text=label_text.upper(),
            font_name=FONT_HEADING,
            bold=True,
            underline=True,
            color=urgency_color,
            size_hint_x=1,
            halign="left",
            valign="center"
        )
        self.title_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        self.clear_btn = MDFlatButton(
            text="CLEAR ALL" if days_left <= 1 else "CLEAR",
            theme_text_color="Custom",
            text_color=urgency_color,
            size_hint_x=None,
            on_release=self.bulk_trash_group
        )

        self.add_widget(self.title_label)
        self.add_widget(self.clear_btn)

    def bulk_trash_group(self, instance):
        threading.Thread(target=self._do_bulk_trash, daemon=True).start()

    def _do_bulk_trash(self):
        results = trash_multiple_emails(self.message_ids)
        for msg in self.messages:
            if msg["sms_id"] in results["succeeded"]:
                log_action(
                    sms_id=msg["sms_id"],
                    sender=msg["sender"],
                    subject=msg.get("subject", ""),
                    preview=msg.get("preview", ""),
                    action="deleted"
                )
        Clock.schedule_once(lambda dt: self._finish_bulk_trash(results))

    def _finish_bulk_trash(self, results):
        if results["failed"]:
            toast(f"{len(results['failed'])} email(s) could not be deleted")
        self.on_clear_complete()


class EmailCard(MDCard):
    """
    Individual spam detail viewport displaying context data.
    """
    def __init__(self, message_data, on_action_complete, **kwargs):
        super().__init__(**kwargs)

        urgency_color_rgba = get_color_from_hex(get_urgency_color(message_data['days_left']))

        # Border thickness matches urgency — thick red for critical, thin for others
        border_width = dp(2) if message_data['days_left'] <= 1 else dp(1)

        with self.canvas.after:
            Color(rgba=urgency_color_rgba)
            self.border_line = Line(
                rectangle=(self.x, self.y, self.width, self.height),
                width=border_width
            )

        def update_border(instance, value):
            self.border_line.rectangle = (
                instance.x, instance.y, instance.width, instance.height
            )

        self.bind(pos=update_border, size=update_border)

        self.orientation = "vertical"
        self.adaptive_height = True
        self.padding = "16dp"
        self.spacing = "12dp"

        self.sms_id = message_data["sms_id"]
        self.message_data = message_data
        self.on_action_complete = on_action_complete

        # Top Metadata Row
        top_row = MDBoxLayout(
            orientation="horizontal", 
            size_hint_y=None,
            height="24dp",
        )
        sender_lbl = Label(
            text=message_data.get("sender", "Unknown Sender"),
            font_name = FONT_BODY,
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="center",
            shorten=True,
            shorten_from="right",
            size_hint_x=1,
            size_hint_y=None,
            height="24dp"
        )
        sender_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        days_lbl = Label(
            text=get_urgency_label(message_data['days_left']),
            font_name=FONT_HEADING,
            bold=True,
            halign="right",
            valign="center",
            color=get_color_from_hex(get_urgency_color(message_data['days_left'])),
            size_hint_x=None,
            width="110dp",
            size_hint_y=None,
            height="24dp"
        )
        top_row.add_widget(sender_lbl)
        top_row.add_widget(days_lbl)

        raw_preview = message_data.get("preview", "")
        # Strip excess whitespace and newlines
        clean_preview = re.sub(r'\s+', ' ', raw_preview).strip()
        # Truncate to a readable length
        if len(clean_preview) > 120:
            clean_preview = clean_preview[:120] + "..."

        subject_lbl = Label(
            text=message_data.get("subject") or "(No subject)",
            font_name=FONT_HEADING,
            bold=True,
            color=get_color_from_hex(COLOR_ON_SURFACE),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        subject_lbl.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        subject_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )
        
        preview_lbl = Label(
            text=message_data.get("preview") or "(No preview available)",
            font_name=FONT_BODY,
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        preview_lbl.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        preview_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        # Action Buttons
        actions_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="44dp",
            spacing="12dp"
        )

        keep_btn = Button(
            text="KEEP",
            font_name=FONT_HEADING,
            font_size="13sp",
            size_hint_x=0.5,
            background_normal="",
            background_color=get_color_from_hex("#e7e8e9"),
            color=get_color_from_hex(COLOR_PRIMARY),
            on_release=self.mark_as_safe
        )

        delete_btn = Button(
            text="DELETE NOW",
            font_name=FONT_HEADING,
            font_size="13sp",
            size_hint_x=0.5,
            background_normal="",
            background_color=get_color_from_hex(get_urgency_color(message_data['days_left'])),
            color=(1, 1, 1, 1),
            on_release=self.execute_immediate_trash
        )

        actions_row.add_widget(keep_btn)
        actions_row.add_widget(delete_btn)

        self.add_widget(top_row)
        self.add_widget(subject_lbl)
        self.add_widget(preview_lbl)
        self.add_widget(actions_row)

    def mark_as_safe(self, instance):
        threading.Thread(target=self._do_mark_safe, daemon=True).start()

    def _do_mark_safe(self):
        mark_keep(self.sms_id)
        log_action(
            sms_id=self.sms_id,
            sender=self.message_data["sender"],
            subject=self.message_data.get("subject", ""),
            preview=self.message_data.get("preview", ""),
            action="kept"
        )
        Clock.schedule_once(lambda dt: toast("Marked as safe — moved to History"))
        Clock.schedule_once(lambda dt: self.on_action_complete())

    def execute_immediate_trash(self, instance):
        threading.Thread(target=self._do_network_trash, daemon=True).start()

    def _do_network_trash(self):
        if trash_email(self.sms_id):
            log_action(
                sms_id=self.sms_id,
                sender=self.message_data["sender"],
                subject=self.message_data.get("subject", ""),
                preview=self.message_data.get("preview", ""),
                action="deleted"
            )
            Clock.schedule_once(lambda dt: toast("Moved to trash — restorable for 30 days"))
            Clock.schedule_once(lambda dt: self.on_action_complete())

class ReviewScreen(MDBoxLayout):
    """
    Primary operational screen managing layout mutations.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_current_ids = []
        self.all_messages = []
        self._confirm_dialog = None
        Clock.schedule_once(self.refresh_list, 0.1)
        self._loading_event = None
        self._loading_label = None
        self._scan_running = False
        self._scan_error = False
        self._initial_scan_done = False

    def refresh_list(self, *args):
        if not self._initial_scan_done:
            return
        self.ids.card_list.clear_widgets()
        self.all_current_ids = []
        self.all_messages = []

        messages = get_all_flagged_messages()

        if not messages:
            self.ids.card_list.add_widget(CleanInboxWidget())
            self.ids.wipe_today_btn.disabled = True
            return

        self.ids.wipe_today_btn.disabled = False
        days_before_deletion = get_setting("days_before_deletion") or 5

        for msg in messages:
            msg["days_left"] = max(0, days_before_deletion - msg.get("days_old", 0))
            self.all_current_ids.append(msg["sms_id"])
            self.all_messages.append(msg)

        messages.sort(key=lambda m: m["days_left"])

        for days_left, group in groupby(messages, key=lambda m: m["days_left"]):
            group_list = list(group)
            group_ids = [m["sms_id"] for m in group_list]

            header = SectionHeader(
                days_left=days_left,
                message_ids=group_ids,
                messages=group_list,
                on_clear_complete=self.refresh_list
            )
            self.ids.card_list.add_widget(header)

            for msg in group_list:
                card = EmailCard(msg, self.refresh_list)
                self.ids.card_list.add_widget(card)

    def handle_scan_now(self):
        if self._scan_running:
            return
        self._scan_running = True
        self._scan_error = False
        self._show_loading_state()
        Clock.schedule_once(self._set_sync_loading_state)
        threading.Thread(target=self._do_scan_now, daemon=True).start()

    def _show_loading_state(self):
        self.ids.card_list.clear_widgets()
        self.ids.wipe_today_btn.disabled = True

        self._loading_label = Label(
            text="Scanning your inbox...",
            font_name=FONT_BODY,
            font_size="15sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="center",
            valign="center",
            size_hint_y=None,
            height=dp(120)
        )
        self._loading_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )
        self.ids.card_list.add_widget(self._loading_label)

        self._loading_messages = [
            "Scanning your inbox...",
            "Checking senders...",
            "Analysing subjects...",
            "Reading message content...",
            "Flagging suspicious emails...",
            "Almost there...",
        ]
        self._loading_index = 0
        self._loading_event = Clock.schedule_interval(
            self._cycle_loading_text, 2.5
        )
    def _cycle_loading_text(self, dt):
        """Cycles to the next loading message."""
        if not hasattr(self, '_loading_label'):
            return
        self._loading_index = (
            self._loading_index + 1
        ) % len(self._loading_messages)
        new_text = self._loading_messages[self._loading_index]
        self._loading_label.text = new_text  

    def _set_sync_loading_state(self, dt):
        """Runs on main thread: changes icon to a clock on every screen's sync button."""
        app = MDApp.get_running_app()
        for icon_id in SYNC_ICON_IDS:
            if icon_id in app.root.ids:
                app.root.ids[icon_id].icon = "clock-outline"

    def _do_scan_now(self):
        """Runs in background thread: does the heavy lifting."""
        run_daily_scan(force=True)
        Clock.schedule_once(self._finalize_sync)

    def show_scan_error(self, error_msg=""):
        """Shows an error message in the inbox when a scan fails."""
        self._scan_error = True
        self.ids.card_list.clear_widgets()
        self.ids.wipe_today_btn.disabled = True

        error_label = Label(
            text="Scan failed — check your internet connection and try again.",
            font_name=FONT_BODY,
            font_size="14sp",
            color=get_color_from_hex(COLOR_SECONDARY),
            halign="center",
            valign="center",
            size_hint_y=None,
            height=dp(80)
        )
        error_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        retry_container = BoxLayout(
            size_hint_y=None,
            height=dp(44),
            padding=[dp(16), 0, dp(16), 0]
        )

        retry_btn = Button(
            text="TAP SYNC TO RETRY",
            font_name=FONT_MONO,
            font_size="12sp",
            size_hint_x=1,
            background_normal="",
            background_color=get_color_from_hex(COLOR_SURFACE_CONTAINER_LOW),
            color=get_color_from_hex(COLOR_PRIMARY),
            on_release=lambda x: self.handle_scan_now()
        )

        from kivy.graphics import Color, Line
        with retry_btn.canvas.after:
            Color(rgba=get_color_from_hex(COLOR_PRIMARY))
            retry_border = Line(
                rectangle=(retry_btn.x, retry_btn.y, retry_btn.width, retry_btn.height),
                width=dp(1)
            )
        retry_btn.bind(
            pos=lambda inst, val: setattr(
                retry_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                retry_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        retry_container.add_widget(retry_btn)
        self.ids.card_list.add_widget(error_label)
        self.ids.card_list.add_widget(retry_container)

    def _finalize_sync(self, dt):
        self._scan_running = False
        if hasattr(self, '_loading_event') and self._loading_event:
            self._loading_event.cancel()
            self._loading_event = None

        app = MDApp.get_running_app()
        for icon_id in SYNC_ICON_IDS:
            if icon_id in app.root.ids:
                app.root.ids[icon_id].icon = "sync"

        Clock.schedule_once(lambda dt: self.refresh_list(), 0.1)

    def handle_bulk_wipe(self, instance=None):
        """Shows a confirmation dialog before wiping all flagged emails."""
        if not self.all_current_ids:
            return

        self._confirm_dialog = MDDialog(
            title="Wipe All Flagged Emails?",
            text=f"This will permanently trash all {len(self.all_current_ids)} flagged email(s). This cannot be undone from SpamReaper.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._dismiss_dialog
                ),
                MDFlatButton(
                    text="WIPE ALL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_SECONDARY),
                    on_release=self._confirm_wipe
                ),
            ]
        )
        self._confirm_dialog.open()

    def _dismiss_dialog(self, instance):
        """Closes the dialog without doing anything."""
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()

    def _confirm_wipe(self, instance):
        """User confirmed — dismiss dialog and proceed with deletion."""
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()
        threading.Thread(target=self._do_bulk_wipe, daemon=True).start()
        
    def _do_bulk_wipe(self):
        results = trash_multiple_emails(self.all_current_ids)
        for msg in self.all_messages:
            if msg["sms_id"] in results["succeeded"]:
                log_action(
                    sms_id=msg["sms_id"],
                    sender=msg["sender"],
                    subject=msg.get("subject", ""),
                    preview=msg.get("preview", ""),
                    action="deleted"
                )
        Clock.schedule_once(lambda dt: self._finish_bulk_wipe(results))

    def _finish_bulk_wipe(self, results):
        if results["failed"]:
            toast(f"{len(results['failed'])} email(s) could not be deleted")
        self.refresh_list()