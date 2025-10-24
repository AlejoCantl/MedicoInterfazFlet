import flet as ft

class CitasView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        
        # --- Constantes de Estilo (mismas que HistorialView) ---
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"
        self.COLOR_FONDO_CLARO = "#F8F9FA"
        
        self.citas = self.api.get_citas_aprobadas()

    def show(self):
        self.page.clean()

        # 🎯 Header con título centrado (igual que HistorialView)
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
                    width=100,
                ),
                # Título centrado
                ft.Container(
                    content=ft.Text(
                        "CITAS APROBADAS", 
                        size=28, 
                        weight=ft.FontWeight.W_900, 
                        color=self.COLOR_PRIMARIO, 
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER
                    ),
                    expand=True,
                    alignment=ft.alignment.center
                ),
                # Espaciador derecho para balance
                ft.Container(width=100),
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=10,
        )

        # Si no hay citas, mostrar mensaje
        if not self.citas:
            mensaje_vacio = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EVENT_BUSY, size=80, color=ft.Colors.GREY_400),
                    ft.Text(
                        "No hay citas aprobadas", 
                        size=18, 
                        weight=ft.FontWeight.W_500,
                        color=self.COLOR_TEXTO, 
                        font_family="Roboto",
                        text_align=ft.TextAlign.CENTER
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20),
                padding=60,
                alignment=ft.alignment.center
            )

            main_content = ft.Column([
                header,
                ft.Card(
                    content=mensaje_vacio,
                    margin=20,
                    elevation=5,
                    expand=True,
                ),
            ], expand=True)

            self.page.add(
                ft.Container(
                    content=main_content,
                    bgcolor=self.COLOR_FONDO_CLARO,
                    expand=True,
                    padding=10,
                )
            )
            self.page.update()
            return

        # Construir filas de la tabla
        rows = []
        for c in self.citas:
            cita_id_key = c.get("cita_id") if c.get("cita_id") is not None else c.get("id")
            paciente_id = c.get("usuario_paciente_id") or c.get("paciente_id")
            
            if cita_id_key is not None:
                rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(
                            str(cita_id_key), 
                            font_family="Roboto", 
                            color=self.COLOR_TEXTO,
                            weight=ft.FontWeight.W_500
                        )),
                        ft.DataCell(ft.Text(
                            c.get("paciente", "N/A"), 
                            font_family="Roboto", 
                            color=self.COLOR_TEXTO,
                            weight=ft.FontWeight.W_500
                        )),
                        ft.DataCell(ft.Text(
                            f"{c.get('fecha_cita', 'N/A')} {c.get('hora_cita', '')}".strip(), 
                            font_family="Roboto", 
                            color=self.COLOR_TEXTO
                        )),
                        ft.DataCell(ft.Text(
                            c.get("especialidad", "N/A"), 
                            font_family="Roboto", 
                            color=self.COLOR_TEXTO,
                            italic=True
                        )),
                        ft.DataCell(ft.ElevatedButton(
                            "Atender", 
                            icon=ft.Icons.MEDICAL_SERVICES, 
                            bgcolor=self.COLOR_EXITO, 
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=lambda e, cid=cita_id_key, pid=paciente_id: self.on_navigate("atencion", cita_id=cid, paciente_id=pid)
                        ))
                    ]
                ))

        # Tabla de citas
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Paciente", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Fecha/Hora", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Especialidad", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            heading_row_color=ft.Colors.with_opacity(0.1, self.COLOR_PRIMARIO),
            column_spacing=20,
            data_row_max_height=80,
            width=None,
        )

        # 🎯 Contenedor de tabla expandible
        tabla_container = ft.Container(
            content=ft.Column(
                [table],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            expand=True,
            padding=10,
            alignment=ft.alignment.top_center,
        )

        # Contenido principal
        main_content = ft.Column(
            [
                header,
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [tabla_container],
                            expand=True,
                        ), 
                        padding=25,
                        expand=True,
                    ), 
                    margin=20,
                    elevation=5,
                    expand=True,
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