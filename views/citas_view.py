import flet as ft

class CitasView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.citas = self.api.get_citas_aprobadas()

    def show(self):
        self.page.clean()
        self.page.add(ft.Text("Citas Aprobadas", size=20))

        if not self.citas:
            self.page.add(ft.Text("No hay citas aprobadas"))
            self.page.add(ft.ElevatedButton("Volver", on_click=lambda e: self.on_navigate("main")))
            return

        rows = []
        for c in self.citas:
            if c.get("estado") == "Aprobada":
                paciente_id = c.get("usuario_paciente_id") or c.get("paciente_id")
                rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.get("id")))),
                        ft.DataCell(ft.Text(c.get("medico", "N/A"))),
                        ft.DataCell(ft.Text(f"{c.get('fecha_cita')} {c.get('hora_cita')}")),
                        ft.DataCell(ft.ElevatedButton("Atender", 
                            on_click=lambda e, cid=c["id"], pid=paciente_id: 
                                self.on_navigate("atencion", cita_id=cid, paciente_id=pid)
                        ))
                    ]
                ))

        table = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Fecha/Hora")),
            ft.DataColumn(ft.Text("Acción")),
        ], rows=rows)

        self.page.add(table)
        self.page.add(ft.ElevatedButton("Volver", on_click=lambda e: self.on_navigate("main")))