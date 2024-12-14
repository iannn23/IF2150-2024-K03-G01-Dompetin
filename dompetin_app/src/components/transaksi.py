import flet as ft
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import List
import json
import random
from .inputform import InputFormView
from .balance import BalanceController

@dataclass
class Transaction:
    title: str
    date: str
    category: str
    amount: float
    transaction_type: str


class TransactionManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.balance_controller = BalanceController(page)
        # Load transaksi dari client storage
        self.transactions: List[Transaction] = self._load_transactions()

    def _load_transactions(self) -> List[Transaction]:
        """Load transaksi dari client storage."""
        transactions_data = self.page.client_storage.get("transactions")
        if transactions_data:
            return [Transaction(**t) for t in json.loads(transactions_data)]
        return []

    def _save_transactions(self):
        """Simpan transaksi ke client storage."""
        self.page.client_storage.set(
            "transactions",
            json.dumps([asdict(t) for t in self.transactions])
        )

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self._save_transactions()

    def get_transactions(self, month: str) -> List[Transaction]:
        """Ambil transaksi berdasarkan bulan."""
        return [
            t for t in self.transactions
            if datetime.strptime(t.date, "%Y-%m-%d").strftime("%B").lower() == month.lower()
        ]

    def _generate_demo_data(self):
        """Generate transaksi dummy untuk demo."""
        titles = ["Jajan Kenan", "Gaji Kenan", "Cabut gigi ian", "Ian CheckIn", "Ian beli Makan"]
        categories = ["Belanja", "Makan", "Transportasi", "Hiburan", "Tagihan"]
        for i in range(1, 13):
            for _ in range(random.randint(5, 10)):
                day = random.randint(1, 28)
                title= random.choice(titles)
                amount = round(random.uniform(10, 1000), 2)
                trans_type = "income" if title == "Gaji Kenan" else "expense"
                date = f"2024-{i:02d}-{day:02d}"
                category = random.choice(categories)
                self.add_transaction(Transaction(title, date, category, amount, trans_type))

    def reset_transactions(self):
        """Reset transactions in client storage."""
        self.transactions = []
        self._save_transactions()
    
    def save_transaction_changes(self, transaction: Transaction, dialog: ft.AlertDialog):
        """Save changes to a transaction."""

        original_amount = transaction.amount
        if transaction.transaction_type == 'income':
            self.balance_controller.decrease_balance(original_amount)
        else:
            self.balance_controller.increase_balance(original_amount)
        # Access the Column's controls to extract values
        column_controls = dialog.content.content.controls

        transaction.title = column_controls[0].value  # First TextField: Title
        transaction.amount = float(column_controls[1].value)  # Second TextField: Amount
        transaction.transaction_type = column_controls[2].value  # First Dropdown: Transaction Type
        transaction.date = column_controls[3].value.strftime("%Y-%m-%d")  # DatePicker value
        transaction.category = column_controls[4].value  # Second Dropdown: Category

        if transaction.transaction_type == 'income':
            self.balance_controller.increase_balance(transaction.amount)
        else:
            self.balance_controller.decrease_balance(transaction.amount)

        self._save_transactions()  # Save changes to client storage
        dialog.open = False  # Close the dialog
        self.page.update()

    def getMonthIncome(self, month: str):
        income = sum(
            t.amount for t in self.transactions
            if t.transaction_type == "income" and datetime.strptime(t.date, "%Y-%m-%d").month == int(month)
        )
        return income

    def getMonthExpense(self, month: str):
        expense = sum(
            t.amount for t in self.transactions
            if t.transaction_type == "expense" and datetime.strptime(t.date, "%Y-%m-%d").month == int(month)
        )
        return expense
        




def TransactionView(page: ft.Page):
    balance_controller = BalanceController(page)  # Initialize BalanceController
    transaction_manager = TransactionManager(page)
    # transaction_manager.reset_transactions()
    def handle_edit(transaction: Transaction, selected_month: str):
        def close_dlg(e):
            dialog.open = False
            e.control.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Transaction"),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.TextField(value=transaction.title, label="Title", width=400),
                        ft.TextField(label="Amount",value= transaction.amount, width=400, read_only=False ,prefix_text="Rp. ", input_filter=ft.NumbersOnlyInputFilter()),
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option("income", "Income"),
                                ft.dropdown.Option("expense", "Expense"),
                            ],
                            value=transaction.transaction_type,
                            label="Transaction Type",
                        ),
                        ft.DatePicker(
                            first_date=datetime(year=2023, month=1, day=1),
                            last_date=datetime(year=2024, month=12, day=31),
                            value=datetime.strptime(transaction.date, "%Y-%m-%d"),
                        ),
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option("Belanja", "Belanja"),
                                ft.dropdown.Option("Makan", "Makan"),
                                ft.dropdown.Option("Transportasi", "Transportasi"),
                                ft.dropdown.Option("Hiburan", "Hiburan"), 
                                ft.dropdown.Option("Tagihan", "Tagihan"),
                            ],
                            value=transaction.category,
                            label="Category",
                        ),
                    ],
                    spacing=10,
                ),
                width=600,
                height=500,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dlg),
                ft.ElevatedButton(
                    "Save",
                    on_click=lambda e: (transaction_manager.save_transaction_changes(transaction, dialog)),
                ),
                ft.ElevatedButton(
                    "Delete",
                    on_click=lambda e: (delete_confirmation(transaction, selected_month),close_dlg(e)),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_100,
                    ),
                ),
            ],
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    
    def delete_confirmation(transaction: Transaction, selected_month: str):
        dialog = ft.AlertDialog(
            title=ft.Text("Delete Transaction"),
            content=ft.Text("Are you sure you want to delete this transaction?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: close_dialog()),
                ft.ElevatedButton(
                    "Delete",
                    on_click=lambda e: (handle_delete(transaction, selected_month), close_dialog()),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_100,
                    ),
                ),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()


    def handle_delete(transaction: Transaction, selected_month: str):
            # Delete transaction and update storage
            transaction_manager.transactions.remove(transaction)
            transaction_manager._save_transactions()
            if transaction.transaction_type == 'income':
                transaction_manager.balance_controller.decrease_balance(transaction.amount)
            else:
                transaction_manager.balance_controller.increase_balance(transaction.amount)

            # Refresh transaction list for the selected month
            handle_month_click(None, selected_month)

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    content = ft.Column(
        [
            ft.Text("Select a month to view transactions", size=20)
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10
    )

    def handle_month_click(e, selected_month):
        transactions = transaction_manager.get_transactions(selected_month)
        transactions_per_page = 5  # Set the number of transactions per page
        total_pages = (len(transactions) + transactions_per_page - 1) // transactions_per_page
        current_page = [1]  # Use a list to make it mutable inside nested functions

        def update_transaction_list():
            start_idx = (current_page[0] - 1) * transactions_per_page
            end_idx = start_idx + transactions_per_page
            transaction_items = [
                ft.Container(
                    content=ft.ListTile(
                        content_padding=ft.Padding(10, 15, 10, 25),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        bgcolor=ft.Colors.WHITE,
                        leading=ft.Icon(
                            name=ft.icons.ARROW_UPWARD if t.transaction_type == "income" else ft.icons.ARROW_DOWNWARD,
                            color="green" if t.transaction_type == "income" else "red",
                        ),
                        title=ft.Text(t.title),
                        subtitle=ft.Text(t.date),
                        trailing=ft.Column(
                            [
                                ft.Text(
                                    f"{'+ ' if t.transaction_type == 'income' else '- '}Rp. {'{:,.2f}'.format(t.amount).replace(',', 'X').replace('.', ',').replace('X', '.')}",
                                    color="green" if t.transaction_type == "income" else "red",
                                    size=18,
                                ),
                                ft.ElevatedButton(
                                    "Edit",
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.Colors.BLUE_100,
                                    tooltip="Edit Transaction",
                                    on_click=lambda e, t=t: handle_edit(t, selected_month),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        side=ft.BorderSide(color=ft.Colors.BLUE_300, width=2),
                                        shadow_color=ft.Colors.TRANSPARENT,
                                    ),
                                    width=120,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    margin=ft.Margin(0, 0, 0, 10),  # Adds a gap of 10 pixels between tiles
                )
                for idx, t in enumerate(transactions[start_idx:end_idx])
            ]

            content.controls = [
                ft.Row(
                    [
                    ft.Text(f"Transactions for {selected_month} (Page {current_page[0]} of {total_pages})", size=24),
                    ft.Container(
                        content=add_transaction_button,
                        alignment=ft.alignment.bottom_right,
                        padding=ft.padding.all(16)
                ),
                    ]
                ),
                ft.ListView(controls=transaction_items, expand=1) if transaction_items else ft.Text("No transactions found"),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Previous",
                            on_click=lambda e: navigate(-1),
                            disabled=current_page[0] <= 1,
                        ),
                        ft.ElevatedButton(
                            text="Next",
                            on_click=lambda e: navigate(1),
                            disabled=current_page[0] >= total_pages,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
            page.update()

        def navigate(direction):
            current_page[0] += direction
            update_transaction_list()

        update_transaction_list()


    month_buttons = [
        ft.TextButton(
            text=month,
            on_click=lambda e, m=month: handle_month_click(e, m.lower()),
            style=ft.ButtonStyle(
                bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50}
            )
        ) for month in months
    ]

    menubar = ft.Row(
        controls=month_buttons,
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    def open_input_form(e):
            page.dialog = ft.AlertDialog(
                content=ft.Container(
                    content=InputFormView(page),
                    width=600,  # Set the width of the container
                    height=800,
                ),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog())
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog.open = True
            page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    add_transaction_button = ft.IconButton(
        icon=ft.icons.ADD,
        on_click=open_input_form,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=7),  # Set the shape to rectangle
            bgcolor=ft.colors.BLUE_100,
        
        )
    )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text("Transactions", size=30, color="#2D60FF"),
                    padding=ft.padding.only(left=20, top=20)
                ),
                
                ft.Container(
                    content=menubar,
                    padding=ft.Padding(0, 0, 0, 0)  # Adjust padding to move menubar closer to the top
                ),
                
                content, 
                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        expand=True,
    )