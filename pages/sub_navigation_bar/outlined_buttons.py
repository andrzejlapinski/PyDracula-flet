import flet as ft
from core.base_page import BasePage

class OutlinedButtonsPage(BasePage):
    """轮廓按钮示例页面"""
    
    def __init__(self, **kwargs):
        super().__init__(title="轮廓按钮", **kwargs)
        
    def show_img_dialog(self, e):
        # self.image_dialog.open = True
        self.page.open(self.image_dialog)
        
    def build_content(self) -> ft.Control:
        self.image_dialog = ft.AlertDialog(
            content=ft.Image(
                src="/images/screenshot1.png",
                width=800,
                fit=ft.ImageFit.CONTAIN,
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
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
            ft.Container(height=20),
            self.build_section(
                "图片展示", 
                ft.Container(
                    content=ft.Image(
                        src="/images/screenshot1.png",
                        width=600,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    on_click=self.show_img_dialog,
                    ink=True,  # 添加点击效果
                    tooltip="点击查看大图",  # 添加提示文本
                ),
            ),
        ]) 