# views/atencion_view.py
import flet as ft

class AtencionView:
    def __init__(self, page: ft.Page, api_client, on_navigate, cita_id: int, paciente_id: int):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.cita_id = cita_id
        self.paciente_id = paciente_id
        self.sistema = ft.TextField(label="Sistema", multiline=True, min_lines=3)
        self.diagnostico = ft.TextField(label="Diagnóstico", multiline=True, min_lines=5)
        self.recomendaciones = ft.TextField(label="Recomendaciones", multiline=True, min_lines=5)
        self.uploaded_images = []
        self.file_picker = ft.FilePicker(on_result=self.on_files_selected)
        page.overlay.append(self.file_picker)

    def on_files_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.uploaded_images = e.files
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"{len(e.files)} imágenes cargadas")))

    def guardar_atencion(self, e):
        if not all([self.sistema.value, self.diagnostico.value, self.recomendaciones.value]):
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Complete todos los campos")))
            return

        response = self.api.registrar_atencion(
            paciente_id=self.paciente_id,
            sintomas=self.sistema.value,
            diagnostico=self.diagnostico.value,
            recomendaciones=self.recomendaciones.value,
            imagenes=self.uploaded_images
        )

        if "error" not in response:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Atención guardada")))
            self.on_navigate("citas")
        else:
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {response['error']}")))

    def show(self):
        self.page.clean()
        self.page.add(ft.Text(f"Atendiendo Cita ID: {self.cita_id}", size=18))
        self.page.add(
            self.sistema, self.diagnostico, self.recomendaciones,
            ft.ElevatedButton("Cargar Imágenes", icon=ft.icons.UPLOAD, 
                on_click=lambda e: self.file_picker.pick_files(allow_multiple=True)),
            ft.ElevatedButton("Guardar Atención", on_click=self.guardar_atencion),
            ft.ElevatedButton("Volver", on_click=lambda e: self.on_navigate("citas"))
        )