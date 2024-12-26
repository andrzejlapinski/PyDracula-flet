import flet as ft
from core.base_page import BasePage
from . import FloatingButtonsPage, OutlinedButtonsPage, TextButtonsPage, IconButtonsPage, MenuButtonsPage, SegmentedButtonsPage, FilledButtonsPage


class SubNavigationBar(BasePage):
    """子导航栏示例"""

    def __init__(self, **kwargs):
        # 设置为有子导航栏
        self.has_sub_nav = True
        super().__init__(title="子导航栏示例", has_sub_nav=self.has_sub_nav, **kwargs)

    def build_content(self) -> ft.Control:
        """构建页面内容"""
        # 定义子页面
        self._pages = [
            {"icon": ft.Icons.RECTANGLE, "label": "填充按钮", "page_class": FilledButtonsPage},
            {"icon": ft.Icons.ADD, "label": "浮动按钮", "page_class": FloatingButtonsPage},
            {"icon": ft.Icons.RECTANGLE, "label": "轮廓按钮", "page_class": OutlinedButtonsPage},
            {"icon": ft.Icons.TEXT_FIELDS, "label": "文本按钮", "page_class": TextButtonsPage},
            {"icon": ft.Icons.STAR, "label": "图标按钮", "page_class": IconButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮", "page_class": MenuButtonsPage},
            # 测试子导航栏滚动
            {"icon": ft.Icons.MENU, "label": "菜单按钮2", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮3", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮4", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮5", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮6", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮7", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮8", "page_class": MenuButtonsPage},
            {"icon": ft.Icons.MENU, "label": "菜单按钮9", "page_class": MenuButtonsPage},
        ]

        # 初始化页面实例
        self._page_instances = {}
        for page_info in self._pages:
            self._page_instances[page_info["label"]] = page_info["page_class"](
                theme_colors=self.theme_colors,
                theme_mode=self.theme_mode,
                page=self.page,  # 使用从父类继承的 page 实例
            )

        # 设置当前页面
        self.current_page = list(self._page_instances.values())[0]

        # 构建子导航栏
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type="all",
            min_width=60,
            # min_extended_width=100,
            bgcolor=self.theme_colors.sub_nav_color,
            destinations=[
                ft.NavigationRailDestination(
                    icon=page_info["icon"],
                    selected_icon=page_info["icon"],
                    label=page_info["label"],
                )
                for page_info in self._pages
            ],
            on_change=self._handle_nav_change,
            height=len(self._pages) * 50 if len(self._pages) * 50 > self.page.height else self.page.height,
        )

        # 将导航栏包装在可滚动容器中
        nav_container = ft.Container(
            content=ft.Column(
                [self.nav_rail],
                scroll="auto",  # 使导航栏可滚动
                alignment="start",
            ),
            bgcolor=self.theme_colors.sub_nav_color,
            border=ft.border.only(right=ft.BorderSide(1, self.theme_colors.divider_color)),
            padding=0,
        )

        # 构建内容区域
        self.content_area = ft.Container(
            content=self.current_page.build_content(),
            expand=True,
            padding=ft.padding.only(left=5),
        )

        # 构建布局
        return ft.Row(
            controls=[
                # 子导航容器
                nav_container,
                # 内容区域
                self.content_area,
            ],
            expand=True,
        )

    def _handle_nav_change(self, e):
        """处理子导航切换事件"""
        if not e.control or not hasattr(self, '_pages'):
            return
            
        selected_index = e.control.selected_index
        selected_label = self._pages[selected_index]["label"]

        # 更新当前页面
        self.current_page = self._page_instances[selected_label]

        # 更新内容区域
        if hasattr(self, 'content_area'):
            self.content_area.content = self.current_page.build_content()
            self.page.update()
