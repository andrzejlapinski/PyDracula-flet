import flet as ft
from components.fletcarousel.horizontal import BasicHorizontalCarousel
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

        # 轮播图项目
        carousel_items = [
            ft.Container(
                content=ft.Text(value=str(i), size=20),
                height=200,
                width=300,
                bgcolor=self.theme_colors.divider_color,
                border_radius=15,
                alignment=ft.alignment.center,
            ) for i in range(10)
        ]

        # 导航按钮
        nav_buttons = [
            ft.FloatingActionButton(
                icon=ft.Icons.NAVIGATE_BEFORE,
                bgcolor=self.theme_colors.divider_color,
            ),
            ft.FloatingActionButton(
                icon=ft.Icons.NAVIGATE_NEXT,
                bgcolor=self.theme_colors.divider_color,
            )
        ]

        carousel = BasicHorizontalCarousel(
            page=self.page,
            items_count=items_count,
            auto_cycle=AutoCycle(duration=5),
            items=carousel_items,
            buttons=nav_buttons,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            items_alignment=ft.MainAxisAlignment.CENTER
        )

        return carousel

    def _build_stats_section(self) -> ft.Container:
        """构建统计信息部分"""
        # 活跃项目卡片
        projects_card = ft.Container(
            content=ft.Column([
                ft.Text("Statistics", color=self.theme_colors.text_color, size=20),
                ft.Text("125", color=self.theme_colors.text_color,
                        size=40, weight="bold"),
                ft.Text("Active Projects",
                        color=self.theme_colors.text_color, size=14),
            ]),
            bgcolor=self.theme_colors.card_color,
            padding=20,
            border_radius=ft.border_radius.all(10),
            width=200,
            height=150,
        )

        # 待办任务卡片
        tasks_card = ft.Container(
            content=ft.Column([
                ft.Text("Tasks", color=self.theme_colors.text_color, size=20),
                ft.Text("42", color=self.theme_colors.text_color,
                        size=40, weight="bold"),
                ft.Text("Pending Tasks",
                        color=self.theme_colors.text_color, size=14),
            ]),
            bgcolor=self.theme_colors.card_color,
            padding=20,
            border_radius=ft.border_radius.all(10),
            width=200,
            height=150,
        )

        stats_row = ft.Row([projects_card, tasks_card], spacing=20)
        container = ft.Container(content=stats_row, padding=20)

        return container

    def _build_actions_section(self) -> ft.Container:
        """构建操作按钮部分"""
        action_buttons = [
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
        ]

        return ft.Container(
            content=ft.Row(action_buttons, spacing=10),
            padding=20,
        )

    def _build_progress_section(self) -> ft.Container:
        """构建进度部分"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Project Progress", size=20,
                        color=self.theme_colors.text_color),
                ft.ProgressBar(
                    width=400,
                    value=0.7,
                    color="blue",
                    bgcolor=self.theme_colors.card_color,
                ),
                ft.Text("70% Completed", size=14,
                        color=self.theme_colors.text_color),
            ], spacing=10),
            padding=20,
        )

    def _build_activities_section(self) -> ft.Container:
        """构建活动列表部分"""
        activities = [
            ("Team Meeting", "10:00 AM", ft.Icons.CALENDAR_MONTH),
            ("Project Review", "2:30 PM", ft.Icons.WORK),
            ("Client Meeting", "4:00 PM", ft.Icons.PERSON),
        ]

        activity_items = [
            ft.ListTile(
                leading=ft.Icon(icon),
                title=ft.Text(title, color=self.theme_colors.text_color),
                subtitle=ft.Text(time, color=self.theme_colors.text_color),
            ) for title, time, icon in activities
        ]

        activities_list = ft.Container(
            content=ft.Column(activity_items),
            bgcolor=self.theme_colors.card_color,
            border_radius=ft.border_radius.all(10),
            padding=10,
        )

        title = ft.Text("Recent Activities", size=20,
                        color=self.theme_colors.text_color)
        content = ft.Column([title, activities_list], spacing=10)
        container = ft.Container(content=content, padding=20)

        return container

    def build_content(self) -> ft.Column:
        """构建页面内容"""
        container = ft.Container(
            content=ft.Column([
                self._build_carousel(),
                self._build_stats_section(),
                self.build_section("", self._build_actions_section()),
                self._build_progress_section(),
                self._build_activities_section(),
            ], scroll="auto", spacing=0),
            bgcolor=self.theme_colors.bg_color,
        )
        return container
