import flet as ft

class MainView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"

    def show(self):
        self.page.clean()

        profile = self.api.get_profile()
        datos = profile.get("datos_especificos", {})

        card = ft.Card(
            content=ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text(f"Dr. {profile.get('nombre', 'N/A')} {profile.get('apellido', 'N/A')}", 
                            size=24, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Text(f"Especialidad: {datos.get('especialidad', 'N/A')}", size=18, color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Text(f"Edad: {profile.get('edad', 'N/A')} años", size=16, color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Text(f"Ubicación: {profile.get('ubicacion', 'N/A')}", size=16, color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([
                        ft.ElevatedButton(
                            "Citas", icon=ft.Icons.CALENDAR_TODAY, width=150, bgcolor=self.COLOR_PRIMARIO, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=lambda e: self.on_navigate("citas")
                        ),
                        ft.ElevatedButton(
                            "Historial", icon=ft.Icons.HISTORY, width=150, bgcolor=self.COLOR_PRIMARIO, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=lambda e: self.on_navigate("historial")
                        ),
                        ft.ElevatedButton(
                            "Salir", icon=ft.Icons.LOGOUT, width=150, bgcolor="#DC3545", color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=lambda e: self.page.window.destroy()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="white",
                border_radius=15
            ),
            elevation=10,
            margin=20,
            width=600
        )

        self.page.add(
            ft.Container(content=card, alignment=ft.alignment.center, padding=20)
        )
        self.page.update()