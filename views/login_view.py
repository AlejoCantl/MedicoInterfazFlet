import flet as ft
import os

class LoginView:
    def __init__(self, page: ft.Page, api_client, on_login_success):
        self.page = page
        self.api = api_client
        self.on_login_success = on_login_success

        # === Rutas absolutas ===
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "..", "assets", "images")
        self.bg_path = os.path.join(assets_dir, "fondo.jpeg")   # ← Tu fondo
        self.logo_path = os.path.join(assets_dir, "logo.png")   # ← Tu logo

        # === Campos ===
        self.username = ft.TextField(
            label="Usuario",
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.92, ft.Colors.WHITE),
            focused_border_color="#FFB800",
            label_style=ft.TextStyle(color="#333333"),
        )
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.92, ft.Colors.WHITE),
            focused_border_color="#FFB800",
            label_style=ft.TextStyle(color="#333333"),
        )
        self.login_status = ft.Text(size=14, weight=ft.FontWeight.BOLD)

        # === Botón ===
        self.login_btn = ft.ElevatedButton(
            text="Iniciar Sesión",
            height=50,
            bgcolor="#FDAA56",
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=self.do_login
        )

    def do_login(self, e):
        if self.api.login(self.username.value, self.password.value):
            self.login_status.value = "Login exitoso"
            self.login_status.color = "#4ECDC4"
            self.page.update()
            self.on_login_success()
        else:
            self.login_status.value = "Credenciales inválidas"
            self.login_status.color = "#FF6B6B"
        self.page.update()

    def show(self):
        self.page.clean()

        # === Fondo que cubre TODA la pantalla ===
        background = ft.Container(
            expand=True,
            padding=0,
            margin=0,
            content=ft.Image(
                src=self.bg_path,
                fit=ft.ImageFit.COVER,
                expand=True,
                opacity=0.9
            )
        )

        # === Logo ===
        logo = ft.Image(
            src=self.logo_path,
            width=220,
            height=220,
            fit=ft.ImageFit.CONTAIN
        )

        # === Formulario responsive ===
        form_width = self.page.window.width * 0.35 if self.page.window.width else 380
        form_width = max(300, min(form_width, 400))  # entre 300 y 400

        login_form = ft.Container(
            width=form_width,
            height=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=32, vertical=28),
            bgcolor=ft.Colors.with_opacity(0.92, ft.Colors.WHITE),
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=8,
                blur_radius=25,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                offset=ft.Offset(0, 12)
            ),
            content=ft.Column([
                # Logo con tamaño dinámico
                ft.Container(
                    content=logo,
                    width=min(260, form_width * 0.7),
                    height=min(260, form_width * 0.7),
                    alignment=ft.alignment.center
                ),
                ft.Text(
                    "Acceso Médico",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#FFB800",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.username,
                self.password,
                self.login_btn,
                self.login_status
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16)
        )

        # === Stack responsive ===
        main_stack = ft.Stack([
            background,
            ft.Container(
                content=login_form,
                alignment=ft.alignment.center
            )
        ], expand=True)

        # === Contenedor raíz responsive ===
        self.page.add(
            ft.Container(
                content=main_stack,
                expand=True,
                padding=0,
                margin=0
            )
        )
        self.page.update()