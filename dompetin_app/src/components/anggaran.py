import flet as ft
from dataclasses import dataclass
from fletcarousel import BasicAnimatedHorizontalCarousel, HintLine, AutoCycle
from components.carousel import create_carousel
from components.charts import BudgetChartManager, create_bar_chart
from components.transaksi import TransactionManager

def BudgetView(page: ft.Page):
    transactions = TransactionManager(page)._load_transactions()
    bar_chart_container = ft.Container(
        alignment=ft.alignment.center,
        expand=True
    )
    create_bar_chart(bar_chart_container, transactions)

    contents = [
        bar_chart_container,
        ft.Container(content=ft.Text("Comparison Chart", size=30), alignment=ft.alignment.center, expand=True),
        ft.Container(content=ft.Text("Future Projections", size=30), alignment=ft.alignment.center, expand=True),
    ]

    carousel = create_carousel(page, contents)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to the Anggaran/Budget view!", size=30),
                carousel,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
