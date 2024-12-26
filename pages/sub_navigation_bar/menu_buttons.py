import flet as ft
from core.base_page import BasePage

class MenuButtonsPage(BasePage):
    """菜单按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="菜单按钮", **kwargs)
        
    def build_content(self) -> ft.Control:
        return ft.Column([
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.PopupMenuButton(
                        icon=ft.Icons.MENU,
                        items=[
                            ft.PopupMenuItem(text="选项 1"),
                            ft.PopupMenuItem(text="选项 2"),
                            ft.PopupMenuItem(text="选项 3"),
                        ],
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="设置",
                                icon=ft.Icons.SETTINGS,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                text="删除",
                                icon=ft.Icons.DELETE,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.PopupMenuButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                                    ft.Text("更多选项"),
                                ],
                            ),
                            items=[
                                ft.PopupMenuItem(text="子选项 1"),
                                ft.PopupMenuItem(text="子选项 2"),
                            ],
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=ft.border_radius.all(4),
                        padding=ft.padding.all(8),
                    ),
                ],
                spacing=10,
            ),
        ]) 