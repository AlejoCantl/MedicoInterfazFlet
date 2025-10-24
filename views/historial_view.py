import flet as ft

class HistorialView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"

        self.search_name = ft.TextField(
            label="Nombre o Apellido", width=300, bgcolor="white", border_color=self.COLOR_PRIMARIO, font_family="Roboto"
        )
        self.search_id = ft.TextField(
            label="Cédula", width=300, bgcolor="white", border_color=self.COLOR_PRIMARIO, font_family="Roboto"
        )
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Paciente", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Diagnóstico", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Recomendaciones", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
            ],
            rows=[],
            border=ft.border.all(1, "grey300"),
            border_radius=10,
            heading_row_color=ft.Colors.with_opacity(0.1, self.COLOR_PRIMARIO)
        )

    def buscar(self, e):
        historial = self.api.get_historial_medico(self.search_name.value, self.search_id.value)
        self.update_table(historial)

    def update_table(self, data):
        rows = []
        for h in data:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(h.get("paciente", "N/A"), font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataCell(ft.Text(h.get("fecha", "N/A"), font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataCell(ft.Text((h.get("diagnostico") or "")[:60] + "..." if len(h.get("diagnostico") or "") > 60 else h.get("diagnostico", ""), font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataCell(ft.Text((h.get("recomendaciones") or "")[:60] + "..." if len(h.get("recomendaciones") or "") > 60 else h.get("recomendaciones", ""), font_family="Roboto", color=self.COLOR_TEXTO)),
            ]))
        self.table.rows = rows
        self.page.update()

    def show(self):
        self.page.clean()

        self.page.add(
            ft.Text("Historial Médico", size=24, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto", text_align=ft.TextAlign.CENTER),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            self.search_name,
                            self.search_id,
                            ft.ElevatedButton(
                                "Buscar", icon=ft.icons.SEARCH, width=200, bgcolor=self.COLOR_PRIMARIO, color="white",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                                on_click=self.buscar
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        self.table
                    ], spacing=15),
                    padding=20,
                    bgcolor="white"
                ),
                elevation=5,
                margin=20
            ),
            ft.ElevatedButton(
                "Volver", icon=ft.icons.ARROW_BACK, width=200, bgcolor=self.COLOR_PRIMARIO, color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                on_click=lambda e: self.on_navigate("main")
            )
        )
        self.page.update()