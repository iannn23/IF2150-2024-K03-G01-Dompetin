import flet as ft
from dataclasses import dataclass
from typing import List
from collections import defaultdict
from components.transaksi import Transaction

class BudgetChartManager:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions  

    def groupByMonth(self):
        grouped_transactions = defaultdict(list)
        for transaction in self.transactions:
            month = transaction.date[:7]  
            grouped_transactions[month].append(transaction)
        return grouped_transactions

    def getMonthlyIncome(self):
        group = self.groupByMonth()
        months = sorted(group.keys())
        income = []
        for month in months:
            total_income = sum(t.amount for t in group[month] if t.transaction_type == "income")
            income.append(total_income)
        return months, income 

    def getMonthlyExpense(self):
        group = self.groupByMonth()
        months = sorted(group.keys())
        expense = []
        for month in months:
            total_expense = sum(t.amount for t in group[month] if t.transaction_type == "expense")
            expense.append(total_expense)
        return months, expense 


def create_bar_chart(bar_chart_container: ft.Container, transactions: List[Transaction]):
    chart_manager = BudgetChartManager(transactions)
    months, income = chart_manager.getMonthlyIncome()
    _, expense = chart_manager.getMonthlyExpense()
    max_y = max(max(income), max(expense))

    bar_groups = []
    for i, month in enumerate(months):
        bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=income[i],
                        width=20,
                        color=ft.Colors.GREEN,
                        tooltip=f"({month}): {income[i]}",
                        border_radius=2,
                    ),
                    ft.BarChartRod(
                        from_y=0,
                        to_y=expense[i],
                        width=20,
                        color=ft.Colors.RED,
                        tooltip=f"({month}): {expense[i]}",
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
            title=ft.Text("Amount"), 
            title_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i, label=ft.Container(ft.Text(month), padding=10)
                ) for i, month in enumerate(months)
            ],
            labels_size=40,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
        max_y=max_y,
        interactive=True,
        expand=True,
    )

    bar_chart_container.content = chart



