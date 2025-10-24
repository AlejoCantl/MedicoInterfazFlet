import flet as ft
import os

class AtencionView:
    def __init__(self, page: ft.Page, api_client, on_navigate, cita_id: int, paciente_id: int):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.cita_id = cita_id
        self.paciente_id = paciente_id
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"
        self.COLOR_ERROR = "#DC3545"

        # Campos
        self.sistema = ft.TextField(
            label="Sistema afectado", multiline=True, min_lines=3, width=600, bgcolor="white",
            border_color=self.COLOR_PRIMARIO, font_family="Roboto"
        )
        self.diagnostico = ft.TextField(
            label="Diagnóstico", multiline=True, min_lines=5, width=600, bgcolor="white",
            border_color=self.COLOR_PRIMARIO, font_family="Roboto"
        )
        self.recomendaciones = ft.TextField(
            label="Recomendaciones", multiline=True, min_lines=5, width=600, bgcolor="white",
            border_color=self.COLOR_PRIMARIO, font_family="Roboto"
        )
        self.uploaded_images = []
        self.yolo_results = ft.Column(scroll=ft.ScrollMode.AUTO)
        self.file_picker = ft.FilePicker(on_result=self.on_files_selected)
        page.overlay.append(self.file_picker)

        # Datos del paciente (de API)
        self.paciente_info = self.api.get_paciente_info(self.paciente_id)  # Asume endpoint agregado

    def on_files_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.uploaded_images = e.files
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"{len(e.files)} imágenes cargadas"), bgcolor=self.COLOR_EXITO))

    def guardar_atencion(self, e):
        if not all([self.sistema.value, self.diagnostico.value, self.recomendaciones.value]):
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Complete todos los campos"), bgcolor=self.COLOR_ERROR))
            return

        response = self.api.registrar_atencion(
            paciente_id=self.paciente_id,
            sintomas=self.sistema.value,
            diagnostico=self.diagnostico.value,
            recomendaciones=self.recomendaciones.value,
            imagenes=self.uploaded_images
        )

        if "error" not in response:
            self.yolo_results.controls.clear()
            for res in response.get("yolo_resultados", []):
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Imagen: {os.path.basename(res['ruta'])}", weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                            ft.Text(f"Detecciones: {len(res['resultado']['detections'])}", color=self.COLOR_TEXTO, font_family="Roboto"),
                            ft.Column([
                                ft.Text(f"• {d['class']} ({d['confidence']:.2f})", color=self.COLOR_TEXTO, font_family="Roboto")
                                for d in res['resultado']['detections']
                            ])
                        ], spacing=5),
                        padding=10,
                        bgcolor="white"
                    ),
                    elevation=3,
                    margin=5
                )
                self.yolo_results.controls.append(card)
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Atención guardada con éxito"), bgcolor=self.COLOR_EXITO))
            self.page.update()
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {response['error']}"), bgcolor=self.COLOR_ERROR))

    def show(self):
        self.page.clean()

        # Tarjeta de paciente
        paciente_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Paciente: {self.paciente_info.get('paciente', 'N/A')}", size=18, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Text(f"Tipo: {self.paciente_info.get('tipo_paciente', 'N/A')} | Peso: {self.paciente_info.get('peso', 'N/A')} | Talla: {self.paciente_info.get('talla', 'N/A')}", color=self.COLOR_TEXTO, font_family="Roboto"),
                    ft.Text(f"Enfermedades: {self.paciente_info.get('enfermedades', 'N/A')}", color=self.COLOR_TEXTO, font_family="Roboto"),
                ], spacing=5),
                padding=15,
                bgcolor="white"
            ),
            elevation=5,
            margin=20
        )

        self.page.add(
            ft.Text("Atención al Paciente", size=24, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto", text_align=ft.TextAlign.CENTER),
            paciente_card,
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        self.sistema,
                        self.diagnostico,
                        self.recomendaciones,
                        ft.Row([
                            ft.ElevatedButton(
                                "Cargar Imágenes", icon=ft.icons.UPLOAD, width=200, bgcolor=self.COLOR_PRIMARIO, color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=lambda e: self.file_picker.pick_files(allow_multiple=True)
                            ),
                            ft.ElevatedButton(
                                "Guardar Atención", icon=ft.icons.SAVE, width=200, bgcolor=self.COLOR_EXITO, color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=self.guardar_atencion
                            ),
                            ft.ElevatedButton(
                                "Volver", icon=ft.icons.ARROW_BACK, width=200, bgcolor=self.COLOR_ERROR, color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=lambda e: self.on_navigate("citas")
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                    ], spacing=15),
                    padding=20,
                    bgcolor="white"
                ),
                elevation=5,
                margin=20
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Resultados YOLO", size=18, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                        self.yolo_results
                    ], spacing=10),
                    padding=20,
                    bgcolor="white"
                ),
                elevation=5,
                margin=20
            )
        )
        self.page.update()