import flet as ft

class MainView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        
        # --- Constantes de Estilo (consistentes con otras vistas) ---
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_FONDO_CLARO = "#F8F9FA"
        self.COLOR_SALIR = "#DC3545"

    def show(self):
        self.page.clean()

        profile = self.api.get_profile()
        datos = profile.get("datos_especificos", {})

        # 🎯 Header con ícono de médico y nombre
        header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.ACCOUNT_CIRCLE, 
                    size=70, 
                    color=self.COLOR_PRIMARIO
                ),
                ft.Column([
                    ft.Text(
                        f"Dr. {profile.get('nombre', 'N/A')} {profile.get('apellido', 'N/A')}", 
                        size=28, 
                        weight=ft.FontWeight.W_900, 
                        color=self.COLOR_TEXTO, 
                        font_family="Roboto"
                    ),
                    ft.Text(
                        datos.get('especialidad', 'N/A'), 
                        size=18, 
                        weight=ft.FontWeight.W_500,
                        color=self.COLOR_PRIMARIO, 
                        font_family="Roboto",
                        italic=True
                    ),
                ], 
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
        )

        # 🎯 Sección de información personal con íconos
        info_personal = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Información Personal", 
                    size=18, 
                    weight=ft.FontWeight.BOLD, 
                    color=self.COLOR_TEXTO,
                    font_family="Roboto"
                ),
                ft.Divider(height=10, color=ft.Colors.GREY_300),
                
                # Edad
                ft.Row([
                    ft.Icon(ft.Icons.CAKE, size=24, color=self.COLOR_PRIMARIO),
                    ft.Text(
                        "Edad:", 
                        size=16, 
                        weight=ft.FontWeight.W_600,
                        color=self.COLOR_TEXTO,
                        font_family="Roboto"
                    ),
                    ft.Text(
                        f"{profile.get('edad', 'N/A')} años", 
                        size=16, 
                        color=self.COLOR_TEXTO,
                        font_family="Roboto"
                    ),
                ], spacing=10),
                
                # Ubicación
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, size=24, color=self.COLOR_PRIMARIO),
                    ft.Text(
                        "Ubicación:", 
                        size=16, 
                        weight=ft.FontWeight.W_600,
                        color=self.COLOR_TEXTO,
                        font_family="Roboto"
                    ),
                    ft.Text(
                        profile.get('ubicacion', 'N/A'), 
                        size=16, 
                        color=self.COLOR_TEXTO,
                        font_family="Roboto"
                    ),
                ], spacing=10),
                
            ], 
            spacing=15),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            margin=ft.margin.only(top=15),
        )

        # 🎯 Botones de acción con mejor diseño
        botones = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Acciones Rápidas", 
                    size=18, 
                    weight=ft.FontWeight.BOLD, 
                    color=self.COLOR_TEXTO,
                    font_family="Roboto",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=10, color=ft.Colors.GREY_300),
                
                ft.Row([
                    ft.ElevatedButton(
                        "Citas", 
                        icon=ft.Icons.CALENDAR_TODAY, 
                        width=180, 
                        height=50,
                        bgcolor=self.COLOR_PRIMARIO, 
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=lambda e: self.on_navigate("citas")
                    ),
                    ft.ElevatedButton(
                        "Historial", 
                        icon=ft.Icons.HISTORY, 
                        width=180,
                        height=50, 
                        bgcolor=self.COLOR_PRIMARIO, 
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=lambda e: self.on_navigate("historial")
                    ),
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                spacing=20),
                
                ft.Row([
                    ft.ElevatedButton(
                        "Cerrar Sesión", 
                        icon=ft.Icons.LOGOUT, 
                        width=180,
                        height=50, 
                        bgcolor=self.COLOR_SALIR, 
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=lambda e: self.page.window.destroy()
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER),
                
            ], 
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15,
            margin=ft.margin.only(top=15),
        )

        # 🎯 Card principal que contiene todo
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    header,
                    info_personal,
                    botones,
                ], 
                spacing=0),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=15
            ),
            elevation=10,
            margin=20,
            width=650
        )

        # Contenedor principal
        self.page.add(
            ft.Container(
                content=card, 
                alignment=ft.alignment.center, 
                padding=20,
                bgcolor=self.COLOR_FONDO_CLARO,
                expand=True
            )
        )
        self.page.update()