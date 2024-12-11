import flet as ft
from flet import Theme
from components.dashboard import DashboardView  # Import the dashboard view
from components.transaksi import TransactionView  # Import the transaction view
from components.anggaran import BudgetView  # Import the budget view
from components.inputform import InputFormView  # Import the input form view

def main(page: ft.Page):
    # Page configuration
    page.fonts = {
        "Custom-Fonts": "dompetin_app/src/fonts/Poppins-SemiBold.ttf"
    }
    page.bgcolor = "#F5F7FA"
    page.theme = Theme(font_family="Custom-Fonts")

    # Navigation Rail (same as previous example)
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        leading=ft.Row(
            [
                ft.Image(src="dompetin_app/src/assets/image.png", width=50, height=56.08),
                ft.Text("Dompetin", color=ft.Colors.BLACK, size=28, font_family="Custom-Fonts"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icon(ft.icons.DASHBOARD, color=ft.colors.BLUE_700, size=30),
                label_content=ft.Text("Dashboard", size=16)
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SWAP_HORIZ_OUTLINED,
                selected_icon=ft.Icon(ft.icons.SWAP_HORIZ, color=ft.colors.BLUE_700, size=30),
                label_content=ft.Text("Transaksi", size=16)
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SHOPPING_CART_OUTLINED,
                selected_icon=ft.Icon(ft.icons.SHOPPING_CART, color=ft.colors.BLUE_700, size=30),
                label_content=ft.Text("Anggaran", size=16),
            ),
        ],
        
        on_change=lambda e: page.go(["/dashboard", "/transaksi", "/anggaran"][e.control.selected_index]),
    )

    # Content area
    content = ft.Container(expand=True)

    # Route change handler
    def route_change(route_event):
        # Update content based on route
        content.content = {
            "/dashboard": DashboardView(page),
            "/transaksi": TransactionView(page),
            "/anggaran": BudgetView(page),
        }.get(page.route, ft.Text("Page not found"))
        
        # Update navigation rail selection to match route
        routes = ["/dashboard", "/transaksi", "/anggaran"]
        rail.selected_index = routes.index(page.route) if page.route in routes else 0
        
        page.update()

    # Page layout
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content
            ],
            expand=True,
        )
    )

    # Set up routing
    page.on_route_change = route_change
    page.go("/dashboard")  # Initial route

ft.app(target=main)