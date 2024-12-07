import flet as ft

def DashboardView(page: ft.Page):
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
                ft.Text("Welcome to the Dashboard!", size=30),
                # Add more dashboard widgets here
                ft.Text("Your financial overview", size=20),
                # Example of additional dashboard elements
                ft.Row([
                    ft.Container(
                        content=ft.Text("Total Balance", size=18),
                        bgcolor=ft.colors.BLUE_100,
                        padding=10,
                        width=200
                    ),
                    ft.Container(
                        content=ft.Text("Recent Transactions", size=18),
                        bgcolor=ft.colors.GREEN_100,
                        padding=10,
                        width=200
                    )
                ])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )