import flet as ft
from typing import Callable, Dict, Any, List
from .theme import ThemeColors
from .base_page import BasePage


class AppConfig:
    def __init__(self):
        self.app_title: str = "PyDracula"
        self.theme_mode: str = "dark"
        self.window_width: int = 1300
        self.window_height: int = 800
        self.window_min_width: int = 500
        self.window_min_height: int = 400
        self.nav_rail_extended: bool = True


class NavRail:
    """导航栏类，用于构建应用程序的导航栏。"""

    def __init__(
        self,
        nav_items: List[Dict],
        theme_colors,
        is_extended: bool = True,
        on_change: Callable = None,
        on_toggle: Callable = None,
        selected_index: int = 0,
        app_title: str = "",
    ):
        """初始化导航栏。"""
        self.nav_items = nav_items
        self.theme_colors = theme_colors
        self.is_extended = is_extended
        self.on_change = on_change
        self.on_toggle = on_toggle
        self.selected_index = selected_index
        self.app_title = app_title

    def _build_title(self) -> ft.Container:
        """构建导航栏标题"""
        return ft.Container(
            content=ft.Image(
                src="images/icon.png",
                width=150 if self.is_extended else 50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.padding.only(top=10, bottom=10),
            padding=0,
        )

    def _build_destinations(self) -> List[ft.NavigationRailDestination]:
        """构建导航项列表"""
        # 添加展开/收起按钮作为第一个导航项
        destinations = [
            ft.NavigationRailDestination(
                icon=ft.Icons.MENU_OPEN,
                selected_icon=ft.Icons.MENU,
                label="Hide",
                padding=ft.padding.only(left=10) if self.is_extended else None,
            )
        ]
        
        # 添加其他导航项
        destinations.extend([
            ft.NavigationRailDestination(
                icon=item["icon"],
                selected_icon=item["icon"],
                label=item["label"],
                padding=ft.padding.only(left=10) if self.is_extended else None,
            ) for item in self.nav_items
        ])
        
        return destinations

    def build(self) -> ft.NavigationRail:
        """构建并返回导航栏对象"""
        nav = ft.NavigationRail(
            selected_index=self.selected_index + 1,  # 因为添加了展开/收起按钮，所以索引需要+1
            # 修改这2个属性来修改导航栏的显示方式
            label_type="selected" if self.is_extended else "none",
            extended=self.is_extended,
            # label_type=ft.NavigationRailLabelType.ALL,
            # extended=False,
            
            
            min_width=60,
            min_extended_width=150,
            bgcolor=self.theme_colors.nav_color,
            leading=self._build_title(),
            destinations=self._build_destinations(),
            on_change=self.on_change,
        )
        return nav


class TitleBar:
    def __init__(self, app_title: str, theme_colors, window, on_update: Callable, platform: str):
        self.app_title = app_title
        self.theme_colors = theme_colors
        self.window = window
        self.on_update = on_update
        self.platform = platform

    def build(self) -> ft.Container:
        def minimize(e):
            self.window.minimized = True
            self.on_update()

        def maximize(e):
            self.window.maximized = not self.window.maximized
            self.on_update()

        def close(e):
            self.window.close()
            self.on_update()

        # 创建标题文本部分
        title_content = ft.Row([
            ft.Container(width=10),  # 左侧间距
            ft.Text(
                self.app_title if self.platform != "macos" else "",
                size=14,
                weight="bold",
                color=self.theme_colors.text_color,
                expand=True,
            ),
        ])

        controls = [
            # 添加窗口拖动区域，使用 GestureDetector 处理双击
            ft.Container(
                content=title_content,
                expand=True,
                data="window-drag-area",  # 标记为可拖动区域
            ),
        ]

        # 在非 macOS 平台上添加窗口控制按钮
        if self.platform != "macos":
            controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.REMOVE,
                                icon_size=20,
                                icon_color=self.theme_colors.text_color,
                                tooltip="最小化",
                                on_click=minimize,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CROP_DIN if self.window.maximized else ft.Icons.CROP_SQUARE,
                                icon_size=20,
                                icon_color=self.theme_colors.text_color,
                                tooltip="还原" if self.window.maximized else "最大化",
                                on_click=maximize,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=20,
                                icon_color=self.theme_colors.text_color,
                                tooltip="关闭",
                                on_click=close,
                            ),
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.padding.only(right=10),
                    expand=False,
                ),
            )

        # 使用 WindowDragArea 包装整个标题栏， 实现窗口拖动
        title_bar = ft.WindowDragArea(
            content=ft.Container(
                content=ft.Row(
                    controls=controls,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=self.theme_colors.title_bar_color,
                height=40,
                data="window-drag-area",  # 标记整个标题栏为可拖动区域
            ),
        )
        return title_bar

class App:
    def __init__(self, config: AppConfig = None):
        self.config = config or AppConfig()
        self.page = None

        # 初始化时设置一个默认的主题颜色，后续会在init_page中更新
        self.theme_colors = ThemeColors(is_dark=self.config.theme_mode != "light")
        self.content_area = None
        self.nav_rail = None
        self.current_page_index = 0
        self.pages: Dict[int, BasePage] = {}
        self.nav_items: List[Dict] = []
        self.is_nav_extended = self.config.nav_rail_extended

    def _init_window(self):
        """初始化窗口设置"""
        # 设置窗口属性
        self.page.window.width = self.config.window_width
        self.page.window.height = self.config.window_height
        self.page.window.min_width = self.config.window_min_width
        self.page.window.min_height = self.config.window_min_height

        # 隐藏标题栏
        self.page.window.title_bar_hidden = True
        # 处理windows平台下的无边框窗口圆角问题
        if self.page.platform.value == "windows":
            self.page.window.frameless = True
            self.page.window.bgcolor = ft.Colors.TRANSPARENT
            self.page.bgcolor = ft.Colors.TRANSPARENT

        # 创建一个主容器
        self.main_container = ft.Container(
            content=self._create_layout(),
            bgcolor=self.theme_colors.bg_color,
            border_radius=10,
            expand=True,
            # 添加窗口调整大小的功能
            data="window-resizable",
        )

        # 设置窗口位置
        self.page.window.center()

    def _init_theme(self):
        """初始化主题设置"""
        # 根据配置设置主题模式
        if self.config.theme_mode == "system":
            is_dark = self.page.platform_brightness == "dark"
            self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        else:
            is_dark = self.config.theme_mode == "dark"
            self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT

        # 更新主题颜色
        self.theme_colors = ThemeColors(is_dark=is_dark)
        self.page.padding = 0

    def _create_layout(self):
        """创建主布局"""
        controls = []

        # 在非 macOS 平台上添加自定义标题栏
        title_bar = TitleBar(
            app_title=self.config.app_title,
            theme_colors=self.theme_colors,
            window=self.page.window,
            on_update=self.page.update,
            platform=self.platform
        )
        controls.append(title_bar.build())

        # 创建导航栏
        self.nav_rail = NavRail(
            nav_items=self.nav_items,
            theme_colors=self.theme_colors,
            is_extended=self.is_nav_extended,
            on_change=self._handle_nav_change,
            on_toggle=self._handle_nav_toggle,
            selected_index=self.current_page_index,
            app_title=self.config.app_title,
        )

        # 添加主要内容区域
        controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=self.nav_rail.build(),
                            padding=0,
                        ),
                        ft.Container(
                            content=ft.VerticalDivider(
                                width=1,
                                color=self.theme_colors.divider_color,
                            ),
                            padding=ft.padding.only(left=0, right=0),
                            margin=ft.margin.all(0),
                        ),
                        ft.Container(
                            content=self.content_area,
                            padding=ft.padding.only(left=10),
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    tight=True,
                ),
                expand=True,
            )
        )

        return ft.Column(
            controls=controls,
            spacing=0,
            expand=True,
        )

    def _handle_nav_change(self, e):
        """处理导航变化"""
        selected_index = e.control.selected_index
        if selected_index == 0:  # 展开/收起按钮
            self._handle_nav_toggle(e)
            # 恢复之前选中的导航项
            e.control.selected_index = self.current_page_index + 1
            self.page.update()
        else:
            actual_index = selected_index - 1  # 因为添加了展开/收起按钮，所以实际索引需要-1
            if actual_index == len(self.nav_items) - 1:  # Exit button
                self.page.window.close()
            else:
                self.current_page_index = actual_index
                self.content_area.content = self.pages[actual_index].content
                self.page.update()

    def _handle_nav_toggle(self, e):
        """处理导航栏展开/收起"""
        self.is_nav_extended = not self.is_nav_extended
        # 更新主容器的内容
        self.main_container.content = self._create_layout()
        self.page.update()

    def init_page(self, page: ft.Page):
        """初始化页面"""
        self.page = page
        self.platform = self.page.platform.value

        # 为所有页面设置 page 对象
        for page_instance in self.pages.values():
            page_instance.page = self.page

        self._init_theme()  # 先初始化主题
        self._init_window()  # 再初始化窗口

        # 添加主容器到页面
        self.page.add(self.main_container)

        # 更新所有组件的主题配色
        self._update_theme(self.config.theme_mode)

        self.page.update()

    def register_page(self, nav_item: Dict, page: BasePage):
        """
        注册页面和对应的导航项

        :param nav_item: 导航项配置，例如 {"icon": Icons.HOME, "label": "主页"}
        :param page: 页面实例
        """
        index = len(self.pages)
        page.page = self.page  # 设置 page 对象
        self.pages[index] = page
        self.nav_items.append(nav_item)

        if self.content_area is None:
            self.content_area = ft.Container(
                content=page.content,
                expand=True,
                bgcolor=self.theme_colors.bg_color,
            )

    def add_exit_nav(self):
        """添加退出导航项"""
        self.nav_items.append({
            "icon": ft.Icons.EXIT_TO_APP,
            "label": "退出"
        })

    def _update_theme(self, theme_mode: str):
        """更新主题"""
        self.config.theme_mode = theme_mode

        # 更新主题模式
        if theme_mode == "system":
            self.page.theme_mode = ft.ThemeMode.DARK if self.page.platform_brightness == "dark" else ft.ThemeMode.LIGHT
            is_dark = self.page.platform_brightness == "dark"
        else:
            self.page.theme_mode = ft.ThemeMode.DARK if theme_mode == "dark" else ft.ThemeMode.LIGHT
            is_dark = theme_mode == "dark"

        # 更新主题颜色
        self.theme_colors = ThemeColors(is_dark=is_dark)

        # 更新导航栏的主题颜色
        if self.nav_rail:
            self.nav_rail.theme_colors = self.theme_colors

        # 更新 macOS 标题栏颜色
        if self.page.platform.value == "macos":
            self.page.window.title_bar_buttons_color = self.theme_colors.text_color

        # 更新所有页面的主题
        for page in self.pages.values():
            page.update_theme(self.theme_colors, theme_mode)

        # 更新当前页面内容
        if self.content_area:
            self.content_area.content = self.pages[self.current_page_index].content
            self.content_area.bgcolor = self.theme_colors.bg_color

        # 更新主容器
        self.main_container.bgcolor = self.theme_colors.bg_color
        self.main_container.content = self._create_layout()
        self.page.update()

    def update_nav_rail_state(self, is_extended: bool):
        """更新导航栏展开状态"""
        self.is_nav_extended = is_extended
        # 更新主容器的内容
        self.main_container.content = self._create_layout()
        self.page.update()
