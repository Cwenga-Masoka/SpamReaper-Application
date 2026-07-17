import threading
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Line
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast

from email_deleter import untrash_email, trash_email, untrash_multiple_emails, trash_multiple_emails
from tracker_db import (
    get_action_history,
    delete_history_record,
    delete_history_records_bulk,
    clear_action_history,
)
from theme import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ON_SURFACE,
    COLOR_ON_SURFACE_VARIANT,
    COLOR_OUTLINE_VARIANT,
    COLOR_OUTLINE,
    FONT_HEADING,
    FONT_BODY,
    FONT_MONO,
)


class HistorySectionHeader(MDBoxLayout):
    """
    Section header for a group of history records (Deleted or Kept),
    with a bulk action button — Restore All or Delete All — mirroring
    the CLEAR button pattern on the Inbox screen's SectionHeader.
    """
    def __init__(self, title_text, color_hex, records, action_type,
                 on_action_complete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "40dp"
        self.padding = ["4dp", "8dp", "4dp", "4dp"]
        self.spacing = "12dp"

        self.records = records
        self.action_type = action_type  # "restore" or "delete_kept"
        self.on_action_complete = on_action_complete
        self._confirm_dialog = None
        self._progress_dialog = None

        color = get_color_from_hex(color_hex)

        self.title_label = Label(
            text=title_text,
            font_name=FONT_HEADING,
            bold=True,
            underline=True,
            color=color,
            size_hint_x=1,
            halign="left",
            valign="center"
        )
        self.title_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        btn_text = "RESTORE ALL" if action_type == "restore" else "DELETE ALL"
        self.action_btn = MDFlatButton(
            text=btn_text,
            theme_text_color="Custom",
            text_color=color,
            size_hint_x=None,
            on_release=self.show_confirm_dialog
        )

        self.add_widget(self.title_label)
        self.add_widget(self.action_btn)

    def show_confirm_dialog(self, instance):
        count = len(self.records)
        if self.action_type == "restore":
            title = "Restore All Deleted Emails?"
            text = f"This will restore all {count} email(s) in this group from Gmail's Trash back to your inbox."
            confirm_label = "RESTORE ALL"
        else:
            title = "Permanently Delete All Kept Emails?"
            text = f"This will permanently trash all {count} kept email(s) in this group. This cannot be undone from SpamReaper."
            confirm_label = "DELETE ALL"

        self._confirm_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._dismiss_dialog
                ),
                MDFlatButton(
                    text=confirm_label,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_SECONDARY),
                    on_release=self._confirm_action
                ),
            ]
        )
        self._confirm_dialog.open()

    def _dismiss_dialog(self, instance):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()

    def _confirm_action(self, instance):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()

        verb = "Restoring" if self.action_type == "restore" else "Deleting"
        self._progress_dialog = MDDialog(
            title=f"{verb} {len(self.records)} email(s)...",
            text="Please wait, this may take a moment.",
            auto_dismiss=False
        )
        self._progress_dialog.open()

        threading.Thread(target=self._do_bulk_action, daemon=True).start()

    def _do_bulk_action(self):
        sms_ids = [r["sms_id"] for r in self.records]

        if self.action_type == "restore":
            results = untrash_multiple_emails(sms_ids)
        else:
            results = trash_multiple_emails(sms_ids)

        delete_history_records_bulk(results["succeeded"])
        Clock.schedule_once(lambda dt: self._finish_bulk_action(results))

    def _finish_bulk_action(self, results):
        if self._progress_dialog:
            self._progress_dialog.dismiss()
            self._progress_dialog = None

        if results["failed"]:
            verb = "restored" if self.action_type == "restore" else "deleted"
            toast(f"{len(results['failed'])} email(s) could not be {verb}")

        self.on_action_complete()


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
        self._confirm_dialog = None

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
        """Confirmation dialog before restoring — mirrors the Inbox pattern."""
        self._confirm_dialog = MDDialog(
            title="Restore This Email?",
            text="This will move the email from Gmail's Trash back to your inbox.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._dismiss_dialog
                ),
                MDFlatButton(
                    text="RESTORE",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._confirm_restore
                ),
            ]
        )
        self._confirm_dialog.open()

    def _dismiss_dialog(self, instance):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()

    def _confirm_restore(self, instance):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()
        threading.Thread(target=self._do_restore, daemon=True).start()

    def _do_restore(self):
        success = untrash_email(self.record["sms_id"])
        if success:
            delete_history_record(self.record["sms_id"])
            Clock.schedule_once(lambda dt: toast("Restored to inbox"))
            Clock.schedule_once(lambda dt: self.on_action_complete())
        else:
            Clock.schedule_once(lambda dt: self._show_restore_failed())

    def _show_restore_failed(self):
        toast("Could not restore — email may have been permanently deleted by Gmail")

    def _on_delete_kept(self, instance):
        """Confirmation dialog before permanently deleting — mirrors the Inbox pattern."""
        self._confirm_dialog = MDDialog(
            title="Permanently Delete This Email?",
            text="This will trash the email in Gmail. This cannot be undone from SpamReaper.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._dismiss_dialog
                ),
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_SECONDARY),
                    on_release=self._confirm_delete_kept
                ),
            ]
        )
        self._confirm_dialog.open()

    def _confirm_delete_kept(self, instance):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()
        threading.Thread(target=self._do_delete_kept, daemon=True).start()

    def _do_delete_kept(self):
        success = trash_email(self.record["sms_id"])
        if success:
            delete_history_record(self.record["sms_id"])
            Clock.schedule_once(lambda dt: toast("Permanently deleted"))
            Clock.schedule_once(lambda dt: self.on_action_complete())
        else:
            Clock.schedule_once(lambda dt: self._show_delete_failed())

    def _show_delete_failed(self):
        toast("Could not delete — email may no longer exist in Gmail")


