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

    def _handle_response(self, response: requests.Response) -> Dict:
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
        response = self.session.get(f"{API_URL}/Medico/citas/aprobadas")
        # Nota: La línea de impresión original era confusa, pero la lógica de manejo de datos es correcta.
        data = self._handle_response(response)
        return data.get("citas_aprobadas", []) if "error" not in data else []

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
        response = self.session.get(f"{API_URL}/Medico/paciente/{paciente_id}")
        data = self._handle_response(response)
        return data if "error" not in data else {}

    def registrar_atencion(
        self,
        cita_id: int,
        sistema: str,
        diagnostico: str,
        recomendaciones: str,
        imagenes: List = []
        ) -> Dict:
        data = {
            "cita_id": cita_id,
            "sistema": sistema,
            "diagnostico": diagnostico,
            "recomendaciones": recomendaciones
        }
        
        # 1. Creamos dos listas: una para los archivos de la solicitud y otra para los objetos que deben cerrarse.
        files_for_request = []
        files_to_close = [] 
        
        try:
            for img in imagenes:
                file_obj = open(img.path, 'rb')
                files_to_close.append(file_obj) # Guardamos el objeto file para el cierre
                
                # Formato de la tupla para la solicitud POST de requests: ('nombre_campo', (nombre_archivo, objeto_archivo, tipo_mime))
                files_for_request.append(('imagenes', (img.name, file_obj, 'image/jpeg')))
            
            response = self.session.post(
                f"{API_URL}/Medico/atencion",
                data=data,
                files=files_for_request # Usamos la lista de la solicitud
            )
            return self._handle_response(response)
        
        except Exception as e:
            return {"error": f"Error al subir imágenes o realizar la solicitud: {e}"}
        
        finally:
            # 2. Recorremos SOLAMENTE los objetos de archivo que necesitamos cerrar.
            for file_obj in files_to_close: 
                try:
                    file_obj.close()
                except Exception as e:
                    print(f"Error cerrando archivo: {e}") 
                    pass

    def is_logged_in(self) -> bool:
        return self.token is not None and self.user_id is not None and self.rol_id is not None