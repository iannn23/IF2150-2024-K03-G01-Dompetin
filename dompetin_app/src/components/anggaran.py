import flet as ft

def BudgetView(page: ft.Page):
    """
    Create and return the dashboard view
    
    Args:
        page (ft.Page): The main page object
    
    Returns:
        ft.Container: Dashboard content
    """
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to the Anggaran/Budget view!", size=30),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )