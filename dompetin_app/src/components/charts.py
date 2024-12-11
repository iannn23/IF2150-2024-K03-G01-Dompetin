import flet as ft
import calendar
from typing import List
from collections import defaultdict
from components.transaksi import Transaction
from datetime import datetime
from components.transaksi import TransactionManager

class State:
    toggle = True

s = State()

def update_charts(page: ft.Page, month: str, year: str, charts: list): 
    months_dict = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, 
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    month_num = months_dict.get(month)
    if month_num is None:
        raise ValueError(f"Invalid month name: {month}")

    transactions = TransactionManager(page)._load_transactions()
    bar_chart_container = ft.Container( # membuat bar chart container baru
        alignment=ft.alignment.center,
        expand=True
    )
    line_chart_container = ft.Container( # membuat line chart container baru
        alignment=ft.alignment.center,
        expand=True
    )

    # Membuat chart baru
    create_bar_chart(bar_chart_container, transactions, month, year)
    create_line_chart(line_chart_container, transactions, month, year)

    contents = [
        bar_chart_container,
        line_chart_container,
    ]

    charts.clear()  
    charts.extend(contents) 

def create_bar_chart(bar_chart_container: ft.Container, transactions: List[Transaction], month: int, year: int):
    if isinstance(month, str):
        months_dict = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, 
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        month = months_dict.get(month, 12)  # mengkonversi string month menjadi int
    
    year = int(year)
    
    num_days = calendar.monthrange(year, month)[1] # mendapatkan jumlah hari pada bulan

    # inisiasi jumlah hari dalam sebulan pada dictionary income dan expense
    income = {day: 0 for day in range(1, num_days + 1)} 
    expense = {day: 0 for day in range(1, num_days + 1)}

    # mendapatkan income dan expense dari list data transaksi
    for t in transactions:
        transaction_date = datetime.strptime(t.date, "%Y-%m-%d") # mengubah t.date menjadi datetime object
        if transaction_date.year == year and transaction_date.month == month:
            day = transaction_date.day
            if t.transaction_type == "income": 
                income[day] += t.amount # Mennjumlahkan total income dalam hari yang sama
            else:
                expense[day] += t.amount # Menjumlahkan total expense dalam hari yang sama

    bar_groups = []
    for day in range(1, num_days + 1): # iterasi sebanyak total hari
        bar_groups.append(
            ft.BarChartGroup (
                x = day-1, # memastikan x-axis mulai dari x = 0
                bar_rods=[
                    ft.BarChartRod( # Bar rod untuk income
                        from_y=0,
                        to_y=income[day],
                        width=20,
                        color=ft.Colors.GREEN,
                        tooltip=f"Day{day}: {income[day]}",
                        border_radius=2
                    ),
                    ft.BarChartRod( # Bar rod untuk expense
                        from_y=0,
                        to_y=expense[day],
                        width=20,
                        color=ft.Colors.RED,
                        tooltip=f"Day{day}: {expense[day]}",
                        border_radius=2,
                    ),
                ],
            )
        )

    chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, ft.Colors.GREY_400),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Amount(Rp)"),
            title_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=day - 1, 
                    label=ft.Container(ft.Text(str(day)), padding=10)
            ) for day in range(1, num_days + 1)],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
        max_y = max(max(income.values()), max(expense.values())), # set max height
        interactive=True,
        expand=True,
    )

    bar_chart_container.content = chart


def create_line_chart(line_chart_container: ft.Container, transactions: List[Transaction], month: int, year: int):
    if isinstance(month, str):
        months_dict = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, 
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        month = months_dict.get(month, 12)  
    
    year = int(year)
    
    num_days = calendar.monthrange(year, month)[1]

    income = {day: 0 for day in range(1, num_days + 1)}
    expense = {day: 0 for day in range(1, num_days + 1)}
    
    for t in transactions:
        transaction_date = datetime.strptime(t.date,"%Y-%m-%d")
        if transaction_date.year == year and transaction_date.month == month:
            day = transaction_date.day
            if t.transaction_type == "income":
                income[day] += t.amount
            else:
                expense[day] += t.amount

    x_values = list(range(1, num_days + 1))
    max_y = max(max(income.values()), max(expense.values()))  

    line_chart_1 = [
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, income[x]) for x in (x_values)],
            stroke_width=2,
            color=ft.Colors.LIGHT_GREEN,
            curved=True,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, expense[x]) for x in (x_values)],
            stroke_width=2,
            color=ft.Colors.RED_700,
            curved=True,
            stroke_cap_round=True,
        ),
    ]

    line_chart_2 = [
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, income[x]) for x in (x_values)],
            stroke_width=2,
            color=ft.Colors.LIGHT_GREEN,
            stroke_cap_round=True,
        ),
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, expense[x]) for x in (x_values)],
            stroke_width=2,
            color=ft.Colors.RED_700,
            stroke_cap_round=True,
        ),
    ]

    chart = ft.LineChart(
        data_series=line_chart_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        ),
        left_axis=ft.ChartAxis(
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=x,
                    label=ft.Container(
                        ft.Text(
                            str(x),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                )
                for x in x_values # menampilkan tanggal pada bulan
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY),
        min_y=0,
        max_y=max_y,
        interactive=True,
        expand=True,
    )

    def toggle_data(e): # ganti model line chart (terdapat 2 model: curved & not curved)
        if s.toggle:
            chart.data_series = line_chart_2
            chart.max_y = max_y + 2
            chart.interactive = False
        else:
            chart.data_series = line_chart_1
            chart.max_y = max_y
            chart.interactive = True
        s.toggle = not s.toggle
        chart.update()

    toggle_button = ft.ElevatedButton("Toggle Line Chart", on_click=toggle_data)
    line_chart_container.content = ft.Column([chart, toggle_button])