class HistoryScreen(MDBoxLayout):
    """
    History screen — shows all previously actioned emails, grouped into
    Deleted and Kept sections, each with a bulk action button, plus a
    page-level Clear History button.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self._clear_history_dialog = None
        Clock.schedule_once(self.refresh_list, 0.1)

    def refresh_list(self, *args):
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

        self._add_clear_history_button()

        deleted = [r for r in history if r["action"] == "deleted"]
        kept = [r for r in history if r["action"] == "kept"]

        if deleted:
            self.card_list.add_widget(
                HistorySectionHeader(
                    title_text="DELETED EMAILS",
                    color_hex=COLOR_SECONDARY,
                    records=deleted,
                    action_type="restore",
                    on_action_complete=self.refresh_list
                )
            )
            for record in deleted:
                self.card_list.add_widget(
                    HistoryCard(record, self.refresh_list)
                )

        if kept:
            self.card_list.add_widget(
                HistorySectionHeader(
                    title_text="KEPT EMAILS",
                    color_hex=COLOR_PRIMARY,
                    records=kept,
                    action_type="delete_kept",
                    on_action_complete=self.refresh_list
                )
            )
            for record in kept:
                self.card_list.add_widget(
                    HistoryCard(record, self.refresh_list)
                )

    def _add_clear_history_button(self):
        """
        Page-level button to wipe all local history records at once.
        This only clears SpamReaper's local record of past actions —
        it does not touch anything in Gmail itself.
        """
        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
            padding=[0, 0, 0, dp(4)]
        )

        spacer = Label(text="", size_hint_x=1)

        clear_btn = MDFlatButton(
            text="CLEAR HISTORY",
            theme_text_color="Custom",
            text_color=get_color_from_hex(COLOR_OUTLINE),
            size_hint_x=None,
            on_release=self._show_clear_history_dialog
        )

        row.add_widget(spacer)
        row.add_widget(clear_btn)
        self.card_list.add_widget(row)

    def _show_clear_history_dialog(self, instance):
        self._clear_history_dialog = MDDialog(
            title="Clear All History?",
            text="This removes SpamReaper's local record of past actions. "
                 "It does not restore or delete anything in Gmail itself.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_PRIMARY),
                    on_release=self._dismiss_clear_history_dialog
                ),
                MDFlatButton(
                    text="CLEAR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(COLOR_SECONDARY),
                    on_release=self._confirm_clear_history
                ),
            ]
        )
        self._clear_history_dialog.open()

    def _dismiss_clear_history_dialog(self, instance):
        if self._clear_history_dialog:
            self._clear_history_dialog.dismiss()

    def _confirm_clear_history(self, instance):
        if self._clear_history_dialog:
            self._clear_history_dialog.dismiss()
        clear_action_history()
        toast("History cleared")
        self.refresh_list()

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