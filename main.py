import flet as ft
from api_client import APIClient
from views import LoginView, MainView, CitasView, AtencionView, HistorialView

def main(page: ft.Page):
    page.title = "Médico - Fundación Amigos de los Niños"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F8FAFC"  # Fondo suave
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"}

    api = APIClient()

    def navigate(to, **kwargs):
        if to == "login":
            LoginView(page, api, lambda: navigate("main")).show()
        elif to == "main":
            MainView(page, api, navigate).show()
        elif to == "citas":
            CitasView(page, api, navigate).show()
        elif to == "atencion":
            AtencionView(page, api, navigate, kwargs["cita_id"], kwargs["paciente_id"]).show()
        elif to == "historial":
            HistorialView(page, api, navigate).show()

    # Iniciar en login
    navigate("login")

ft.app(target=main)