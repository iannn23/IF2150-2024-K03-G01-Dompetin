import flet as ft

def InputFormView(page: ft.Page):
    
    def button_clicked(e):
        t.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb5.value}'."
        page.update()

    t = ft.Text()
    titleJudul = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Judul")])
    tb1 = ft.TextField(label="Judul", read_only=True, hint_text="Masukan judul transaksi")

    titleJumlah = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Jumlah Nominal")])
    tb2 = ft.TextField(label="Jumlah", prefix_text="Rp. ")

    titleCatatan = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Catatan")])
    tb3 = ft.TextField(label="Catatan", read_only=True, hint_text="Masukan catatan tambahan untuk transaksi")

    tb5 = ft.TextField(label="With an icon", icon=ft.Icons.EMOJI_EMOTIONS)
    
    def amenity_selected(e):
        page.update()

    title = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Kategori")])
    amenities = ["Belanja", "Makan", "Hiburan", "Transportasi", "Tagihan", "Penghasilan"]
    amenity_chips = []

    for amenity in amenities:
        amenity_chips.append(
            ft.Chip(
                label=ft.Text(amenity),
                bgcolor=ft.Colors.GREEN_200,
                disabled_color=ft.Colors.GREEN_100,
                autofocus=True,
                on_select=amenity_selected,
            )
        )

    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)

    page.add(titleJudul, tb1, titleJumlah, tb2, title, ft.Row(amenity_chips),titleCatatan,tb3, b,t)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Input Transaksi", size=30),
                tb1,
                tb2,
                ft.Row(amenity_chips),
                tb3,
                b
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
    )