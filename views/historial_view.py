import flet as ft

class HistorialView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.search_name = ft.TextField(label="Nombre o Apellido", width=300)
        self.search_id = ft.TextField(label="Cédula", width=300)
        self.table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Diagnóstico")),
            ft.DataColumn(ft.Text("Recomendaciones")),
        ], rows=[])

    def buscar(self, e):
        historial = self.api.get_historial_medico(self.search_name.value, self.search_id.value)
        self.update_table(historial)

    def update_table(self, data):
        rows = []
        for h in data:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(h.get("paciente", "N/A"))),
                ft.DataCell(ft.Text(h.get("fecha", "N/A"))),
                ft.DataCell(ft.Text((h.get("diagnostico") or "")[:60] + "..." if len(h.get("diagnostico") or "") > 60 else h.get("diagnostico", ""))),
                ft.DataCell(ft.Text((h.get("recomendaciones") or "")[:60] + "..." if len(h.get("recomendaciones") or "") > 60 else h.get("recomendaciones", ""))),
            ]))
        self.table.rows = rows
        self.page.update()

    def show(self):
        self.page.clean()
        self.page.add(
            ft.Text("Historial Médico", size=20),
            ft.Row([self.search_name, self.search_id, ft.ElevatedButton("Buscar", on_click=self.buscar)]),
            self.table,
            ft.ElevatedButton("Volver", on_click=lambda e: self.on_navigate("main"))
        )