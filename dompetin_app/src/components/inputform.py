import flet as ft
import datetime
from .balance import BalanceController

def InputFormView(page: ft.Page):
    from .transaksi import TransactionManager  # Local import to avoid circular import

    transaction_manager = TransactionManager(page)
    Balance_controller = BalanceController(page)

    def button_clicked(e):
<<<<<<< HEAD
        from .transaksi import Transaction  # Local import to avoid circular import

=======
        from .transaksi import Transaction

        
>>>>>>> 1b8f02242eb2f90f9a9bd1e61dd16cf2c1dd31c1
        # Validate inputs

        if selected_type.current is None:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Please select transaction type."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
            def close_dlg(e):
                dialog.open = False
                e.control.page.update()
            page.open(dialog)
            return

        if selected_date.current.value == "No date selected":
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Please select a date."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
            def close_dlg(e):
                dialog.open = False
                e.control.page.update()
            page.open(dialog)
            return

        if not tb1.value:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Please fill the Title."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
            def close_dlg(e):
                dialog.open = False
                e.control.page.update()
            page.open(dialog)
            return

        if not tb2.value or not tb2.value.isdigit():
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Please fill a valid amount."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
            def close_dlg(e):
                dialog.open = False
                e.control.page.update()
            page.open(dialog)
            return

<<<<<<< HEAD
        if selected_amenity.current is None and selected_type.current.label.value == "Pengeluaran":
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a category."))
            page.snack_bar.open = True
            page.update()
            return

        if selected_type.current is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a type."))
            page.snack_bar.open = True
            page.update()
            return
        
        # If all inputs are valid, create a transaction
        selected_amenity_value = selected_amenity.current.label.value if selected_amenity.current else "None"
        selected_type_value = selected_type.current.label.value if selected_type.current else "None"
        transaction = Transaction(
=======
        if selected_amenity.current is None:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Please select a category."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
            def close_dlg(e):
                dialog.open = False
                e.control.page.update()
            page.open(dialog)
            return

        

        selected_amenity_value = selected_amenity.current.label.value if selected_amenity.current else "None"
        if selected_type.current.label.value == "Pengeluaran":
            selected_type_value = "expense"
        elif selected_type.current.label.value == "Penghasilan":
            selected_type_value = "income"
        else:
            selected_type_value = "None"

        drafttransaction = Transaction(
>>>>>>> 1b8f02242eb2f90f9a9bd1e61dd16cf2c1dd31c1
            title=tb1.value,
            date=selected_date.current.value,
            category=selected_amenity_value,
            amount=float(tb2.value),
            transaction_type=selected_type_value
        )
<<<<<<< HEAD
        transaction_manager.add_transaction(transaction)  # Add transaction to TransactionManager
        t.value = str(transaction)
        page.update()   

=======
        transaction_manager.add_transaction(drafttransaction)  # Add transaction to TransactionManager
        if selected_type_value == "expense":
            Balance_controller.decrease_balance(float(tb2.value))
        elif selected_type_value == "income":
            Balance_controller.increase_balance(float(tb2.value))
        t.value = str(drafttransaction)
        dialog = ft.AlertDialog(
                title=ft.Text("Message"),
                content=ft.Text("Transaction Added."),
                actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(e))],
            )
        def close_dlg(e):
            dialog.open = False
            e.control.page.update()

        page.open(dialog)
    
