from datetime import datetime
import flet as ft

class HistorialView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        
        # --- Constantes de Estilo ---
        self.COLOR_PRIMARIO = "#007BFF"     # Azul principal
        self.COLOR_TEXTO = "#343A40"        # Gris oscuro para texto
        self.COLOR_EXITO = "#28A745"        # Verde
        self.COLOR_FONDO_CLARO = "#F8F9FA"  # Fondo de tarjetas
        
        # Estilo común para el texto de los TextFields
        self.TEXT_INPUT_STYLE = ft.TextStyle(font_family="Roboto", color=self.COLOR_TEXTO)
        # Estilo común para la etiqueta (label) de los TextFields
        self.LABEL_INPUT_STYLE = ft.TextStyle(font_family="Roboto", color=self.COLOR_PRIMARIO, weight=ft.FontWeight.BOLD)

        self.search_name = ft.TextField(
            label="Buscar por Nombre o Apellido",
            width=300, 
            bgcolor=ft.Colors.WHITE, 
            border_color=self.COLOR_PRIMARIO,
            border_radius=10,
            text_style=self.TEXT_INPUT_STYLE,
            label_style=self.LABEL_INPUT_STYLE,
            prefix_icon=ft.Icons.PERSON_OUTLINE
        )
        
        self.search_id = ft.TextField(
            label="Buscar por Cédula",
            width=300, 
            bgcolor=ft.Colors.WHITE, 
            border_color=self.COLOR_PRIMARIO,
            border_radius=10,
            text_style=self.TEXT_INPUT_STYLE,
            label_style=self.LABEL_INPUT_STYLE,
            prefix_icon=ft.Icons.BADGE
        )
        
        # 🎯 MEJORA: Tabla con expand=True y mejor espaciado
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Paciente", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Cédula", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Diagnóstico", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Recomendaciones", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Sistema", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Especialidad", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            heading_row_color=ft.Colors.with_opacity(0.1, self.COLOR_PRIMARIO),
            column_spacing=20,  # Reducido para mejor distribución
            sort_column_index=2,
            sort_ascending=False,
            data_row_max_height=100,
            width=None,  # Permite que la tabla use todo el ancho disponible
        )
        
        # Inicializa la tabla con todos los registros al cargar
        self.buscar(None) 

    def buscar(self, e):
        """Busca el historial médico basado en los campos de búsqueda."""
        historial = self.api.get_historial_medico(self.search_name.value, self.search_id.value)
        self.update_table(historial)

    def update_table(self, data):
        """Actualiza las filas de la tabla con los datos proporcionados."""
        rows = []
        
        # Función auxiliar para truncar texto
        def format_text(text, max_len=60):
            t = h.get(text, "") or ""
            return t[:max_len] + "..." if len(t) > max_len else t

        for h in data:
            fecha_str = h.get("fecha")
            hora_str = h.get("hora_cita")
            
            fecha_display = "N/A"

            if fecha_str:
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                    fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
                    hora_formateada = hora_str[:5] if hora_str else ""
                    fecha_display = f"{fecha_formateada} {hora_formateada}".strip()
                except ValueError:
                    fecha_display = f"{fecha_str} {hora_str}"
            
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(h.get("paciente", "N/A"), font_family="Roboto", color=self.COLOR_TEXTO, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(h.get("identificacion", "N/A"), font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataCell(ft.Text(fecha_display, font_family="Roboto", color=self.COLOR_TEXTO)), 
                ft.DataCell(ft.Text(format_text("diagnostico"), font_family="Roboto", color=self.COLOR_TEXTO, italic=True)),
                ft.DataCell(ft.Text(format_text("recomendaciones"), font_family="Roboto", color=self.COLOR_TEXTO, italic=True)),
                ft.DataCell(ft.Text(format_text("sistema"), font_family="Roboto", color=self.COLOR_TEXTO, italic=True)),
                ft.DataCell(ft.Text(format_text("especialidad"), font_family="Roboto", color=self.COLOR_TEXTO, italic=True)),
            ]))
        self.table.rows = rows
        self.page.update()

    def show(self):
        self.page.clean()

        # 🎯 Header with perfectly centered title
        header = ft.Container(
            content=ft.Row([
                # Botón izquierdo con ancho fijo
                ft.Container(
                    content=ft.ElevatedButton(
                        "Volver", 
                        icon=ft.Icons.ARROW_BACK, 
                        width=100, 
                        bgcolor=self.COLOR_PRIMARIO, 
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=lambda e: self.on_navigate("main")
                    ),
                    width=100,  # Ancho fijo para balance
                ),
                # Título centrado
                ft.Container(
                    content=ft.Text(
                        "HISTORIAL MÉDICO", 
                        size=28, 
                        weight=ft.FontWeight.W_900, 
                        color=self.COLOR_PRIMARIO, 
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
                # Espaciador derecho del mismo ancho que el botón
                ft.Container(width=100),  # Balance perfecto
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=10,
        )

        # 🎯 MEJORA CLAVE: Contenedor de tabla que ocupa todo el espacio
        tabla_container = ft.Container(
            content=ft.Column(
                [self.table],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH  # Estira horizontalmente
            ),
            expand=True,  # Ocupa todo el espacio vertical disponible
            padding=10,
            alignment=ft.alignment.top_center,
        )

        # Main content
        main_content = ft.Column(
            [
                header,
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row([
                                    self.search_name,
                                    self.search_id,
                                    ft.ElevatedButton(
                                        "Buscar", 
                                        icon=ft.Icons.SEARCH, 
                                        width=200, 
                                        bgcolor=self.COLOR_PRIMARIO, 
                                        color=ft.Colors.WHITE,
                                        on_click=self.buscar
                                    )
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                ft.Divider(height=20, color=ft.Colors.GREY_300),
                                tabla_container  # Tabla mejorada
                            ],
                            expand=True,  # La columna se expande
                        ), 
                        padding=25,
                        expand=True,
                    ), 
                    margin=20,
                    elevation=5,
                    expand=True,  # Card se expande
                ),
            ],
            expand=True,
            spacing=0,
        )

        self.page.add(
            ft.Container(
                content=main_content,
                bgcolor=self.COLOR_FONDO_CLARO,
                expand=True,
                padding=10,
            )
        )
        self.page.update()