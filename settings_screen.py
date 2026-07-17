import os
import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.app import MDApp

from config_manager import get_setting, save_setting
from tracker_db import initialize_db
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
)


class SettingsScreen(MDBoxLayout):
    """
    Settings screen — three sections:
    1. Review Window slider
    2. Spam Keywords tag editor
    3. Account actions (disconnect, clear history)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Scrollable content area
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)

        self.content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(16),
            padding=[dp(16), dp(16), dp(16), dp(32)]
        )
        self.content.bind(
            minimum_height=self.content.setter('height')
        )

        scroll.add_widget(self.content)
        self.add_widget(scroll)

        # Build each section
        Clock.schedule_once(self._build_ui, 0)

    def _build_ui(self, dt):
        self._build_page_title()
        self._build_review_window_section()
        self._build_keywords_section()
        self._build_notifications_section()
        self._build_account_section()

    def _build_page_title(self):
        """Page title and subtitle — 'SETTINGS / Configure surgical cleanup protocols.'"""
        title_block = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(52),
            spacing=dp(4)
        )

        title = Label(
            text="SETTINGS",
            font_name=FONT_HEADING,
            bold=True,
            font_size="20sp",
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(28)
        )
        title.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))

        subtitle = Label(
            text="Configure surgical cleanup protocols.",
            font_name=FONT_BODY,
            font_size="14sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(20)
        )
        subtitle.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))

        title_block.add_widget(title)
        title_block.add_widget(subtitle)
        self.content.add_widget(title_block)


    def _build_review_window_section(self):
        """Slider for days_before_deletion — range 1 to 30."""
        current_days = get_setting("days_before_deletion") or 5

        # Section card
        section = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(16),
            spacing=dp(12),
            md_bg_color=get_color_from_hex("#ffffff")
        )

        # Draw card border
        from kivy.graphics import Color, Line
        with section.canvas.after:
            Color(rgba=get_color_from_hex(COLOR_OUTLINE_VARIANT))
            self.review_border = Line(
                rectangle=(section.x, section.y, section.width, section.height),
                width=dp(1)
            )
        section.bind(
            pos=lambda inst, val: setattr(
                self.review_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                self.review_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        # Header row: label + current value badge
        header_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(32)
        )

        section_title = Label(
            text="REVIEW WINDOW",
            font_name=FONT_MONO,
            font_size="13sp",
            bold=True,
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="left",
            valign="center",
            size_hint_x=1
        )
        section_title.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))

        self.days_badge = Label(
            text=f"{current_days} {'DAY' if current_days == 1 else 'DAYS'}",
            font_name=FONT_MONO,
            font_size="13sp",
            color=get_color_from_hex("#071e27"),
            halign="right",
            valign="center",
            size_hint_x=None,
            width=dp(80)
        )

        header_row.add_widget(section_title)
        header_row.add_widget(self.days_badge)

        # Description
        desc = Label(
            text="Days emails remain in reaper-vault before permanent extraction.",
            font_name=FONT_BODY,
            font_size="14sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        desc.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        desc.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        # Slider
        self.days_slider = MDSlider(
            min=1,
            max=30,
            value=current_days,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex(COLOR_PRIMARY)
        )
        self.days_slider.bind(value=self._on_slider_value_display)
        self.days_slider.bind(on_touch_up=self._on_slider_released)

        # Range labels row
        range_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(16),
            padding=0
        )
        left_label = Label(
            text="1D",
            font_name=FONT_MONO,
            font_size="11sp",
            color=get_color_from_hex(COLOR_OUTLINE),
            halign="left",
            valign="center",
            size_hint_x=1
        )
        left_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )
        right_label = Label(
            text="30D",
            font_name=FONT_MONO,
            font_size="11sp",
            color=get_color_from_hex(COLOR_OUTLINE),
            halign="right",
            valign="center",
            size_hint_x=1
        )
        right_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        range_row.add_widget(left_label)
        range_row.add_widget(right_label)

        section.add_widget(header_row)
        section.add_widget(desc)
        section.add_widget(self.days_slider)
        section.add_widget(range_row)

        # Fix section height after adding children
        section.bind(minimum_height=section.setter('height'))

        self.content.add_widget(section)


    def _on_slider_value_display(self, instance, value):
        """Updates the badge display only — no disk write."""
        days = int(value)
        self.days_badge.text = f"{days} {'DAY' if days == 1 else 'DAYS'}"
        if days <= 3:
            self.days_badge.color = get_color_from_hex("#da3433")
        else:
            self.days_badge.color = get_color_from_hex("#071e27")

    def _on_slider_released(self, instance, touch):
        """Saves to config when user releases slider, then refreshes inbox."""
        if instance.collide_point(*touch.pos):
            days = int(instance.value)
            save_setting("days_before_deletion", days)

            # Refresh the inbox so day counts update immediately
            app = MDApp.get_running_app()
            for widget in app.root.walk():
                from review_screen import ReviewScreen
                if isinstance(widget, ReviewScreen):
                    widget.refresh_list()
                    break

    def _build_notifications_section(self):
        """Lets the user jump to system settings to re-enable notifications
        if they dismissed or denied the prompt initially."""
        from kivy.graphics import Color, Line

        section = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(16),
            spacing=dp(12),
            md_bg_color=get_color_from_hex("#ffffff")
        )

        with section.canvas.after:
            Color(rgba=get_color_from_hex(COLOR_OUTLINE_VARIANT))
            self.notif_border = Line(
                rectangle=(section.x, section.y, section.width, section.height),
                width=dp(1)
            )
        section.bind(
            pos=lambda inst, val: setattr(
                self.notif_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                self.notif_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        section_title = Label(
            text="NOTIFICATIONS",
            font_name=FONT_MONO,
            font_size="13sp",
            bold=True,
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(24)
        )
        section_title.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))

        notif_btn = Button(
            text="ENABLE NOTIFICATIONS",
            font_name=FONT_HEADING,
            font_size="14sp",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=get_color_from_hex("#e7e8e9"),
            color=get_color_from_hex(COLOR_PRIMARY),
            on_release=self._open_notification_settings
        )

        notif_desc = Label(
            text="If you dismissed the notification prompt, tap here to enable "
                "deletion reminders in Android's app settings.",
            font_name=FONT_BODY,
            font_size="13sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        notif_desc.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        notif_desc.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        section.add_widget(section_title)
        section.add_widget(notif_btn)
        section.add_widget(notif_desc)
        section.bind(minimum_height=section.setter('height'))

        self.content.add_widget(section)

    def _build_keywords_section(self):
        """Tag editor for spam keywords — add new ones, remove existing ones."""
        keywords = get_setting("spam_keywords") or []

        # Section card
        section = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(16),
            spacing=dp(12),
            md_bg_color=get_color_from_hex("#ffffff")
        )

        from kivy.graphics import Color, Line
        with section.canvas.after:
            Color(rgba=get_color_from_hex(COLOR_OUTLINE_VARIANT))
            self.keywords_border = Line(
                rectangle=(section.x, section.y, section.width, section.height),
                width=dp(1)
            )
        section.bind(
            pos=lambda inst, val: setattr(
                self.keywords_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                self.keywords_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        # Section title
        section_title = Label(
            text="SPAM KEYWORDS",
            font_name=FONT_MONO,
            font_size="13sp",
            bold=True,
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(24)
        )
        section_title.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        # Description
        desc = Label(
            text="Messages containing these terms are flagged for removal.",
            font_name=FONT_BODY,
            font_size="14sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        desc.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        desc.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        self.tags_container = GridLayout(
            cols=4,
            size_hint_y=None,
            spacing=dp(8),
            padding=[0, dp(4), 0, dp(4)]
        )
        self.tags_container.bind(
            minimum_height=self.tags_container.setter('height')
        )

        # Recalculate columns when width changes
        def update_cols(instance, width):
            # Each tag is roughly 120dp wide — fit as many as possible
            # but never fewer than 1 or more than 4
            col_count = max(1, min(4, int(width / dp(120))))
            instance.cols = col_count

        self.tags_container.bind(width=update_cols)

        # Populate existing tags
        for keyword in keywords:
            self._add_keyword_tag(keyword)

        # Divider between tags and input field
        divider_line = MDBoxLayout(
            size_hint_y=None,
            height=dp(1),
            md_bg_color=get_color_from_hex(COLOR_OUTLINE_VARIANT)
        )

        add_label = Label(
            text="ADD KEYWORD",
            font_name=FONT_MONO,
            font_size="11sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(20)
        )
        add_label.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        # Input row
        input_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(44),
            spacing=dp(8)
        )

        self.keyword_input = MDTextField(
            hint_text="Add custom keyword...",
            font_name=FONT_BODY,
            size_hint_x=1,
            mode="rectangle"
        )

        add_btn = Button(
            text="ADD",
            font_name=FONT_MONO,
            font_size="13sp",
            size_hint_x=None,
            width=dp(72),
            background_normal="",
            background_color=get_color_from_hex(COLOR_PRIMARY),
            color=(1, 1, 1, 1),
            on_release=self._on_add_keyword
        )

        input_row.add_widget(self.keyword_input)
        input_row.add_widget(add_btn)

        section.add_widget(section_title)
        section.add_widget(desc)
        section.add_widget(self.tags_container)
        section.add_widget(divider_line)
        section.add_widget(add_label)
        section.add_widget(input_row)
        section.bind(minimum_height=section.setter('height'))

        self.content.add_widget(section)


    def _add_keyword_tag(self, keyword):
        """Creates a single keyword tag with an X remove button."""
        from kivy.graphics import Color, Line

        tag = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(32),
            spacing=dp(4),
            padding=[dp(8), dp(4), dp(4), dp(4)],
        )

        with tag.canvas.before:
            Color(rgba=get_color_from_hex(COLOR_OUTLINE_VARIANT))
            tag_border = Line(
                rectangle=(tag.x, tag.y, tag.width, tag.height),
                width=dp(1)
            )
        tag.bind(
            pos=lambda inst, val: setattr(
                tag_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                tag_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        word_lbl = Label(
            text=keyword,
            font_name=FONT_MONO,
            font_size="11sp",
            color=get_color_from_hex(COLOR_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="center"
        )
        word_lbl.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        remove_btn = Button(
            text="x",
            font_size="12sp",
            size_hint_x=None,
            width=dp(24),
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            on_release=lambda inst, kw=keyword, t=tag: self._on_remove_keyword(kw, t)
        )

        tag.add_widget(word_lbl)
        tag.add_widget(remove_btn)
        self.tags_container.add_widget(tag)

    def _on_add_keyword(self, instance):
        """Adds a new keyword to config and refreshes the tag list."""
        new_word = self.keyword_input.text.strip().lower()
        if not new_word:
            return

        keywords = get_setting("spam_keywords") or []
        if new_word in keywords:
            self.keyword_input.text = ""
            self._dismiss_keyboard()
            return

        keywords.append(new_word)
        save_setting("spam_keywords", keywords)
        self.keyword_input.text = ""
        self._dismiss_keyboard()
        self._add_keyword_tag(new_word)


    def _dismiss_keyboard(self):
        """Dismisses the soft keyboard — works on both Android and desktop."""
        from kivy.core.window import Window
        Window.release_all_keyboards()

    def _on_remove_keyword(self, keyword, tag_widget):
        """Removes a keyword from config and removes its tag widget."""
        keywords = get_setting("spam_keywords") or []
        if keyword in keywords:
            keywords.remove(keyword)
            save_setting("spam_keywords", keywords)
        self.tags_container.remove_widget(tag_widget)

    def _open_notification_settings(self, instance):
        """
        Opens Android's system notification settings screen for this app.
        We can't reliably re-trigger the permission popup after a denial,
        so this sends the user to Settings to flip it back on manually.
        """
        import platform
        if platform.system() != 'Linux':
            print("Notification settings only available on Android.")
            return
        try:
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            Settings = autoclass('android.provider.Settings')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            activity = PythonActivity.mActivity
            package_name = activity.getPackageName()

            intent = Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
            intent.putExtra(Settings.EXTRA_APP_PACKAGE, package_name)
            activity.startActivity(intent)
        except Exception as e:
            print(f"Could not open notification settings: {e}")
            from kivymd.toast import toast
            toast("Could not open notification settings")

    def _build_account_section(self):
        """Account actions — disconnect Gmail and clear history."""
        from kivy.graphics import Color, Line

        # Section card
        section = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(16),
            spacing=dp(12),
            md_bg_color=get_color_from_hex("#ffffff")
        )

        with section.canvas.after:
            Color(rgba=get_color_from_hex(COLOR_OUTLINE_VARIANT))
            self.account_border = Line(
                rectangle=(section.x, section.y, section.width, section.height),
                width=dp(1)
            )
        section.bind(
            pos=lambda inst, val: setattr(
                self.account_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            ),
            size=lambda inst, val: setattr(
                self.account_border, 'rectangle',
                (inst.x, inst.y, inst.width, inst.height)
            )
        )

        # Section title
        section_title = Label(
            text="ACCOUNT",
            font_name=FONT_MONO,
            font_size="13sp",
            bold=True,
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="left",
            valign="center",
            size_hint_y=None,
            height=dp(24)
        )
        section_title.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        # Disconnect Gmail button
        disconnect_btn = Button(
            text="DISCONNECT GMAIL",
            font_name=FONT_HEADING,
            font_size="14sp",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=get_color_from_hex("#e7e8e9"),
            color=get_color_from_hex(COLOR_PRIMARY),
            on_release=self._on_disconnect_gmail
        )

        disconnect_desc = Label(
            text="Removes your saved login. You will need to reconnect on next launch.",
            font_name=FONT_BODY,
            font_size="13sp",
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        disconnect_desc.bind(
            texture_size=lambda inst, val: setattr(inst, 'height', val[1])
        )
        disconnect_desc.bind(
            width=lambda inst, val: setattr(inst, 'text_size', (val, None))
        )

        section.add_widget(section_title)
        section.add_widget(disconnect_btn)
        section.add_widget(disconnect_desc)
        section.bind(minimum_height=section.setter('height'))

        self.content.add_widget(section)

        # Danger zone — delete everything
        danger_btn = Button(
            text="DELETE ACCOUNT & DATA",
            font_name=FONT_MONO,
            font_size="11sp",
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=get_color_from_hex("#f8f9fa"),
            color=get_color_from_hex(COLOR_ON_SURFACE_VARIANT),
            on_release=self._on_delete_all
        )
        self.content.add_widget(danger_btn)


    def _on_disconnect_gmail(self, instance):
        """Deletes the saved token file and shows a restart confirmation."""
        token_path = "./gmail_token.json"
        if os.path.exists(token_path):
            os.remove(token_path)
            print("Gmail token deleted.")

        # Show confirmation label
        self.content.add_widget(Label(
            text="Disconnected. Please restart SpamReaper to reconnect your Gmail account.",
            font_name=FONT_BODY,
            font_size="13sp",
            color=get_color_from_hex(COLOR_PRIMARY),
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(48)
        ))


    def _on_clear_history(self, instance):
        """Clears all flagged message records from the local database."""
        import sqlite3
        from config_manager import get_setting as gs
        db_name = gs("database_name") or "spamreaper.db"
        conn = sqlite3.connect(db_name)
        conn.execute("DELETE FROM flagged_messages")
        conn.commit()
        conn.close()
        print("History cleared.")

        # Refresh the inbox list so it shows the empty state
        app = MDApp.get_running_app()
        for widget in app.root.walk():
            from review_screen import ReviewScreen
            if isinstance(widget, ReviewScreen):
                widget.refresh_list()
                break

        # Confirm to user
        self.content.add_widget(Label(
            text="History cleared. All flagged records removed.",
            font_name=FONT_BODY,
            font_size="13sp",
            color=get_color_from_hex("#ba1a1a"),
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(32)
        ))


    def _on_delete_all(self, instance):
        """Deletes token AND clears the database — full reset."""
        self._on_clear_history(instance)
        self._on_disconnect_gmail(instance)