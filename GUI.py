from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.dropdown import DropDown
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import re
import db_funtions as func

Window.size=(412,800)

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    helper_text= StringProperty()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class GUI(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue='700'
        self.account_type=None
        self.verifier=False
        self.career_id=None
        self.tutor_code=None
        self.dialog=None
        self.dpdown_user_type_items=[
            {
                "viewclass":  "IconListItem",
                "icon": "account",
                "text": "Maestro",
                "height": dp(56),
                "on_release": lambda x="Maestro": self.set_item_user(x)
            },
            {
                "viewclass":  "IconListItem",
                "icon": "account-school",
                "text": "Estudiante",
                "height": dp(56),
                "on_release": lambda x="Estudiante": self.set_item_user(x)
            }
        ]
        self.dpdown_career_items=[
            {
                "viewclass":  "IconListItem",
                "icon": "code-braces",
                "text": "Ingeniería de Sistemas",
                "height": dp(56),
                "on_release": lambda x="Ingeniería de Sistemas": self.set_item_career(x)
            },
            {
                "viewclass":  "IconListItem",
                "icon": "lightning-bolt",
                "text": "Ingeniería Electrónica",
                "height": dp(56),
                "on_release": lambda x="Ingeniería Electrónica": self.set_item_career(x)
            },
            {
                "viewclass":  "IconListItem",
                "icon": "account-school",
                "text": "Ingeniería Industrial",
                "height": dp(56),
                "on_release": lambda x="Ingeniería Industrial": self.set_item_career(x)
            }
        ]
        self.dpdown_signature_items=[
            {
                "viewclass":  "IconListItem",
                "icon": "account",
                "text": "Maestro",
                "height": dp(56),
                "on_release": lambda x="Maestro": self.set_item_user(x)
            },
        ]
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Builder.load_file("style/main.kv"))
        self.screen_manager.add_widget(Builder.load_file("style/login.kv"))
        self.screen_manager.add_widget(Builder.load_file("style/signup.kv"))
        self.screen_manager.add_widget(Builder.load_file("style/Inicio.kv"))
        self.screen_manager.add_widget(Builder.load_file("style/agendarTutoria.kv"))
        self.menu = MDDropdownMenu(
            caller=self.screen_manager.get_screen("signup").ids.usertype,
            items=self.dpdown_user_type_items,
            width_mult=3,
        )
        self.menu_career = MDDropdownMenu(
            caller=self.screen_manager.get_screen("signup").ids.career_list,
            ver_growth="up",
            hor_growth="right",
            items=self.dpdown_career_items,
            width_mult= 8,
        )
        self.menu_career.bind()
        self.menu.bind()

        return self.screen_manager
    #Calendario
    def show_date_picker(self):
        date_dialog=MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    #boton ok
    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)

    #boton cancelar
    def on_cancel(self, instance, value):
        self.root.ids.date_label.text="Cancelaste la operación"

    def set_item_user(self, text_item):
        self.screen_manager.get_screen("signup").ids.usertype.text=text_item
        self.screen_manager.get_screen("signup").ids.career_list.pos=(-6000,110)
        self.screen_manager.get_screen("signup").ids.code.pos=(-6000,110)
        if text_item=="Estudiante":
            self.screen_manager.get_screen("signup").ids.career_list.pos=(60,110)
            self.account_type=1
        elif text_item=="Maestro":
            self.screen_manager.get_screen("signup").ids.code.pos=(60,110)
            self.account_type=2
        self.menu.dismiss()

    def set_item_career(self, text_item):
        self.screen_manager.get_screen("signup").ids.career_list.text=text_item
        if text_item=="Ingeniería de Sistemas":
            self.career_id=1
        elif text_item=="Ingeniería Electrónica":
            self.career_id=2
        elif text_item=="Ingeniería Industrial":
            self.career_id=3
        self.menu_career.dismiss()

    def show_alert_dialog(self,text):
        if not self.dialog:
            self.dialog = MDDialog(
                text=text,
                buttons=[
                    MDFlatButton(
                        text="Intentar de nuevo",
                        theme_text_color="Custom",
                        on_release=self.close_dialog
                    )
                ],
            )
        self.dialog.open()
    
    def close_dialog(self,ob):
        self.dialog.dismiss()

    def is_empty(self,text):
        if text=="" or " ":
            return True
        else:
            return False

    def verify_email_signup(self):
        emailConfirmPattern=re.compile(r"^[A-Za-z0-9]+@ucentral\.edu\.co$")
        text=self.screen_manager.get_screen("signup").ids.newemail.text
        if re.fullmatch(emailConfirmPattern,text):
            self.verifier= True
        else:
            self.verifier= False
            self.screen_manager.get_screen("signup").ids.newemail.helper_text="el correo instucional debe ser de la(ej. correo@ucentral.edu.co)"
            self.screen_manager.get_screen("signup").ids.newemail.error=True

    def verify_password_signup(self):
        verifypass1 = self.screen_manager.get_screen("signup").ids.newpassword.ids.text_field.text
        verifypass2 = self.screen_manager.get_screen("signup").ids.verifypassword.ids.text_field.text

        if verifypass1 == verifypass2:
            self.verifier= True
        else:
            self.verifier= False
            self.screen_manager.get_screen("signup").ids.verifypassword.helper_text="Las contraseñas no coinciden"
            self.screen_manager.get_screen("signup").ids.verifypassword.ids.text_field.error=True

    def save_data_signup(self):
        nombre=self.screen_manager.get_screen("signup").ids.newnombre.text
        email = self.screen_manager.get_screen("signup").ids.newemail.text
        verifypass1 = self.screen_manager.get_screen("signup").ids.newpassword.ids.text_field.text
        cedula = self.screen_manager.get_screen("signup").ids.cedula.text
        usertype = self.screen_manager.get_screen("signup").ids.usertype.text
        careerlist = self.screen_manager.get_screen("signup").ids.career_list.text
        codeT = self.screen_manager.get_screen("signup").ids.code.text
        self.tutor_code=codeT
        self.verify_email_signup()
        self.verify_password_signup()
        if self.verifier:
            if self.account_type==1:
                func.new_user(cedula,email,verifypass1,nombre,self.account_type,career_id=self.career_id)
            elif self.account_type==2:
                func.new_user(cedula,email,verifypass1,nombre,self.account_type,tutor_c=self.tutor_code)

    #---Login----
    def verify_email_login(self):
        emailConfirmPattern=re.compile(r"^[A-Za-z0-9]+@ucentral\.edu\.co$")
        text=self.screen_manager.get_screen("login").ids.emailEstablecido.text
        if re.fullmatch(emailConfirmPattern,text):
            self.verifier= True
        else:
            self.verifier= False
            self.screen_manager.get_screen("login").ids.emailEstablecido.helper_text="el correo instucional debe ser de la(ej. correo@ucentral.edu.co)"
            self.screen_manager.get_screen("login").ids.emailEstablecido.error=True

    def save_data_login(self):
        user_logged=False
        email_log=self.screen_manager.get_screen("login").ids.emailEstablecido.text
        password_log =self.screen_manager.get_screen("login").ids.passwordEstablecida.ids.text_field.text
        self.verify_email_login()
        if self.verifier:
            comp=func.login(email_log,password_log)
            if comp[0]==False:
                self.show_alert_dialog("El email no se encuentra registrado!")
            elif comp[1]==False:
                self.show_alert_dialog("La contraseña no corresponde al usuario registrado!")
            else:
                user_logged=True
        return user_logged


#----Agendar tutorias------


if __name__ == "__main__":
    LabelBase.register(name="zapf",fn_regular="fonts/zapf.ttf")
    LabelBase.register(name="galliard",fn_regular="fonts/galliard-bt-bold.ttf")
    GUI().run()