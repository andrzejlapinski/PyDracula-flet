import flet as ft
from core.base_page import BasePage

class OutlinedButtonsPage(BasePage):
    """轮廓按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="轮廓按钮", **kwargs)
        
    def build_content(self) -> ft.Control:
        return ft.Column([
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.OutlinedButton(text="基本轮廓按钮"),
                    ft.OutlinedButton(
                        text="带图标",
                        icon=ft.Icons.SETTINGS,
                    ),
                    ft.OutlinedButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        ]) 