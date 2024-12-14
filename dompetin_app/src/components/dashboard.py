import flet as ft
from .balance import BalanceController
from datetime import datetime
from .transaksi import TransactionManager

def DashboardView(page: ft.Page):
    """
    Create and return the dashboard view
    
    Args:
        page (ft.Page): The main page object
    
    Returns:
        ft.Container: Dashboard content
    """
    transaction_manager = TransactionManager(page)
    current_date = datetime.now()
    current_month = current_date.strftime("%B")
    balance_controller = BalanceController(page)
    balance = balance_controller.get_balance()
    # display_balance = ft.Text(f"Rp.{balance}"),

    month_income = transaction_manager.getMonthIncome(current_month)
    month_expense = transaction_manager.getMonthExpense(current_month)



    def balance_edit(e):
        def close_dlg(e):
            saldo_dialog.open = False
            e.control.page.update()
        saldo_input = ft.TextField(
            label="Balance",
            prefix_text="Rp. ",
            input_filter=ft.NumbersOnlyInputFilter(),
            width=400,
        )
        saldo_dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Masukkan Saldo Awal", size=14),
                    saldo_input,
                ]),
                width=400,
                height=100,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.ElevatedButton("Save", on_click=lambda e: (balance_controller.set_balance(float(saldo_input.value)), close_dlg(e))),
            ]
        )
        saldo_dialog.open = True
        page.dialog = saldo_dialog
        page.update()


    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Welcome Dompetin App!", size=30,color="#2D60FF"),
                # Add more dashboard widgets here
                ft.Text(f"Your {current_month} financial overview", size=20),
                # Example of additional dashboard elements
                ft.Row([
                    ft.Text("Your current balance: ", size=20, color="#2D60FF"),
                    balance_controller.display_balance(),
                    ft.ElevatedButton(
                                    "Edit",
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.Colors.BLUE_100,
                                    tooltip="Edit Balance",
                                    on_click=lambda e, page=page: balance_edit(e),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        side=ft.BorderSide(color=ft.Colors.BLUE_300, width=2),
                                        shadow_color=ft.Colors.TRANSPARENT,
                                    ),
                                    width=100,
                                ),
                ]),
                ft.Row([
                    ft.Column([
                        ft.Container(
                        content=ft.Text("Monthly Income", size=18),
                        bgcolor=ft.colors.GREEN_100,
                        padding=10,
                        width=200
                    ),
                        ft.Text(f"Rp.{month_income}", size=20, color=ft.colors.GREEN_100),
                    ]),
                ft.Column([
                    ft.Container(
                        content=ft.Text("Monthly Expense", size=18),
                        bgcolor=ft.colors.RED_100,
                        padding=10,
                        width=200
                    ),
                    ft.Text(f"Rp.{month_expense}", size=20, color=ft.colors.RED_100),
                    ]),
                ])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )