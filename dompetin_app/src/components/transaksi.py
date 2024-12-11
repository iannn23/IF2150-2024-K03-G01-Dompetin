import flet as ft
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List
import json
import random
from .inputform import InputFormView

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
        # Load transaksi dari client storage
        self.transactions: List[Transaction] = self._load_transactions()
        if not self.transactions:  # Generate demo data jika kosong
            self._generate_demo_data()

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
        titles = ["Jajan Kenan", "Gaji Kenan", "Cabut gigi ian", "Ian CheckIn", "Ian beli Kondom"]
        categories = ["Food & Drinks","Sex","Transportation"]
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
        self._generate_demo_data()




def TransactionView(page: ft.Page):
    transaction_manager = TransactionManager(page)
    # transaction_manager.reset_transactions()
    def handle_edit(transaction, selected_month):
        # Open a dialog or a form for editing
        dialog = ft.AlertDialog(
            title=ft.Text("Edit Transaction"),
            content=ft.Column(
                [
                    ft.TextField(value=transaction_manager.description, label="Description", width=400),
                    ft.TextField(value=str(transaction_manager.amount), label="Amount", width=400),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("income", "Income"),
                            ft.dropdown.Option("expense", "Expense"),
                        ],
                        value=transaction_manager.transaction_type,
                        label="Transaction Type",
                    ),
                ],
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: dialog.close()),
                ft.ElevatedButton(
                    "Save",
                    on_click=lambda e: transaction_manager._save_transaction_changes(e, transaction, dialog),
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

            # Refresh transaction list for the selected month
            handle_month_click(None, selected_month)


    # Create transaction manager instanc
    transaction_manager = TransactionManager(page)

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
        transactions_per_page = 6  # Set the number of transactions per page
        total_pages = (len(transactions) + transactions_per_page - 1) // transactions_per_page
        current_page = [1]  # Use a list to make it mutable inside nested functions

        def update_transaction_list():
            start_idx = (current_page[0] - 1) * transactions_per_page
            end_idx = start_idx + transactions_per_page
            transaction_items = [
    ft.Container(
        content=ft.ListTile(
            content_padding=ft.Padding(10, 10, 10, 10),
            shape=ft.RoundedRectangleBorder(radius=5),
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
                        f"{'+ ' if t.transaction_type == 'income' else '- '}${t.amount:.2f}",
                        color="green" if t.transaction_type == "income" else "red",
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color="red",
                        tooltip="Delete Transaction",
                        on_click=lambda e, t=t: handle_delete(t, selected_month),
                        style=ft.ButtonStyle(padding=ft.Padding(5, 5, 5, 5)),
                    ),
                ]
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