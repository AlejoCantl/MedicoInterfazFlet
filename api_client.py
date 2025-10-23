# api_client.py
import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.rol_id = None

    def login(self, username: str, password: str) -> bool:
        try:
            response = self.session.post(f"{API_URL}/Usuario/login", json={
                "nombre_usuario": username,
                "contrasena": password
            })
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                profile = self.get_profile()
                self.user_id = profile.get("user_id")
                self.rol_id = profile.get("rol_id")
                return True
            return False
        except Exception as e:
            print(f"[API] Error login: {e}")
            return False

    def get_profile(self) -> Dict:
        response = self.session.get(f"{API_URL}/Usuario/perfil")
        return response.json() if response.status_code == 200 else {}

    def get_citas_aprobadas(self) -> List[Dict]:
        response = self.session.get(f"{API_URL}/Paciente/citas")
        return response.json().get("citas", []) if response.status_code == 200 else []

    def get_historial_medico(self, nombre: str = None, identificacion: str = None) -> List[Dict]:
        params = {}
        if nombre:
            params["nombre"] = nombre
        if identificacion:
            params["identificacion"] = identificacion
        response = self.session.get(f"{API_URL}/Medico/historial", params=params)
        return response.json().get("historial", []) if response.status_code == 200 else []

    def registrar_atencion(self, paciente_id: int, sintomas: str, diagnostico: str, recomendaciones: str, imagenes=[]) -> Dict:
        files = []
        data = {
            "sintomas": sintomas,
            "diagnostico": diagnostico,
            "recomendaciones": recomendaciones
        }
        for img in imagenes:
            files.append(('imagenes', (img.name, open(img.path, 'rb'), 'image/jpeg')))
        response = self.session.post(
            f"{API_URL}/Medico/atencion?paciente_id={paciente_id}",
            data=data,
            files=files
        )
        return response.json() if response.status_code == 200 else {"error": response.text}