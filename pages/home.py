import flet as ft
from components.fletcarousel.horizontal import  BasicHorizontalCarousel
from components.fletcarousel.attributes import AutoCycle
from core.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, **kwargs):
        self.images = [
            "banner1.jpg",
            "banner2.jpg",
            "banner3.jpg",
        ]
        super().__init__(title="主页", **kwargs)

    def _build_carousel(self) -> ft.Container:
        """构建轮播图"""
        # 根据窗口的大小来修改轮播图显示的数量
        items_count = 4 if self.page.width > 800 else 3
        return BasicHorizontalCarousel(
            page=self.page,
            items_count=items_count,
            auto_cycle=AutoCycle(duration=5),
            items=[
                ft.Container(
                    content=ft.Text(value=str(i), size=20),
                    height=200,
                    width=300,
                    bgcolor=self.theme_colors.card_color,
                    border_radius=15,
                    alignment=ft.alignment.center,
                ) for i in range(10)
            ],
            buttons=[
                ft.FloatingActionButton(
                    icon=ft.Icons.NAVIGATE_BEFORE,
                    bgcolor=self.theme_colors.divider_color,
                ),
                ft.FloatingActionButton(
                    icon=ft.Icons.NAVIGATE_NEXT,
                    bgcolor=self.theme_colors.divider_color,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            items_alignment=ft.MainAxisAlignment.CENTER
        )

    def build_content(self) -> ft.Column:
        return ft.Column(
            controls=[
                self._build_carousel(),  # 添加轮播图
                self._build_stats_section(),
                self._build_actions_section(),
                self._build_progress_section(),
                self._build_activities_section(),
            ],
            scroll="auto",
            spacing=0,
        )

    def _build_stats_section(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Statistics", color=self.theme_colors.text_color, size=20),
                            ft.Text("125", color=self.theme_colors.text_color, size=40, weight="bold"),
                            ft.Text("Active Projects", color=self.theme_colors.text_color, size=14),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        padding=20,
                        border_radius=ft.border_radius.all(10),
                        width=200,
                        height=150,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tasks", color=self.theme_colors.text_color, size=20),
                            ft.Text("42", color=self.theme_colors.text_color, size=40, weight="bold"),
                            ft.Text("Pending Tasks", color=self.theme_colors.text_color, size=14),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        padding=20,
                        border_radius=ft.border_radius.all(10),
                        width=200,
                        height=150,
                    ),
                ],
                spacing=20,
            ),
            padding=20,
        )

    def _build_actions_section(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE,
                        icon_color=self.theme_colors.text_color,
                        icon_size=30,
                        tooltip="Add New",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE,
                        icon_color="red",
                        icon_size=30,
                        tooltip="Favorite",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SHARE,
                        icon_color=self.theme_colors.text_color,
                        icon_size=30,
                        tooltip="Share",
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )

    def _build_progress_section(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Project Progress", size=20, color=self.theme_colors.text_color),
                    ft.ProgressBar(
                        width=400,
                        value=0.7,
                        color="blue",
                        bgcolor=self.theme_colors.card_color,
                    ),
                    ft.Text("70% Completed", size=14, color=self.theme_colors.text_color),
                ],
                spacing=10,
            ),
            padding=20,
        )

    def _build_activities_section(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Recent Activities", size=20, color=self.theme_colors.text_color),
                    ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.CALENDAR_MONTH),
                                title=ft.Text("Team Meeting", color=self.theme_colors.text_color),
                                subtitle=ft.Text("10:00 AM", color=self.theme_colors.text_color),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.WORK),
                                title=ft.Text("Project Review", color=self.theme_colors.text_color),
                                subtitle=ft.Text("2:30 PM", color=self.theme_colors.text_color),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PERSON),
                                title=ft.Text("Client Meeting", color=self.theme_colors.text_color),
                                subtitle=ft.Text("4:00 PM", color=self.theme_colors.text_color),
                            ),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        border_radius=ft.border_radius.all(10),
                        padding=10,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )