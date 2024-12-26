import flet as ft
from core.base_page import BasePage

class IconButtonsPage(BasePage):
    """图标按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="图标按钮", **kwargs)
        
    def build_content(self) -> ft.Control:
        return ft.Column([
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE_BORDER,
                        icon_color="red",
                        icon_size=30,
                        tooltip="收藏",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SHARE,
                        icon_size=30,
                        tooltip="分享",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=30,
                        tooltip="删除",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        ]) 