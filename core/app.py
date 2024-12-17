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
    """
    导航栏类，用于构建应用程序的导航栏。
    """
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
        """
        初始化导航栏。

        :param nav_items: 导航项列表，每个项是一个字典，包含"icon"和"label"。
        :param theme_colors: 主题颜色对象。
        :param is_extended: 是否扩展导航栏，默认为True。
        :param on_change: 导航栏项变化时的回调函数。
        :param on_toggle: 导航栏扩展/收缩时的回调函数。
        :param selected_index: 当前选中的导航项索引，默认为0。
        :param app_title: 应用程序标题，默认为空字符串。
        """
        self.nav_items = nav_items
        self.theme_colors = theme_colors
        self.is_extended = is_extended
        self.on_change = on_change
        self.on_toggle = on_toggle
        self.selected_index = selected_index
        self.app_title = app_title

    def build(self) -> ft.NavigationRail:
        """
        构建并返回导航栏对象。
        """
        return ft.NavigationRail(
            selected_index=self.selected_index,
            label_type="selected" if self.is_extended else "none",
            min_width=60,
            min_extended_width=200,
            extended=self.is_extended,
            bgcolor=self.theme_colors.nav_color,
            leading=ft.Container(
                content=ft.Text(
                    f" {self.app_title} " if self.is_extended else self.app_title[0],
                    size=30,
                    weight="bold",
                    color="#89A8B2"
                ),
                margin=ft.padding.only(top=20, bottom=20),
                padding=0,
            ),
            destinations=[
                ft.NavigationRailDestination(
                    icon=item["icon"],
                    selected_icon=item["icon"],
                    label=item["label"],
                    padding=ft.padding.only(left=10) if self.is_extended else None,
                ) for item in self.nav_items
            ],
            on_change=self.on_change,
            trailing=ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT if self.is_extended else ft.Icons.CHEVRON_RIGHT,
                    icon_color=self.theme_colors.text_color,
                    on_click=self.on_toggle,
                ),
                margin=ft.padding.only(bottom=20),
            ),
        ) 

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
            
        # 使用 GestureDetector 包装整个标题栏
        return ft.WindowDragArea(
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

class App:
    def __init__(self, config: AppConfig = None):
        self.config = config or AppConfig()
        self.page = None
        
        # 根据配置确定是否使用深色主题
        is_dark = True
        if self.config.theme_mode == "light":
            is_dark = False
        elif self.config.theme_mode == "system":
            # 如果是系统主题，则需要等待页面初始化后才能获取系统主题
            is_dark = True  # 默认深色，后续会在 init_page 中更新
            
        self.theme_colors = ThemeColors(is_dark=is_dark)
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

        # 设置窗口透明和阴影效果
        self.page.window.bgcolor = ft.Colors.TRANSPARENT
        self.page.bgcolor = ft.Colors.TRANSPARENT
        self.page.padding = 15
        
        # 创建一个带阴影的主容器
        self.main_container = ft.Container(
            content=self._create_layout(),
            bgcolor=self.theme_colors.bg_color,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color="#66000000",  # 增加阴影不透明度
                offset=ft.Offset(0, 3),
            ),
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
            self.page.theme_mode = ft.ThemeMode.DARK if self.page.platform_brightness == "dark" else ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.DARK if self.config.theme_mode == "dark" else ft.ThemeMode.LIGHT
            
        self.page.bgcolor = self.theme_colors.bg_color
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
        nav_rail = NavRail(
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
                            content=nav_rail.build(),
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
        if selected_index == len(self.nav_items) - 1:  # Exit button
            self.page.window.close()
        else:
            self.current_page_index = selected_index
            self.content_area.content = self.pages[selected_index].content
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
            
        self._init_window()
        self._init_theme()

        # 添加主容器到页面
        self.page.add(self.main_container)
        
        # 调用当前页面的 did_mount（如果存在）
        if self.current_page_index in self.pages and hasattr(self.pages[self.current_page_index], 'did_mount'):
            self.pages[self.current_page_index].did_mount()
            
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