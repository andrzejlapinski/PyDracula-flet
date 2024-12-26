import flet as ft
from core.base_page import BasePage


class FilledButtonsPage(BasePage):
    """填充按钮示例页面"""

    def __init__(self, **kwargs):
        super().__init__(title="填充按钮", **kwargs)

    def _build_activities_section(self) -> ft.Container:
        """构建活动列表部分"""
        activities = [
            ("Team Meeting", "10:00 AM", ft.Icons.CALENDAR_MONTH),
            ("Project Review", "2:30 PM", ft.Icons.WORK),
            ("Client Meeting", "4:00 PM", ft.Icons.PERSON),
        ]

        activity_items = [
            ft.ListTile(
                leading=ft.Icon(icon, color=self.theme_colors.text_color),
                title=ft.Text(title, color=self.theme_colors.text_color),
                subtitle=ft.Text(time, color=self.theme_colors.text_color),
            ) for title, time, icon in activities
        ]

        return ft.Container(
            content=ft.Column([
                ft.Text("Recent Activities", size=20, color=self.theme_colors.text_color),
                ft.Container(
                    content=ft.Column(activity_items),
                    bgcolor=self.theme_colors.card_color,
                    border_radius=ft.border_radius.all(10),
                    padding=10,
                )
            ], 
            spacing=10),
            padding=20,
            bgcolor=self.theme_colors.bg_color,
        )
    
    def build_content(self) -> ft.Control:
        # 创建基本按钮行
        button_row = ft.Row(
            controls=[
                ft.FilledButton(text="基本按钮"),
                ft.FilledButton(
                    text="带图标的按钮",
                    icon=ft.Icons.ADD,
                ),
                ft.FilledButton(
                    text="禁用按钮",
                    disabled=True,
                ),
            ],
            spacing=10,
        )

        # 创建按钮示例部分
        buttons_section = self.build_section(
            "填充按钮示例",
            ft.Column([button_row], spacing=10),
            expand=True,
        )

        # 创建活动列表部分
        activities_section = self.build_section(
            "活动列表示例",
            self._build_activities_section(),
            expand=True,
        )

        # 将所有部分放入一个可滚动的列中
        return ft.Column(
            controls=[
                buttons_section,
                activities_section,
            ],
            scroll="auto",
            expand=True,
            spacing=20,
        )
