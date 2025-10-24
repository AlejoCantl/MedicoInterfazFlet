import flet as ft
import os

class LoginView:
    def __init__(self, page: ft.Page, api_client, on_login_success):
        self.page = page
        self.api = api_client
        self.on_login_success = on_login_success

        # Colores
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"
        self.COLOR_ERROR = "#DC3545"

        # Rutas
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "assets", "images")
        self.bg_path = os.path.join(assets_dir, "fondo.jpeg")
        self.logo_path = os.path.join(assets_dir, "logo.png")

        # Campos
        self.username = ft.TextField(
            label="Usuario", border_radius=10, width=300, bgcolor="white", border_color=self.COLOR_PRIMARIO,
            focused_border_color=self.COLOR_PRIMARIO, label_style=ft.TextStyle(color=self.COLOR_TEXTO, font_family="Roboto"),
            text_style=ft.TextStyle(font_family="Roboto")
        )
        self.password = ft.TextField(
            label="Contraseña", password=True, can_reveal_password=True, border_radius=10, width=300, bgcolor="white",
            border_color=self.COLOR_PRIMARIO, focused_border_color=self.COLOR_PRIMARIO, label_style=ft.TextStyle(color=self.COLOR_TEXTO, font_family="Roboto"),
            text_style=ft.TextStyle(font_family="Roboto")
        )
        self.login_status = ft.Text(size=14, weight=ft.FontWeight.BOLD, font_family="Roboto")

        # Botón
        self.login_btn = ft.ElevatedButton(
            text="Iniciar Sesión", height=50, width=300, bgcolor=self.COLOR_PRIMARIO, color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
            on_click=self.do_login
        )

    def do_login(self, e):
        if self.api.login(self.username.value, self.password.value):
            self.login_status.value = "¡Login exitoso!"
            self.login_status.color = self.COLOR_EXITO
            self.page.update()
            self.on_login_success()
        else:
            self.login_status.value = "Credenciales inválidas"
            self.login_status.color = self.COLOR_ERROR
        self.page.update()

    def show(self):
        self.page.clean()

        # Fondo
        background = ft.Container(expand=True, content=ft.Image(src=self.bg_path, fit=ft.ImageFit.COVER, opacity=0.8))

        # Logo
        logo = ft.Image(src=self.logo_path, width=150, height=150, fit=ft.ImageFit.CONTAIN)

        # Formulario
        form = ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    logo,
                    ft.Text("Acceso Médico", size=24, weight=ft.FontWeight.BOLD, color=self.COLOR_PRIMARIO, font_family="Roboto", text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color="transparent"),
                    self.username,
                    self.password,
                    self.login_btn,
                    self.login_status
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="white",
                border_radius=15
            ),
            elevation=10,
            margin=20,
            width=400
        )

        self.page.add(
            ft.Stack([
                background,
                ft.Container(content=form, alignment=ft.alignment.center)
            ], expand=True)
        )
        self.page.update()