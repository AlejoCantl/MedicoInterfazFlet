import flet as ft
import os

class AtencionView:
    def __init__(self, page: ft.Page, api_client, on_navigate, cita_id: int, paciente_id: int):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.cita_id = cita_id
        self.paciente_id = paciente_id
        
        # Colores consistentes
        self.COLOR_PRIMARIO = "#007BFF"  # Azul (Botones principales)
        self.COLOR_TEXTO = "#343A40"     # Gris oscuro (Texto principal)
        self.COLOR_EXITO = "#28A745"     # Verde (Guardar)
        self.COLOR_ERROR = "#DC3545"     # Rojo (Volver/Error)
        self.COLOR_FONDO_CARD = "#F8F9FA" # Gris claro para fondo de tarjetas

        # Estilo de texto centralizado para los TextField
        text_style = ft.TextStyle(font_family="Roboto", color=self.COLOR_TEXTO)
        
        # Estilo para las etiquetas de los TextField
        label_style = ft.TextStyle(font_family="Roboto", color=self.COLOR_PRIMARIO, weight=ft.FontWeight.BOLD)

        # 🛑 CORRECCIÓN DE FONT Y MEJORAS DE UX en TextField
        self.sistema = ft.TextField(
            label="Sistema afectado (Motivo de Consulta)", 
            multiline=True, 
            min_lines=3, 
            max_lines=5, 
            bgcolor=ft.Colors.WHITE,
            border_color=self.COLOR_PRIMARIO,
            border_radius=10,
            text_style=text_style,
            label_style=label_style,
            hint_text="Describe los síntomas y sistemas involucrados."
        )
        self.diagnostico = ft.TextField(
            label="Diagnóstico (CIE-10)", 
            multiline=True, 
            min_lines=3, 
            max_lines=7, 
            bgcolor=ft.Colors.WHITE,
            border_color=self.COLOR_PRIMARIO,
            border_radius=10,
            text_style=text_style,
            label_style=label_style,
            hint_text="Escribe el diagnóstico médico."
        )
        self.recomendaciones = ft.TextField(
            label="Recomendaciones y Tratamiento", 
            multiline=True, 
            min_lines=3, 
            max_lines=7, 
            bgcolor=ft.Colors.WHITE,
            border_color=self.COLOR_PRIMARIO,
            border_radius=10,
            text_style=text_style,
            label_style=label_style,
            hint_text="Detalla el plan de manejo y seguimiento."
        )
        self.uploaded_images = []
        self.yolo_results = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True) # expand para usar el espacio
        self.file_picker = ft.FilePicker(on_result=self.on_files_selected)
        page.overlay.append(self.file_picker)

        self.paciente_info = self.api.get_paciente_info(self.paciente_id)
        
        # CONTROLES DE IMAGEN (para mostrar cuántas hay)
        self.image_count_text = ft.Text("0 imágenes adjuntas", color=self.COLOR_TEXTO)

        # 🛑 CORRECCIÓN 1: Inicializar page.snack_bar en el constructor
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mensaje temporal"),
            duration=4000
        )

    def _show_snack_bar(self, message: str, color: str):
        """Método auxiliar para mostrar el SnackBar de la forma correcta."""
        self.page.snack_bar.content = ft.Text(message, font_family="Roboto")
        self.page.snack_bar.bgcolor = color
        self.page.snack_bar.open = True
        self.page.update()

    def on_files_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.uploaded_images = e.files
            self.image_count_text.value = f"{len(e.files)} imágenes adjuntas"
            # 🛑 CORRECCIÓN 2: Usar el método auxiliar
            self._show_snack_bar(
                f"{len(e.files)} imágenes cargadas exitosamente.", 
                self.COLOR_EXITO
            )
        else:
            self.image_count_text.value = "0 imágenes adjuntas"
            # 🛑 CORRECCIÓN 3: Usar el método auxiliar
            self._show_snack_bar(
                "Carga de imágenes cancelada.", 
                self.COLOR_ERROR
            )
        self.page.update()

    # atencion_view.py (Método guardar_atencion)

    def guardar_atencion(self, e):
        if not all([self.sistema.value, self.diagnostico.value, self.recomendaciones.value]):
            self._show_snack_bar("🔴 Complete todos los campos obligatorios.", self.COLOR_ERROR)
            return

        e.control.disabled = True
        self.page.update()

        response = self.api.registrar_atencion(
            cita_id=self.cita_id,
            sistema=self.sistema.value,
            diagnostico=self.diagnostico.value,
            recomendaciones=self.recomendaciones.value,
            imagenes=self.uploaded_images
        )
        
        e.control.disabled = False

        if "error" not in response:
            self.yolo_results.controls.clear()
            
            yolo_header = ft.Text("✅ Resultados de Detección (YOLO)", size=18, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto")
            self.yolo_results.controls.append(yolo_header)
            self.yolo_results.controls.append(ft.Divider())

            
            # 🛑 CORRECCIÓN CLAVE: El bucle principal ahora itera sobre listas de detecciones por imagen.
            # 'detecciones_por_imagen' es ahora una lista, no un diccionario.
            # Ya no podemos acceder a 'res.get("ruta", "N/A")', porque 'res' es una lista. 
            # Usaremos el índice (idx) para simular el nombre de la imagen.

            resultados_yolo = response.get("detections", [])
            
            for idx, detecciones_por_imagen in enumerate(resultados_yolo):
                
                # La lista de detecciones individuales (d) es el elemento actual.
                detections_list = ft.Column([
                    ft.Text(
                        f"• {d.get('class', 'N/A')} ({d.get('confidence', 0.0):.2f})", 
                        color=self.COLOR_TEXTO, 
                        font_family="Roboto", 
                        size=13
                    )
                    # 🛑 CORRECCIÓN: Iteramos directamente sobre la lista 'detecciones_por_imagen'
                    for d in detecciones_por_imagen
                ], spacing=3)
                
                # 🛑 AJUSTE VISUAL: Ya que 'ruta' no está, usamos el índice y el nombre original del archivo.
                imagen_name = self.uploaded_images[idx].name if idx < len(self.uploaded_images) else f"Imagen {idx + 1}"
                
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"🔬 Imagen: {os.path.basename(imagen_name)}", weight=ft.FontWeight.BOLD, color=self.COLOR_PRIMARIO, font_family="Roboto"),
                            ft.Text(f"Detecciones totales: {len(detecciones_por_imagen)}", color=self.COLOR_TEXTO, font_family="Roboto", size=14),
                            detections_list
                        ], spacing=8),
                        padding=15,
                        bgcolor=ft.Colors.WHITE
                    ),
                    elevation=3,
                    margin=5
                )
                self.yolo_results.controls.append(card)

            self._show_snack_bar("👍 Atención guardada con éxito. Resultados YOLO actualizados.", self.COLOR_EXITO)
        else:
            self._show_snack_bar(f"❌ Error al guardar: {response.get('error', 'Error desconocido')}", self.COLOR_ERROR)

        self.page.update()

    def show(self):
        self.page.clean()
        
        # 1. TARJETA DE INFORMACIÓN DEL PACIENTE (Más detallada y visual)
        paciente_card_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("👤 Información del Paciente", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_PRIMARIO, font_family="Roboto"),
                    ft.Divider(color=self.COLOR_PRIMARIO),
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_OUTLINE, color=self.COLOR_TEXTO),
                        ft.Text(f"Paciente: {self.paciente_info.get('paciente', 'N/A')}", size=16, color=self.COLOR_TEXTO, font_family="Roboto", weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Row([
                        ft.Icon(ft.Icons.MAIL_OUTLINE, color=self.COLOR_TEXTO, size=18),
                        ft.Text(f"Correo: {self.paciente_info.get('correo', 'N/A')}", color=self.COLOR_TEXTO, font_family="Roboto"),
                        ft.VerticalDivider(),
                        ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, color=self.COLOR_TEXTO, size=18),
                        ft.Text(f"Edad: {self.paciente_info.get('edad', 'N/A')} años", color=self.COLOR_TEXTO, font_family="Roboto"),
                    ], spacing=15),
                    ft.Row([
                        ft.Icon(ft.Icons.BALANCE_OUTLINED, color=self.COLOR_TEXTO, size=18),
                        ft.Text(f"Peso/Talla: {self.paciente_info.get('peso', 'N/A')} / {self.paciente_info.get('talla', 'N/A')}", color=self.COLOR_TEXTO, font_family="Roboto"),
                        ft.VerticalDivider(),
                        ft.Icon(ft.Icons.LOCAL_HOSPITAL_OUTLINED, color=self.COLOR_TEXTO, size=18),
                        ft.Text(f"Tipo: {self.paciente_info.get('tipo_paciente', 'N/A')}", color=self.COLOR_TEXTO, font_family="Roboto"),
                    ], spacing=15),
                    ft.Row([
                         ft.Icon(ft.Icons.MEDICAL_INFORMATION_OUTLINED, color=self.COLOR_ERROR, size=18),
                         ft.Text(f"Enfermedades crónicas: {self.paciente_info.get('enfermedades', 'N/A')}", color=self.COLOR_ERROR, font_family="Roboto", weight=ft.FontWeight.W_500),
                    ]),
                ], 
                spacing=8
            ),
            padding=20,
            bgcolor=self.COLOR_FONDO_CARD
        )
        paciente_card = ft.Card(content=paciente_card_content, elevation=8, margin=ft.margin.only(bottom=20))

        # 2. FORMULARIO DE ATENCIÓN
        form_column = ft.Container(
            content=ft.Column([
                ft.Text("📝 Registro de la Consulta", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                ft.Divider(),
                self.sistema,
                self.diagnostico,
                self.recomendaciones,
                
                # Fila de Carga de Imágenes
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Cargar Imágenes", icon=ft.Icons.UPLOAD_FILE, 
                            bgcolor=self.COLOR_PRIMARIO, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=lambda e: self.file_picker.pick_files(allow_multiple=True),
                            tooltip="Seleccionar imágenes para análisis YOLO"
                        ),
                        self.image_count_text # Muestra el contador de imágenes
                    ],
                    alignment=ft.MainAxisAlignment.START, spacing=15
                ),
                
                ft.Divider(height=20),
                
                # Fila de Acciones (Guardar y Volver)
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Guardar Atención", icon=ft.Icons.SAVE_AS, width=220, 
                            bgcolor=self.COLOR_EXITO, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=8),
                            on_click=self.guardar_atencion
                        ),
                        ft.ElevatedButton(
                            "Volver a Citas", icon=ft.Icons.ARROW_BACK, width=220, 
                            bgcolor=self.COLOR_ERROR, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                            on_click=lambda e: self.on_navigate("citas")
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER, spacing=30
                )
            ], spacing=15),
            padding=20,
            bgcolor=self.COLOR_FONDO_CARD,
            border_radius=15
        )
        form_card = ft.Card(content=form_column, elevation=8, expand=3) # Expand 3 para darle más peso

        # 3. RESULTADOS YOLO (Separado y con scroll)
        yolo_column = ft.Container(
            content=ft.Column([
                ft.Text("🔍 Resultados de Detección (YOLO)", size=20, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto"),
                ft.Divider(),
                self.yolo_results
            ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE),
            padding=20,
            bgcolor=self.COLOR_FONDO_CARD,
            border_radius=15,
            expand=2 # Expand 2 para que ocupe menos espacio que el formulario
        )
        yolo_card = ft.Card(content=yolo_column, elevation=8, expand=2)

        # 4. DISTRIBUCIÓN GENERAL (Header, Paciente, y Dos Columnas)
        main_column_content = ft.Column( # Cambiamos el nombre de la variable para ser más claros
            [
                ft.Text("ATENCIÓN CLÍNICA DETALLADA", size=28, weight=ft.FontWeight.W_900, color=self.COLOR_TEXTO, font_family="Roboto", text_align=ft.TextAlign.CENTER),
                paciente_card,
                ft.Row(
                    [
                        form_card,
                        yolo_card
                    ],
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START # Alineación superior
                )
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            # Se eliminó 'padding=20' de aquí
        )

        # 🛑 SOLUCIÓN: Envolver el Column en un Container y aplicar el padding aquí.
        main_content = ft.Container(
            content=main_column_content,
            padding=20, # Aplicamos el padding al Container
            expand=True
        )

        self.page.add(main_content)
        self.page.update()