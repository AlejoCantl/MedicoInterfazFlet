# api_client.py
import requests
from typing import List, Dict
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.rol_id = None

    def _decode_token(self, token: str) -> Dict:
        """
        Decodifica el JWT sin verificar la firma (solo lectura)
        Retorna el payload del token
        """
        try:
            # Decodificar sin verificar la firma (options={"verify_signature": False})
            payload = jwt.decode(token, options={"verify_signature": False})
            print(f"[DEBUG DECODE] Payload decodificado: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            print("[DEBUG DECODE] Token expirado")
            return {"error": "Token expirado"}
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG DECODE] Token inválido: {e}")
            return {"error": "Token inválido"}
        except Exception as e:
            print(f"[DEBUG DECODE] Error decodificando token: {e}")
            return {"error": f"Error al decodificar: {str(e)}"}

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

    def login(self, username: str, password: str) -> Dict:
        """
        Realiza el login y valida que el usuario sea médico (rol_id = 2)
        decodificando el JWT directamente
        Retorna un diccionario con 'success' (bool) y 'message' (str)
        """
        try:
            response = self.session.post(f"{API_URL}/Usuario/login", json={
                "nombre_usuario": username,
                "contrasena": password
            })
            
            if response.status_code == 200:
                data = response.json()
                token = data["access_token"]
                
                # 🔍 DECODIFICAR EL TOKEN
                payload = self._decode_token(token)
                
                if "error" in payload:
                    return {
                        "success": False,
                        "message": f"Error en el token: {payload['error']}"
                    }
                
                # 📋 EXTRAER DATOS DEL TOKEN
                self.user_id = payload.get("sub")  # El 'sub' contiene el user_id
                self.rol_id = payload.get("rol_id")
                token_exp = payload.get("exp")
                
                print(f"[DEBUG] user_id: {self.user_id}, rol_id: {self.rol_id}, exp: {token_exp}")
                
                # ✅ VALIDACIÓN DE ROL MÉDICO
                if self.rol_id != 2:
                    self._clear_session()
                    return {
                        "success": False,
                        "message": "Acceso denegado. Rol inválido."
                    }
                
                # ✅ TODO OK: Guardar token y configurar sesión
                self.token = token
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                
                return {
                    "success": True,
                    "message": "Login exitoso"
                }
            
            return {
                "success": False,
                "message": "Credenciales inválidas"
            }
            
        except Exception as e:
            print(f"[API] Error login: {e}")
            self._clear_session()
            return {
                "success": False,
                "message": f"Error de conexión: {str(e)}"
            }

    def _clear_session(self):
        """Limpia la sesión actual"""
        self.token = None
        self.user_id = None
        self.rol_id = None
        self.session.headers.pop("Authorization", None)

    def get_profile(self) -> Dict:
        response = self.session.get(f"{API_URL}/Usuario/perfil")
        return self._handle_response(response)

    def get_citas_aprobadas(self) -> List[Dict]:
        response = self.session.get(f"{API_URL}/Medico/citas/aprobadas")
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
        
        files_for_request = []
        files_to_close = [] 
        
        try:
            for img in imagenes:
                file_obj = open(img.path, 'rb')
                files_to_close.append(file_obj)
                files_for_request.append(('imagenes', (img.name, file_obj, 'image/jpeg')))
            
            response = self.session.post(
                f"{API_URL}/Medico/atencion",
                data=data,
                files=files_for_request
            )
            return self._handle_response(response)
        
        except Exception as e:
            return {"error": f"Error al subir imágenes o realizar la solicitud: {e}"}
        
        finally:
            for file_obj in files_to_close: 
                try:
                    file_obj.close()
                except Exception as e:
                    print(f"Error cerrando archivo: {e}") 
                    pass

    def is_logged_in(self) -> bool:
        return self.token is not None and self.user_id is not None and self.rol_id == 2