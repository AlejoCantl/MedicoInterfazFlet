import flet as ft

class CitasView:
    def __init__(self, page: ft.Page, api_client, on_navigate):
        self.page = page
        self.api = api_client
        self.on_navigate = on_navigate
        self.COLOR_PRIMARIO = "#007BFF"
        self.COLOR_TEXTO = "#343A40"
        self.COLOR_EXITO = "#28A745"
        self.citas = self.api.get_citas_aprobadas()

    def show(self):
        self.page.clean()

        self.page.add(
            ft.Text("Citas Aprobadas", size=24, weight=ft.FontWeight.BOLD, color=self.COLOR_TEXTO, font_family="Roboto", text_align=ft.TextAlign.CENTER)
        )

        if not self.citas:
            self.page.add(
                ft.Text("No hay citas aprobadas", size=16, italic=True, color=self.COLOR_TEXTO, font_family="Roboto", text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    "Volver", icon=ft.icons.ARROW_BACK, width=200, bgcolor=self.COLOR_PRIMARIO, color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=5),
                    on_click=lambda e: self.on_navigate("main")
                )
            )
            return

        rows = []
        for c in self.citas:
            if c.get("estado") == "Aprobada":
                paciente_id = c.get("usuario_paciente_id") or c.get("paciente_id")
                rows.append(ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c.get("id")), font_family="Roboto", color=self.COLOR_TEXTO)),
                        ft.DataCell(ft.Text(c.get("paciente", c.get("medico", "N/A")), font_family="Roboto", color=self.COLOR_TEXTO)),
                        ft.DataCell(ft.Text(f"{c.get('fecha_cita')} {c.get('hora_cita')}", font_family="Roboto", color=self.COLOR_TEXTO)),
                        ft.DataCell(ft.Text(c.get("especialidad", "N/A"), font_family="Roboto", color=self.COLOR_TEXTO)),
                        ft.DataCell(ft.ElevatedButton(
                            "Atender", icon=ft.icons.MEDICAL_SERVICES, bgcolor=self.COLOR_EXITO, color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=3),
                            on_click=lambda e, cid=c["id"], pid=paciente_id: self.on_navigate("atencion", cita_id=cid, paciente_id=pid)
                        ))
                    ]
                ))

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Paciente", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Fecha/Hora", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Especialidad", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
                ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD, font_family="Roboto", color=self.COLOR_TEXTO)),
            ],
            rows=rows,
            border=ft.border.all(1, "grey300"),
            border_radius=10,
            heading_row_color=ft.colors.with_opacity(0.1, self.COLOR_PRIMARIO)
        )

        self.page.add(
            ft.Card(
                content=ft.Container(content=table, padding=10),
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