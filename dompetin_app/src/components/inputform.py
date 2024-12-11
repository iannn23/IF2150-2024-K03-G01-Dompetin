import flet as ft
import datetime

def InputFormView(page: ft.Page):
    from .transaksi import TransactionManager
    transaction_manager = TransactionManager(page)

    def button_clicked(e):
        from .transaksi import Transaction
        # Validate inputs
        if selected_date.current.value == "No date selected":
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a date."))
            page.snack_bar.open = True
            page.update()
            return

        if not tb1.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a title."))
            page.snack_bar.open = True
            page.update()
            return

        if not tb2.value or not tb2.value.isdigit():
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a valid amount."))
            page.snack_bar.open = True
            page.update()
            return

        if selected_amenity.current is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a category."))
            page.snack_bar.open = True
            page.update()
            return

        if selected_type.current is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a type."))
            page.snack_bar.open = True
            page.update()
            return

        selected_amenity_value = selected_amenity.current.label.value if selected_amenity.current else "None"
        selected_type_value = selected_type.current.label.value if selected_type.current else "None"
        drafttransaction = Transaction(
            title=tb1.value,
            date=selected_date.current.value,
            category=selected_amenity_value,
            amount=float(tb2.value),
            transaction_type=selected_type_value
        )
        transaction_manager.add_transaction(drafttransaction)  # Add transaction to TransactionManager
        t.value = str(drafttransaction)
        page.update()   
    
    selected_date = ft.Ref[ft.Text]()
    def handle_change(e):
        selected_date.current.value = e.control.value.strftime('%Y-%m-%d')
        page.update()
    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    titleDate = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Date")])
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
    titleJudul = ft.Row([ft.Icon(ft.Icons.EDIT), ft.Text("Judul")])
    tb1 = ft.TextField(label="Judul", read_only=False, hint_text="Masukan judul transaksi")

    titleJumlah = ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY), ft.Text("Jumlah Nominal")])
    tb2 = ft.TextField(label="Jumlah", prefix_text="Rp. ", input_filter=ft.NumbersOnlyInputFilter())

    titleCatatan = ft.Row([ft.Icon(ft.Icons.LIGHTBULB), ft.Text("Catatan")])
    tb3 = ft.TextField(label="Catatan", read_only=False, hint_text="Masukan catatan tambahan untuk transaksi")

    # tb5 = ft.TextField(label="With an icon", icon=ft.Icons.EMOJI_EMOTIONS)
    selected_type = ft.Ref[ft.Chip]()
    def type_selected(e):
        for chip in type_chips:
            chip.selected = False
        e.control.selected = True
        selected_type.current = e.control
        page.update()

    titleTipe = ft.Row([ft.Icon(ft.icons.ADD_TO_HOME_SCREEN_ROUNDED), ft.Text("Tipe")])
    types = ["Pengeluaran", "Penghasilan"]
    type_chips = []

    for type in types:
        chip = ft.Chip(
            label=ft.Text(type),
            bgcolor=ft.colors.BLUE_100,
            disabled_color=ft.colors.BLUE_100,
            autofocus=True,
            on_select=type_selected,
        )
        type_chips.append(chip)
        
    selected_amenity = ft.Ref[ft.Chip]()
    def amenity_selected(e):
        for chip in amenity_chips:
            chip.selected = False
        e.control.selected = True
        selected_amenity.current = e.control
        page.update()

    titleKategori = ft.Row([ft.Icon(ft.icons.CATEGORY), ft.Text("Kategori")])
    amenities = ["Belanja", "Makan", "Hiburan", "Transportasi", "Tagihan", "Penghasilan"]
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
                ft.Row(amenity_chips,scroll=ft.ScrollMode.AUTO),
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
