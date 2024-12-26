import flet as ft
from core.base_page import BasePage

class SegmentedButtonsPage(BasePage):
    """分段按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="分段按钮", **kwargs)
        
    def build_content(self) -> ft.Control:
        return ft.Column([
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    text="日",
                                    icon=ft.Icons.CALENDAR_VIEW_DAY,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                                ft.OutlinedButton(
                                    text="周",
                                    icon=ft.Icons.CALENDAR_VIEW_WEEK,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                                ft.OutlinedButton(
                                    text="月",
                                    icon=ft.Icons.CALENDAR_VIEW_MONTH,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                            ],
                            spacing=0,
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=ft.border_radius.all(4),
                    ),
                ],
                spacing=10,
            ),
        ]) 