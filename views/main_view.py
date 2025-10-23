import flet as ft

class MainView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate  # Función para navegar

    def show(self):
        self.page.clean()
        profile = self.api.get_profile()
        datos = profile.get("datos_especificos", {})

        info = ft.Column([
            ft.Text(f"Dr. {profile.get('nombre', 'N/A')} {profile.get('apellido', 'N/A')}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Especialidad: {datos.get('especialidad', 'N/A')}"),
            ft.Text(f"Edad: {profile.get('edad', 'N/A')} años"),
            # ft.Text(f"Ubicación: {profile.get('ubicacion', 'N/A')}"),
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton("Módulo Citas", on_click=lambda e: self.on_navigate("citas")),
                ft.ElevatedButton("Historial", on_click=lambda e: self.on_navigate("historial")),
                ft.ElevatedButton("Salir", on_click=lambda e: self.page.window_destroy())
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], spacing=15)

        self.page.add(info)