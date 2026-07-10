import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.app import MDApp

from email_deleter import untrash_email, trash_email
from tracker_db import get_action_history, delete_history_record, log_action
from theme import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ON_SURFACE,
    COLOR_ON_SURFACE_VARIANT,
    COLOR_SURFACE_CONTAINER_LOW,
    COLOR_OUTLINE_VARIANT,
    COLOR_OUTLINE,
    FONT_HEADING,
    FONT_BODY,
    FONT_MONO,
    get_urgency_color,
)


class HistoryCard(MDCard):
    """
    A single history record — shows sender, subject, action taken,
    date, and either a Restore button (deleted) or Delete button (kept).
    """

    def __init__(self, record, on_action_complete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.adaptive_height = True
        self.padding = dp(16)
        self.spacing = dp(8)
        self.record = record
        self.on_action_complete = on_action_complete

        # Draw colored border based on action type
        action = record["action"]
        border_color = get_color_from_hex(
            COLOR_SECONDARY if action == "deleted" else COLOR_PRIMARY
        )

        with self.canvas.after:
            Color(rgba=border_color)
            self.border_line = Line(
                rectangle=(self.x, self.y, self.width, self.height),
                width=dp(1)
            )
        self.bind(
            pos=lambda inst, val: setattr(
                self.border_line, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                self.border_line, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        # Top row — sender + action badge
        top_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(24)
        )

        sender_lbl = Label(
            text=record.get("sender", "Unknown Sender"),
            font_name=FONT_BODY,
            font_size="13sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="center",
            shorten=True,
            shorten_from="right",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(24)
        )
        sender_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        action_badge = Label(
            text="DELETED" if action == "deleted" else "KEPT",
            font_name=FONT_MONO,
            font_size="11sp",
            bold=True,
            color=border_color,
            halign="right",
            valign="center",
            size_hint_x=None,
            width=dp(72),
            size_hint_y=None,
            height=dp(24)
        )

        top_row.add_widget(sender_lbl)
        top_row.add_widget(action_badge)

        # Subject
        subject_lbl = Label(
            text=record.get("subject") or "(No subject)",
            font_name=FONT_HEADING,
            font_size="14sp",
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

        # Date + countdown row
        date_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(20)
        )

        date_lbl = Label(
            text=f"Actioned on {record['actioned_on']}",
            font_name=FONT_MONO,
            font_size="11sp",
            color=get_color_from_hex(COLOR_OUTLINE),
            halign="left",
            valign="center",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(20)
        )
        date_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        date_row.add_widget(date_lbl)

        # Restore countdown — only for deleted emails
        if action == "deleted":
            days_left = record.get("days_until_permanent", 0)
            if days_left > 0:
                if days_left <= 3:
                    countdown_color = get_color_from_hex(COLOR_SECONDARY)
                elif days_left <= 7:
                    countdown_color = get_color_from_hex("#8a4300")
                else:
                    countdown_color = get_color_from_hex(COLOR_PRIMARY)

                countdown_lbl = Label(
                    text=f"RESTORABLE FOR {days_left} MORE {'DAY' if days_left == 1 else 'DAYS'}",
                    font_name=FONT_MONO,
                    font_size="11sp",
                    bold=True,
                    color=countdown_color,
                    halign="right",
                    valign="center",
                    size_hint_x=None,
                    width=dp(220),
                    size_hint_y=None,
                    height=dp(20)
                )
                date_row.add_widget(countdown_lbl)
            else:
                permanent_lbl = Label(
                    text="PERMANENTLY DELETED",
                    font_name=FONT_MONO,
                    font_size="11sp",
                    bold=True,
                    color=get_color_from_hex(COLOR_OUTLINE),
                    halign="right",
                    valign="center",
                    size_hint_x=None,
                    width=dp(200),
                    size_hint_y=None,
                    height=dp(20)
                )
                date_row.add_widget(permanent_lbl)

        # Action button row
        btn_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(44),
            spacing=dp(8)
        )

        if action == "deleted":
            days_left = record.get("days_until_permanent", 0)
            restore_btn = Button(
                text="RESTORE TO INBOX",
                font_name=FONT_HEADING,
                font_size="13sp",
                size_hint_x=1,
                background_normal="",
                background_color=get_color_from_hex(COLOR_PRIMARY),
                color=(1, 1, 1, 1),
                disabled=days_left <= 0,
                on_release=self._on_restore
            )
            btn_row.add_widget(restore_btn)

        elif action == "kept":
            delete_btn = Button(
                text="DELETE NOW",
                font_name=FONT_HEADING,
                font_size="13sp",
                size_hint_x=1,
                background_normal="",
                background_color=get_color_from_hex(COLOR_SECONDARY),
                color=(1, 1, 1, 1),
                on_release=self._on_delete_kept
            )
            btn_row.add_widget(delete_btn)

        self.add_widget(top_row)
        self.add_widget(subject_lbl)
        self.add_widget(date_row)
        self.add_widget(btn_row)

    def _on_restore(self, instance):
        """Restores a deleted email from Gmail Trash back to inbox."""
        threading.Thread(target=self._do_restore, daemon=True).start()

    def _do_restore(self):
        success = untrash_email(self.record["sms_id"])
        if success:
            delete_history_record(self.record["sms_id"])
            Clock.schedule_once(lambda dt: self.on_action_complete())
        else:
            Clock.schedule_once(lambda dt: self._show_restore_failed())

    def _show_restore_failed(self):
        """Shows an inline error if restore failed."""
        from kivymd.toast import toast
        toast("Could not restore — email may have been permanently deleted by Gmail")

    def _on_delete_kept(self, instance):
        """Permanently deletes a kept email via Gmail API."""
        threading.Thread(target=self._do_delete_kept, daemon=True).start()

    def _do_delete_kept(self):
        success = trash_email(self.record["sms_id"])
        if success:
            delete_history_record(self.record["sms_id"])
            Clock.schedule_once(lambda dt: self.on_action_complete())
        else:
            Clock.schedule_once(lambda dt: self._show_delete_failed())

    def _show_delete_failed(self):
        from kivymd.toast import toast
        toast("Could not delete — email may no longer exist in Gmail")


class HistoryScreen(MDBoxLayout):
    """
    History screen — shows all previously actioned emails,
    grouped into Deleted and Kept sections.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, *args):
        # Clear existing content
        if hasattr(self, 'scroll'):
            self.remove_widget(self.scroll)

        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.card_list = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(12),
            padding=[dp(16), dp(16), dp(16), dp(32)]
        )
        self.card_list.bind(
            minimum_height=self.card_list.setter('height')
        )

        self.scroll.add_widget(self.card_list)
        self.add_widget(self.scroll)

        history = get_action_history()

        if not history:
            self._show_empty_state()
            return

        # Split into deleted and kept
        deleted = [r for r in history if r["action"] == "deleted"]
        kept = [r for r in history if r["action"] == "kept"]

        if deleted:
            self._add_section_header("DELETED EMAILS", COLOR_SECONDARY)
            for record in deleted:
                self.card_list.add_widget(
                    HistoryCard(record, self.refresh_list)
                )

        if kept:
            self._add_section_header("KEPT EMAILS", COLOR_PRIMARY)
            for record in kept:
                self.card_list.add_widget(
                    HistoryCard(record, self.refresh_list)
                )

    def _add_section_header(self, text, color_hex):
        header = Label(
            text=text,
            font_name=FONT_HEADING,
            font_size="14sp",
            bold=True,
            underline=True,
            color=get_color_from_hex(color_hex),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(32)
        )
        header.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )
        self.card_list.add_widget(header)

    def _show_empty_state(self):
        self.card_list.add_widget(Label(
            text="No history yet.\nDeleted and kept emails will appear here.",
            font_name=FONT_BODY,
            font_size="15sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="center",
            valign="center",
            size_hint_y=None,
            height=dp(120)
        ))