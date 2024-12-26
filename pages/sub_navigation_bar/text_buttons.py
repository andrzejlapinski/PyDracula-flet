import flet as ft
from core.base_page import BasePage

class TextButtonsPage(BasePage):
    """文本按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="文本按钮", **kwargs)
        
    def build_content(self) -> ft.Control:
        return ft.Column([
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.TextButton(text="基本文本按钮"),
                    ft.TextButton(
                        text="带图标",
                        icon=ft.Icons.INFO,
                    ),
                    ft.TextButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        ]) 