>>>>>>> 1b8f02242eb2f90f9a9bd1e61dd16cf2c1dd31c1
    selected_date = ft.Ref[ft.Text]()
    def handle_change(e):
        selected_date.current.value = e.control.value.strftime('%Y-%m-%d')
        page.update()
    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    titleDate = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Date")])
    date_picker_button = ft.IconButton(
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        ),
    )
    selected_date_display = ft.Text(ref=selected_date, value="No date selected")

    t = ft.Text()
    titleJudul = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Judul")])
    tb1 = ft.TextField(label="Judul", read_only=False, hint_text="Masukan judul transaksi")

    titleJumlah = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Jumlah Nominal")])
    tb2 = ft.TextField(label="Jumlah", prefix_text="Rp. ", input_filter=ft.NumbersOnlyInputFilter())

    titleCatatan = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Catatan")])
    tb3 = ft.TextField(label="Catatan", read_only=False, hint_text="Masukan catatan tambahan untuk transaksi")
    
    titleKategori = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Kategori")], opacity=0, height=0)
    amenity_chips = ft.Row(scroll=ft.ScrollMode.AUTO, opacity=0, height=0)

    selected_amenity = ft.Ref[ft.Chip]()
    def amenity_selected(e):
        for chip in amenity_chips.controls:
            chip.selected = False
        e.control.selected = True
        selected_amenity.current = e.control
        page.update()

    def update_categories(transaction_type):
        if transaction_type == "Pengeluaran":
            amenities = ["Belanja", "Makan", "Hiburan", "Transportasi", "Tagihan"]
            titleKategori.opacity = 1
            titleKategori.height = None
            amenity_chips.opacity = 1
            amenity_chips.height = None
        elif transaction_type == "Penghasilan":
            amenities = ["Income"]
            titleKategori.opacity = 0
            titleKategori.height = 0
            amenity_chips.opacity = 0
            amenity_chips.height = 0
            selected_amenity.current = ft.Chip(label=ft.Text("Income"))

        amenity_chips.controls.clear()
        for amenity in amenities:
            chip = ft.Chip(
                label=ft.Text(amenity),
                bgcolor=ft.colors.BLUE_200,
                disabled_color=ft.colors.BLUE_100,
                autofocus=True,
                on_select=amenity_selected,
            )
            amenity_chips.controls.append(chip)
        page.update()

    titleTipe = ft.Row([ft.Icon(ft.icons.HOTEL_CLASS), ft.Text("Tipe")])
    types = ["Pengeluaran", "Penghasilan"]
    type_chips = []

    selected_type = ft.Ref[ft.Chip]()
    def type_selected(e):
        for chip in type_chips:
            chip.selected = False
        e.control.selected = True
        selected_type.current = e.control
        update_categories(selected_type.current.label.value)
        page.update()
    for type in types:
        chip = ft.Chip(
            label=ft.Text(type),
            bgcolor=ft.colors.BLUE_200,
            disabled_color=ft.colors.BLUE_100,
            autofocus=True,
            on_select=type_selected,
        )
        type_chips.append(chip)

<<<<<<< HEAD
=======
    titleKategori = ft.Row([ft.Icon(ft.icons.CATEGORY), ft.Text("Kategori")])
    amenities = ["Belanja", "Makan", "Hiburan", "Transportasi", "Tagihan"]
    amenity_chips = []

    for amenity in amenities:
        chip = ft.Chip(
            label=ft.Text(amenity),
            bgcolor=ft.colors.BLUE_100,
            disabled_color=ft.colors.GREEN_100,
            autofocus=True,
            on_select=amenity_selected,
        )
        amenity_chips.append(chip)
>>>>>>> 1b8f02242eb2f90f9a9bd1e61dd16cf2c1dd31c1

    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)

    return ft.Container(
        content=ft.ListView( 
            controls=[
                ft.Text("Input Transaksi", size=30),
                titleTipe,
                ft.Row(type_chips),
                titleDate,
                ft.Row([date_picker_button, selected_date_display], alignment=ft.MainAxisAlignment.START),
                titleJudul,
                tb1,
                titleJumlah,
                tb2,
                titleKategori,
                amenity_chips,  # Use the updated amenity_chips container
                titleCatatan,
                tb3,
                b,
                t
            ],
            expand=1, spacing=10, padding=20, auto_scroll=True
        ),
        alignment=ft.alignment.center,
        expand=True,
    )