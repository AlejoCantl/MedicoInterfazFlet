import flet as ft
import os

class AtencionView:
    def __init__(self, page: ft.Page, api_client, on_navigate, cita_id: int, paciente_id: int):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.cita_id = cita_id
        self.paciente_id = paciente_id
        
        # Colores consistentes con otras vistas
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"
        self.COLOR_ERROR = "#DC3545"
        self.COLOR_FONDO_CLARO = "#F8F9FA"

        # Estilos de texto
        text_style = ft.TextStyle(font_family="Roboto", color=self.COLOR_TEXTO)
        label_style = ft.TextStyle(font_family="Roboto", color=self.COLOR_PRIMARIO, weight=ft.FontWeight.BOLD)

        # Campos del formulario
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
            hint_text="Describe los síntomas y sistemas involucrados"
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
            hint_text="Escribe el diagnóstico médico"
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
            hint_text="Detalla el plan de manejo y seguimiento"
        )
        
        self.uploaded_images = []
        self.yolo_results = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.file_picker = ft.FilePicker(on_result=self.on_files_selected)
        page.overlay.append(self.file_picker)

        self.paciente_info = self.api.get_paciente_info(self.paciente_id)
        self.image_count_text = ft.Text(
            "0 imágenes adjuntas", 
            color=self.COLOR_TEXTO,
            font_family="Roboto",
            weight=ft.FontWeight.W_500
        )

        # Inicializar SnackBar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Mensaje temporal"),
            duration=3000
        )

    def _show_snack_bar(self, message: str, color: str):
        """Muestra notificaciones al usuario."""
        self.page.snack_bar.content = ft.Text(message, font_family="Roboto")
        self.page.snack_bar.bgcolor = color
        self.page.snack_bar.open = True
        self.page.update()

    def on_files_selected(self, e: ft.FilePickerResultEvent):
        """Maneja la selección de archivos."""
        if e.files:
            self.uploaded_images = e.files
            self.image_count_text.value = f"✅ {len(e.files)} imágenes adjuntas"
            self.image_count_text.color = self.COLOR_EXITO
            self._show_snack_bar(
                f"✅ {len(e.files)} imágenes cargadas exitosamente", 
                self.COLOR_EXITO
            )
        else:
            self.image_count_text.value = "❌ 0 imágenes adjuntas"
            self.image_count_text.color = self.COLOR_ERROR
        self.page.update()

    def resetear_formulario(self):
        """Resetea todos los campos del formulario."""
        self.sistema.value = ""
        self.diagnostico.value = ""
        self.recomendaciones.value = ""
        self.uploaded_images = []
        self.image_count_text.value = "0 imágenes adjuntas"
        self.image_count_text.color = self.COLOR_TEXTO
        self.page.update()

    def guardar_atencion(self, e):
        """Guarda la atención médica y procesa las imágenes con YOLO."""
        if not all([self.sistema.value, self.diagnostico.value, self.recomendaciones.value]):
            self._show_snack_bar("⚠️ Complete todos los campos obligatorios", self.COLOR_ERROR)
            return

        # Deshabilitar botón mientras procesa
        e.control.disabled = True
        e.control.text = "Procesando..."
        self.page.update()

        response = self.api.registrar_atencion(
            cita_id=self.cita_id,
            sistema=self.sistema.value,
            diagnostico=self.diagnostico.value,
            recomendaciones=self.recomendaciones.value,
            imagenes=self.uploaded_images
        )
        
        # Rehabilitar botón
        e.control.disabled = False
        e.control.text = "Guardar Atención"
        self.page.update()

        if "error" not in response:
            # Limpiar resultados anteriores
            self.yolo_results.controls.clear()
            
            resultados_yolo = response.get("detections", [])
            
            if resultados_yolo and len(resultados_yolo) > 0:
                # Header de resultados
                self.yolo_results.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=self.COLOR_EXITO, size=24),
                            ft.Text(
                                "Detecciones realizadas con éxito", 
                                size=16, 
                                weight=ft.FontWeight.BOLD,
                                color=self.COLOR_EXITO,
                                font_family="Roboto"
                            ),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.1, self.COLOR_EXITO),
                        border_radius=10,
                    )
                )
                
                # Procesar cada imagen
                for idx, detecciones_por_imagen in enumerate(resultados_yolo):
                    imagen_name = self.uploaded_images[idx].name if idx < len(self.uploaded_images) else f"Imagen {idx + 1}"
                    
                    # Crear lista de detecciones
                    if detecciones_por_imagen:
                        detections_widgets = []
                        for d in detecciones_por_imagen:
                            confidence = d.get('confidence', 0.0)
                            confidence_color = self.COLOR_EXITO if confidence > 0.7 else self.COLOR_PRIMARIO if confidence > 0.5 else self.COLOR_ERROR
                            
                            detections_widgets.append(
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CIRCLE, size=8, color=confidence_color),
                                        ft.Text(
                                            f"{d.get('class', 'N/A')}", 
                                            color=self.COLOR_TEXTO,
                                            font_family="Roboto",
                                            weight=ft.FontWeight.W_500,
                                            size=14
                                        ),
                                        ft.Container(expand=True),
                                        ft.Text(
                                            f"{confidence:.1%}", 
                                            color=confidence_color,
                                            font_family="Roboto",
                                            weight=ft.FontWeight.BOLD,
                                            size=13
                                        ),
                                    ]),
                                    padding=5,
                                )
                            )
                    else:
                        detections_widgets = [
                            ft.Text(
                                "No se detectaron objetos en esta imagen",
                                color=ft.Colors.GREY_600,
                                font_family="Roboto",
                                italic=True,
                                size=13
                            )
                        ]
                    
                    # Card para cada imagen
                    card = ft.Container(
                        content=ft.Column([
                            # Header de la imagen
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.IMAGE, color=self.COLOR_PRIMARIO, size=20),
                                    ft.Text(
                                        os.path.basename(imagen_name),
                                        weight=ft.FontWeight.BOLD,
                                        color=self.COLOR_PRIMARIO,
                                        font_family="Roboto",
                                        size=15
                                    ),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Text(
                                            f"{len(detecciones_por_imagen)} detecciones",
                                            color=ft.Colors.WHITE,
                                            font_family="Roboto",
                                            size=12,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        bgcolor=self.COLOR_PRIMARIO,
                                        border_radius=15
                                    )
                                ]),
                                padding=10,
                                bgcolor=ft.Colors.with_opacity(0.05, self.COLOR_PRIMARIO),
                            ),
                            # Lista de detecciones
                            ft.Container(
                                content=ft.Column(detections_widgets, spacing=2),
                                padding=10,
                            )
                        ]),
                        bgcolor=ft.Colors.WHITE,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=10,
                        padding=5,
                        margin=5,
                    )
                    self.yolo_results.controls.append(card)
            else:
                # No hay detecciones
                self.yolo_results.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=40, color=ft.Colors.GREY_400),
                            ft.Text(
                                "No se procesaron imágenes",
                                size=14,
                                color=ft.Colors.GREY_600,
                                font_family="Roboto",
                                text_align=ft.TextAlign.CENTER
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10),
                        padding=30,
                        alignment=ft.alignment.center
                    )
                )

            self._show_snack_bar("✅ Atención guardada exitosamente", self.COLOR_EXITO)
            # 🛑 CORRECCIÓN: Resetear el formulario después de guardar
            self.resetear_formulario()
        else:
            self._show_snack_bar(
                f"❌ Error: {response.get('error', 'Error desconocido')}", 
                self.COLOR_ERROR
            )

        self.page.update()

    def show(self):
        self.page.clean()

        # 🎯 Header con título centrado
        header = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.ElevatedButton(
                        "Volver",
                        icon=ft.Icons.ARROW_BACK,
                        bgcolor=self.COLOR_PRIMARIO,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=lambda e: self.on_navigate("citas")
                    ),
                    width=100,
                ),
                ft.Container(
                    content=ft.Text(
                        "ATENCIÓN MÉDICA",
                        size=28,
                        weight=ft.FontWeight.W_900,
                        color=self.COLOR_PRIMARIO,
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
                ft.Container(width=100),  # Espacio para mantener simetría
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=10,
        )

        # 1. TARJETA DE INFORMACIÓN DEL PACIENTE
        paciente_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, color=self.COLOR_PRIMARIO, size=28),
                        ft.Text(
                            "Información del Paciente",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                    ]),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                    ft.Row([
                        ft.Column([
                            ft.Text("Nombre:", size=12, color=ft.Colors.GREY_600, font_family="Roboto"),
                            ft.Text(
                                self.paciente_info.get('paciente', 'N/A'),
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=self.COLOR_TEXTO,
                                font_family="Roboto"
                            ),
                        ], spacing=2),
                        ft.VerticalDivider(),
                        ft.Column([
                            ft.Text("Edad:", size=12, color=ft.Colors.GREY_600, font_family="Roboto"),
                            ft.Text(
                                f"{self.paciente_info.get('edad', 'N/A')} años",
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=self.COLOR_TEXTO,
                                font_family="Roboto"
                            ),
                        ], spacing=2),
                        ft.VerticalDivider(),
                        ft.Column([
                            ft.Text("Tipo:", size=12, color=ft.Colors.GREY_600, font_family="Roboto"),
                            ft.Text(
                                self.paciente_info.get('tipo_paciente', 'N/A'),
                                size=15,
                                weight=ft.FontWeight.W_600,
                                color=self.COLOR_TEXTO,
                                font_family="Roboto"
                            ),
                        ], spacing=2),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    ft.Row([
                        ft.Icon(ft.Icons.EMAIL_OUTLINED, size=18, color=ft.Colors.GREY_600),
                        ft.Text(
                            self.paciente_info.get('correo', 'N/A'),
                            size=13,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.MONITOR_WEIGHT_OUTLINED, size=18, color=ft.Colors.GREY_600),
                        ft.Text(
                            f"Peso: {self.paciente_info.get('peso', 'N/A')} kg",
                            size=13,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                        ft.Text("|", color=ft.Colors.GREY_400),
                        ft.Text(
                            f"Talla: {self.paciente_info.get('talla', 'N/A')} m",
                            size=13,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                    ], spacing=10),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.WARNING_AMBER, size=18, color=self.COLOR_ERROR),
                            ft.Text(
                                f"Enfermedades: {self.paciente_info.get('enfermedades', 'Ninguna')}",
                                size=13,
                                weight=ft.FontWeight.W_500,
                                color=self.COLOR_ERROR,
                                font_family="Roboto"
                            ),
                        ], spacing=10),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.1, self.COLOR_ERROR),
                        border_radius=8,
                    ),
                ], spacing=12),
                padding=20,
            ),
            elevation=5,
            margin=ft.margin.only(bottom=15)
        )

        # 2. FORMULARIO DE ATENCIÓN
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.EDIT_NOTE, color=self.COLOR_PRIMARIO, size=24),
                        ft.Text(
                            "Registro de Consulta",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                    ]),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                    self.sistema,
                    self.diagnostico,
                    self.recomendaciones,
                    ft.Row([
                        ft.ElevatedButton(
                            "📎 Adjuntar Imágenes",
                            icon=ft.Icons.UPLOAD_FILE,
                            bgcolor=self.COLOR_PRIMARIO,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: self.file_picker.pick_files(allow_multiple=True)
                        ),
                        self.image_count_text
                    ], spacing=15, alignment=ft.MainAxisAlignment.START),
                    ft.Divider(height=10),
                    ft.ElevatedButton(
                        "Guardar Atención",
                        icon=ft.Icons.SAVE,
                        width=250,
                        height=45,
                        bgcolor=self.COLOR_EXITO,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=self.guardar_atencion
                    ),
                ], spacing=15, scroll=ft.ScrollMode.AUTO),  # Habilitar scroll
                padding=20,
            ),
            elevation=5,
            margin=ft.margin.only(bottom=15)
        )

        # 3. RESULTADOS YOLO
        yolo_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.BIOTECH, color=self.COLOR_PRIMARIO, size=24),
                        ft.Text(
                            "Resultados de Análisis YOLO",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=self.COLOR_TEXTO,
                            font_family="Roboto"
                        ),
                    ]),
                    ft.Divider(height=10, color=ft.Colors.GREY_300),
                    ft.Container(
                        content=self.yolo_results,
                        expand=True,
                    )
                ], spacing=10, scroll=ft.ScrollMode.AUTO),  # Habilitar scroll
                padding=20,
                expand=True,
            ),
            elevation=5,
        )

        # Layout con dos columnas
        main_content = ft.Column([
            header,
            paciente_card,
            ft.Row([
                ft.Container(content=form_card, expand=3),
                ft.Container(content=yolo_card, expand=2),
            ], expand=True, spacing=15, alignment=ft.MainAxisAlignment.START),
        ], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)  # Habilitar scroll en el contenedor principal

        self.page.add(
            ft.Container(
                content=main_content,
                bgcolor=self.COLOR_FONDO_CLARO,
                padding=10,
                expand=True,
            )
        )
        self.page.update()