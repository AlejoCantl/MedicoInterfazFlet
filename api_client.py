# api_client.py
import requests
from typing import List, Dict, Optional
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

    def _handle_response(self, response: requests.Response) -> Dict:
        """Manejo centralizado de respuestas"""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            self.token = None
            self.session.headers.pop("Authorization", None)
            return {"error": "Sesión expirada. Inicie sesión nuevamente."}
        elif response.status_code == 403:
            return {"error": "Acceso denegado."}
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}

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
        return self._handle_response(response)

    def get_citas_aprobadas(self) -> List[Dict]:
        """Obtiene citas aprobadas del médico"""
        response = self.session.get(f"{API_URL}/Medico/citas/aprobadas")
        data = self._handle_response(response)
        return data.get("citas", []) if "error" not in data else []

    def get_historial_medico(self, nombre: str = None, identificacion: str = None) -> List[Dict]:
        params = {}
        if nombre:
            params["nombre"] = nombre
        if identificacion:
            params["identificacion"] = identificacion
        response = self.session.get(f"{API_URL}/Medico/historial", params=params)
        data = self._handle_response(response)
        return data.get("historial", []) if "error" not in data else []

    def get_paciente_info(self, paciente_id: int) -> Dict:
        """Obtiene datos del paciente para mostrar en atención"""
        response = self.session.get(f"{API_URL}/Medico/paciente/{paciente_id}")
        data = self._handle_response(response)
        return data if "error" not in data else {}

    def registrar_atencion(
        self,
        paciente_id: int,
        sintomas: str,
        diagnostico: str,
        recomendaciones: str,
        imagenes: List = []
    ) -> Dict:
        """
        Registra atención con imágenes.
        Usa multipart/form-data correctamente.
        """
        data = {
            "sintomas": sintomas,
            "diagnostico": diagnostico,
            "recomendaciones": recomendaciones
        }
        files = []
        try:
            for img in imagenes:
                # Abrir archivo en modo binario
                file_obj = open(img.path, 'rb')
                files.append(('imagenes', (img.name, file_obj, 'image/jpeg')))
            
            response = self.session.post(
                f"{API_URL}/Medico/atencion",
                data=data,
                files=files
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Error al subir imágenes: {e}"}
        finally:
            # CERRAR TODOS LOS ARCHIVOS
            for _, file_obj, _ in files:
                try:
                    file_obj.close()
                except:
                    pass

    def is_logged_in(self) -> bool:
        return self.token is not None and self.user_id is not None