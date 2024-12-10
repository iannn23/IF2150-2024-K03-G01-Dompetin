import flet as ft
from fletcarousel import BasicAnimatedHorizontalCarousel, HintLine, AutoCycle

def create_carousel(page: ft.Page, charts: list):
    carousel = BasicAnimatedHorizontalCarousel(
        page=page,
        auto_cycle=AutoCycle(7),
        expand=True,
        padding=50,
        hint_lines=HintLine(
            active_color="red",
            inactive_color="purple",
            alignment=ft.MainAxisAlignment.CENTER,
            max_list_size=400,
        ),
        items=charts,  
        animated_switcher=ft.AnimatedSwitcher(
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=500,
            reverse_duration=500,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_OUT,
            content=ft.Container(),
        ),
    )
    return carousel