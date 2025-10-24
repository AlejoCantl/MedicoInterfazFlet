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
        self.login_status.value = ""  # Limpiar estado al mostrar

        # Configurar la página para que ocupe toda la pantalla
        self.page.padding = 0
        self.page.spacing = 0

        # Fondo que cubre toda la pantalla
        background_container = ft.Container(
            expand=True,
            content=ft.Image(
                src=self.bg_path, 
                fit=ft.ImageFit.COVER,
                width=self.page.width,  # Ancho de la página
                height=self.page.height,  # Alto de la página
                opacity=0.8,
            ),
            margin=0,
            padding=0,
        )

        # Formulario centrado
        login_form = ft.Card(
            content=ft.Container(
                padding=25,
                width=340,
                content=ft.Column(
                    [
                        ft.Image(src=self.logo_path, width=100, height=100, fit=ft.ImageFit.CONTAIN), 
                        ft.Text(
                            "Acceso Médico", 
                            size=22, 
                            weight=ft.FontWeight.W_900, 
                            color=self.COLOR_PRIMARIO, 
                            font_family="Roboto", 
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=5, color="transparent"),
                        self.username,
                        self.password,
                        ft.Container(height=8),  # Espaciado
                        self.login_btn,
                        self.login_status
                    ], 
                    spacing=10, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
                border_radius=15,
                blur=ft.Blur(10, 10, ft.BlurTileMode.MIRROR)
            ),
            elevation=8,
            color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
        )

        # Contenedor que centra el formulario
        centered_content = ft.Container(
            content=ft.Container(
                    content=login_form,
                    width=420,  # Dimensiones aquí en el contenedor interno
                    height=420,
                     ),
            alignment=ft.alignment.center,
            expand=True  # El contenedor padre se expande para centrar el contenido interno
            )

        # Stack principal
        main_stack = ft.Stack(
            [
                background_container,
                centered_content
            ], 
            expand=True
        )

        # Contenedor final
        self.page.add(
            ft.Container(
                content=main_stack,
                expand=True,
                padding=0,
                margin=0,
                bgcolor=ft.Colors.BLACK
            )
        )
        self.page.update()