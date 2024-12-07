import flet as ft

class MyButton(ft.ElevatedButton):
    def __init__(self, text, txtcolor, bgcolor):
        super().__init__()
        self.bgcolor = bgcolor
        self.color = txtcolor
        self.text = text
        self.width = 100
        self.height = 50