from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.anchorlayout import AnchorLayout
from datetime import date
import csv

class ReminderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        self.selected_date = None
        self.login_dialog = None
        self.texts = {
            "choose_date": "Choose a date",
            "enter_reminder": "Enter reminder",
            "save": "Save",
            "open_calendar": "Open calendar",
            "reminder_saved": "Reminder saved",
            "date_cancelled": "Date selection cancelled",
            "ok": "OK",
            "theme": "Theme",
            "login_title": "Please log in",
            "login": "Login",
            "cancel": "Cancel",
            "username": "Username",
            "password": "Password"
        }
        main_layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40)
        top_controls = MDBoxLayout(orientation="horizontal", spacing=20, size_hint=(None, None), size=("240dp", "56dp"))
        theme_row = MDBoxLayout(orientation="horizontal", spacing=40, size_hint=(None, None), size=("160dp", "56dp"))
        self.theme_switch = MDSwitch(size_hint=(None, None), size=("36dp", "36dp"))
        self.theme_switch.bind(active=self.toggle_theme)

        self.theme_label = MDLabel(
            text=self.texts["theme"],
            halign="left",
            valign="middle",
            font_style="Subtitle1",
            size_hint=(None, None),
            size=("90dp", "56dp")
        )
        theme_row.add_widget(self.theme_switch)
        theme_row.add_widget(self.theme_label)
        top_controls.add_widget(theme_row)
        
        anchor = AnchorLayout(anchor_x="left", anchor_y="top", size_hint=(1, None), height="56dp")

        anchor.add_widget(top_controls)
        main_layout.add_widget(anchor)

        self.date_label = MDLabel(text=self.texts["choose_date"], halign="center", font_style="H5")
        self.reminder_input = MDTextField(hint_text=self.texts["enter_reminder"], size_hint_x=0.8, pos_hint={"center_x": 0.5})
        self.save_button = MDRaisedButton(text=self.texts["save"], pos_hint={"center_x": 0.5})
        self.save_button.bind(on_release=self.save_reminder)
        self.date_picker_button = MDRaisedButton(text=self.texts["open_calendar"], pos_hint={"center_x": 0.5})
        self.date_picker_button.bind(on_release=self.show_date_picker)

        main_layout.add_widget(self.date_label)
        main_layout.add_widget(self.reminder_input)
        main_layout.add_widget(self.save_button)
        main_layout.add_widget(self.date_picker_button)

        return main_layout

    def on_start(self):
        self.open_login_dialog()

    def toggle_theme(self, switch, value):
        self.theme_cls.theme_style = "Light" if value else "Dark"

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected, on_cancel=self.on_cancel)
        date_dialog.open()

    def open_login_dialog(self):
        if self.login_dialog:
            self.login_dialog.open()
            return
        content = MDBoxLayout(orientation="vertical", spacing=12, size_hint_y=None, height="160dp")

        self.username_field = MDTextField(hint_text=self.texts["username"], size_hint_x=0.9, pos_hint={"center_x": 0.5})
        self.password_field = MDTextField(hint_text=self.texts["password"], password=True, size_hint_x=0.9, pos_hint={"center_x": 0.5})


        content.add_widget(self.username_field)
        content.add_widget(self.password_field)


        login_button = MDRaisedButton(text=self.texts["login"], on_release=self._on_login_pressed)
        cancel_button = MDFlatButton(text=self.texts["cancel"], on_release=self._on_login_cancel)

        self.login_dialog = MDDialog(title=self.texts["login_title"], type="custom", content_cls=content, buttons=[cancel_button, login_button])
        self.login_dialog.open()

    def _on_login_pressed(self, instance):
        if self.login_dialog:
            self.login_dialog.dismiss()

    def _on_login_cancel(self, instance):
        if self.login_dialog:
            self.login_dialog.dismiss()

    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value
        self.date_label.text = f"{self.texts['choose_date']}: {value.strftime('%d.%m.%Y')}"

    def on_cancel(self, instance, value):
        self.date_label.text = self.texts["date_cancelled"]

    def save_reminder(self, instance):
        if self.selected_date and self.reminder_input.text:
            reminder_text = self.reminder_input.text
            date_str = self.selected_date.strftime('%d.%m.%Y')

            reminders = 'reminders' # Заменить на Юз

            with open(f'{reminders}.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([date_str, reminder_text])
            dialog = MDDialog(
                title=self.texts["reminder_saved"],
                text=f"{self.texts['choose_date']}: {date_str}\n{self.texts['enter_reminder']}: {reminder_text}",
                buttons=[MDRaisedButton(text=self.texts["ok"], on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()

if __name__ == "__main__":
    ReminderApp().run()





#Регистрация ????????????
#Окно для логина
#Проверка существования пользователя 
#Хэширование паролей?