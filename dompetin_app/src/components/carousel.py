import flet as ft
from fletcarousel import BasicAnimatedHorizontalCarousel, HintLine, AutoCycle

# Fungsi membuat Carousel
def create_carousel(page: ft.Page, charts: list):
    carousel = BasicAnimatedHorizontalCarousel(
        page=page,
        expand=True,
        height=600,
        padding=50,
        hint_lines=HintLine(
            active_color="blue",
            inactive_color="grey",
            alignment=ft.MainAxisAlignment.CENTER,
            max_list_size=400,
        ),
        items=charts,  
        animated_switcher=ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=300,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            content=ft.Container(),
        ),
    )
    return carousel

# Fungsi meng-update carousel
def update_carousel(carousel_container: ft.Container, page: ft.Page, charts: list):
    carousel_container.content = None
    new_carousel = create_carousel(page, charts)
    carousel_container.content = new_carousel
    carousel_container.update()
