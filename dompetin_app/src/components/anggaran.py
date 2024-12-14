import flet as ft
from components.carousel import create_carousel, update_carousel
from components.charts import create_bar_chart, create_line_chart, update_charts, create_pie_chart
from components.transaksi import TransactionManager
from datetime import datetime

def show_month_year_picker(page: ft.Page, selected_month: int, selected_year: int, carousel_container: ft.Container, charts: list):
    # Fungsi submit
    def on_submit(e):
        # Mengupdate value dropdown
        month = month_dropdown.value 
        year = year_dropdown.value
        dialog.open = False # menutup dialog
        page.update()
        update_charts(page, month, year, charts) 
        update_carousel(carousel_container, page, charts)
    
    months = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    current_year = datetime.now().year # Menyimpan current year
    years = [str(year) for year in range(current_year-5, current_year+5)]  # Range years

    month_dropdown = ft.Dropdown( # drop down untuk memilih bulan
        value=months[selected_month - 1],  
        options=[ft.dropdown.Option(month) for month in months],
        label="Select Month"
    )
    
    year_dropdown = ft.Dropdown( # drop down untuk memilih tahun
        value=str(selected_year),  
        options=[ft.dropdown.Option(year) for year in years],
        label="Select Year"
    )

    submit_button = ft.ElevatedButton("Submit", on_click=on_submit) # submit button (menggunakan fungsi submit)

    dialog = ft.AlertDialog(
        content=ft.Column(
            [month_dropdown, year_dropdown, submit_button],
            spacing=20,
            height=200,
        ),
        alignment=ft.alignment.center
    )

    page.dialog = dialog
    dialog.open = True
    page.update()


def BudgetView(page: ft.Page):
    selected_month = 1  
    selected_year = datetime.now().year  

    carousel_container = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
    )

    charts = []

    select_month_year_button = ft.ElevatedButton(
        "Select Month and Year",
        on_click=lambda e: show_month_year_picker(page, selected_month, selected_year, carousel_container, charts)
    )

    transactions = TransactionManager(page)._load_transactions()
    bar_chart_container = ft.Container(
        alignment=ft.alignment.center,
        expand=True
    )
    line_chart_container = ft.Container(
        alignment=ft.alignment.center,
        expand=True
    )
    pie_chart_container = ft.Container(
        content=ft.Text("Hint: Hover cursor over the chart", size=14),
        alignment=ft.alignment.center,
        expand=True
    )

    create_bar_chart(bar_chart_container, transactions, selected_month, selected_year)
    create_line_chart(line_chart_container, transactions, selected_month, selected_year)
    create_pie_chart(pie_chart_container, transactions, selected_month, selected_year)

    charts = [
        bar_chart_container,
        line_chart_container,
        pie_chart_container,
    ]

    initial_carousel = create_carousel(page, charts)
    carousel_container.content = initial_carousel

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome to the Anggaran/Budget view!", size=30),
                ft.Container(
                    content=ft.Column(
                        [
                        carousel_container, 
                        select_month_year_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )