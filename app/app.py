import os
import json
import flet as ft
from typing import Callable, Dict, List, TYPE_CHECKING
from collections import UserDict

from .config.theme import ThemeColors

if TYPE_CHECKING:
    from .base import BasePage

class AppConfig(UserDict):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, main_path=""):
        if hasattr(self.__dict__, "_initialized"):  # Check if already initialized
            return
        self._initialized = True
        self.main_path = main_path
        self.config_file = os.path.join(main_path, "app/config/config.json")
        self.data = {}  # Initialize data
        self._ensure_config_file()
        self.load_config()
        print("加载配置管理器成功")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _ensure_config_file(self):
        """Ensures the config file and directories exist."""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        """Creates a default configuration."""
        self.data = {
            "Theme": {"mode": "dark", "color": "ft.Colors.BLUE", "background_image": "images/backgrounds/background1.jpg"},
            "Window": {
                "width": 1300,
                "height": 800,
                "min_width": 500,
                "min_height": 400,
                "font": {
                    "windows": [
                        "Segoe UI",
                        "Microsoft YaHei UI",
                        "Arial",
                    ],
                    "macos": [
                        "SF Pro",
                        "Helvetica Neue",
                        "PingFang SC",
                        "Hiragino Sans GB",
                    ],
                    "linux": [
                        "Ubuntu",
                        "Noto Sans CJK SC",
                        "DejaVu Sans",
                    ],
                },
            },
            "App": {"title": "PyDracula"}
        }
        self.save_config()

    def load_config(self):
        """Loads the configuration from the file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_default_config()

    def save_config(self):
        """Saves the current configuration to the file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get(self, section, key, default=None):
        """Retrieves a configuration value."""
        return self.data.get(section, {}).get(key, default)

    def set(self, section, key, value):
        """Sets a configuration value and saves it."""
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.save_config()

    def __getattr__(self, item):
        """Dynamic attribute access from the config data."""
        if item in self.__dict__:  # Check if it's an instance attribute first
            return self.__dict__[item]
        for section, settings in self.data.items():
            if item in settings:
                return settings[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        """Dynamic attribute setting and updating config."""
        if key in ['data', '_initialized', 'config_file', 'main_path']:  # Exempt internal attributes
            super().__setattr__(key, value)
        else:
            self.set("App", key, value)

    def add_section(self, section):
        """Adds a new section to the config if it doesn't exist."""
        if section not in self.data:
            self.data[section] = {}
            self.save_config()

    def remove_section(self, section):
        """Removes a section from the config if it exists."""
        if section in self.data:
            del self.data[section]
            self.save_config()

    def config_sections(self):
        """Returns a list of all section names in the config."""
        return list(self.data.keys())


class NavRail:
    """导航栏类，用于构建应用程序的导航栏。"""

    def __init__(
        self,
        page: ft.Page,
        theme_colors,
        on_change: Callable = None,
    ):
        self.page = page
        self.theme_colors: ThemeColors = theme_colors
        self.buttons = {}
        self.pages = {}  # 存储页面实例
        self.current_page = None
        self.nav_bar = []
        self.bottom_buttons = [ft.Container(expand=True)]  # 添加一个弹性容器作为占位符
        self.on_change = on_change  # 保存回调函数
        self.first_page_added = False  # 添加标记，用于跟踪第一个页面

    def add_page(self, name: str, page_class, icon, is_bottom=False):
        """
        添加页面和对应的导航按钮
        :param name: 页面唯一标识
        :param page_class: 页面类
        :param icon: 按钮图标
        :param is_bottom: 是否固定在底部
        """
        # 创建页面实例 - 直接使用已经创建的实例
        page_instance = page_class
        self.pages[name] = page_instance

        # 如果是第一个添加的页面，则自动激活
        active = not self.first_page_added
        if not self.first_page_added:
            self.first_page_added = True

        # 添加对应的导航按钮
        self.add_button(name, icon, active, is_bottom)

    # 显示第一个页面
    def show_first_page(self):
        if self.first_page_added:
            self.show_page(next(iter(self.pages.keys())))

    def show_page(self, name):
        """显示指定页面"""
        if name not in self.pages:
            print(f"页面 {name} 不存在！")
            return

        for btn_name, button in self.buttons.items():
            button.icon_color = self.theme_colors.accent_color if btn_name == name else self.theme_colors.text_color

        # 更新当前页面
        self.current_page = name

        # 调用回调函数通知页面变更
        if self.on_change:
            self.on_change(self.pages[name])

        self.page.update()

    def add_button(self, name, icon, active=False, is_bottom=False, on_click=None):
        """
        添加一个导航按钮
        :param name: 按钮唯一标识
        :param icon: 按钮图标 (Flet 图标名称)
        :param active: 是否默认激活
        :param is_bottom: 是否固定在底部
        """
        if name in self.buttons:
            raise ValueError(f"按钮 '{name}' 已存在！")

        button = ft.IconButton(
            icon=icon,
            icon_color=self.theme_colors.accent_color if active else self.theme_colors.text_color,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda e: self._handle_click(name) if on_click is None else on_click(e),
            hover_color=self.theme_colors.nav_color,
            mouse_cursor=ft.MouseCursor.BASIC,
        )
        self.buttons[name] = button

        # 如果按钮需要固定在底部，将它单独存储
        if is_bottom:
            self.bottom_buttons.append(button)
        else:
            self.nav_bar.append(button)

    def _handle_click(self, name):
        """处理按钮点击事件"""
        self.show_page(name)

    def switch_to(self, page_name: str):
        """
        切换到指定页面
        :param page_name: 页面名称
        :return: 是否切换成功
        """
        if page_name not in self.pages:
            print(f"页面 {page_name} 不存在！")
            return False

        # 更新按钮状态
        for btn_name, button in self.buttons.items():
            button.icon_color = self.theme_colors.accent_color if btn_name == page_name else self.theme_colors.text_color

        # 显示页面
        self.show_page(page_name)
        return True

    def build(self):
        """
        返回导航栏控件
        """
        # 在主导航栏的按钮和底部按钮之间插入一个 Spacer
        user_image = ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_src="images/user.jpeg",
                    content=ft.Text("User"),
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=self.theme_colors.accent_color, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
        controls = [ft.Container(height=50), user_image]  # 顶部空隙和用户头像
        controls.extend(self.nav_bar)  # 主按钮
        controls.extend(self.bottom_buttons)  # 底部按钮

        return ft.Container(
            content=ft.Column(controls=controls, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=self.theme_colors.nav_color,
            padding=ft.padding.symmetric(horizontal=13),
            width=65,
            border_radius=ft.border_radius.horizontal(left=8),
            left=0,
            top=0,
            bottom=0,
            expand=True,
        )

    def update_theme(self, theme_colors):
        """更新主题颜色"""
        self.theme_colors = theme_colors
        # 更新所有按钮的颜色
        for btn_name, button in self.buttons.items():
            button.icon_color = self.theme_colors.accent_color if btn_name == self.current_page else self.theme_colors.text_color
            button.hover_color = self.theme_colors.nav_color
        # 更新用户头像状态点的颜色
        if len(self.nav_bar) > 0 and isinstance(self.nav_bar[0], ft.Stack):
            status_dot = self.nav_bar[0].controls[1].content
            if isinstance(status_dot, ft.CircleAvatar):
                status_dot.bgcolor = self.theme_colors.accent_color


class App:
    def __init__(self, page: ft.Page, config: AppConfig = None):
        self.config = config or AppConfig()
        self.page = page

        # 初始化时设置一个默认的主题颜色，后续会在init_page中更新
        self.theme_colors = ThemeColors(is_dark=self.config.get("Theme", "mode") != "light")
        self.content_area = None
        self.nav_rail = None
        self.pages: Dict[int, "BasePage"] = {}
        self.main_container = None

        # 创建导航栏
        self.nav_rail = NavRail(
            page=self.page,
            theme_colors=self.theme_colors,
            on_change=self._handle_page_change,
        )

    def _init_window(self):
        """初始化窗口设置"""
        # 设置窗口属性
        self.page.window.width = self.config.get("Window", "width")
        self.page.window.height = self.config.get("Window", "height")
        self.page.window.min_width = self.config.get("Window", "min_width")
        self.page.window.min_height = self.config.get("Window", "min_height")

        # 隐藏标题栏
        self.page.window.title_bar_hidden = True
        # 处理windows平台下的无边框窗口圆角问题
        if self.page.platform.value == "windows":
            self.page.window.frameless = True
            self.page.window.bgcolor = ft.Colors.TRANSPARENT
            self.page.bgcolor = ft.Colors.TRANSPARENT

        # 设置窗口位置
        self.page.window.center()

    def _init_theme(self):
        """初始化主题设置"""
        # 根据配置设置主题模式
        if self.config.get("Theme", "mode") == "system":
            is_dark = self.page.platform_brightness == "dark"
            self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        else:
            is_dark = self.config.get("Theme", "mode") == "dark"
            self.page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT

        # 更新主题颜色
        self.theme_colors = ThemeColors(is_dark=is_dark)
        self.page.padding = 0

    def build_windows_title_bar(self):
        """创建windows标题栏"""

        def minimize(e):
            self.page.window.minimized = True
            self.page.update()

        def maximize(e):
            self.page.window.maximized = not self.page.window.maximized
            self.page.update()

        def close(e):
            self.page.window.close()
            self.page.update()

        title_bar = ft.WindowDragArea(
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
                        icon=ft.Icons.CROP_DIN if self.page.window.maximized else ft.Icons.CROP_SQUARE,
                        icon_size=20,
                        icon_color=self.theme_colors.text_color,
                        tooltip="还原" if self.page.window.maximized else "最大化",
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
            height=40,
            right=0,
            top=0,
            left=150,
            expand=True,
        )
        return title_bar

    def _create_layout(self) -> ft.Stack:
        """创建主布局"""

        # 创建主布局
        controls = [
            # 导航栏
            self.nav_rail.build(),
            # 内容区域
            ft.Container(
                content=self.content_area,
                left=65,  # nav_rail width
                right=0,
                top=0,
                bottom=0,
            ),
        ]

        # 如果不是macOS系统，添加Windows标题栏
        if self.page.platform.value != "macos":
            controls.append(self.build_windows_title_bar())

        layout = ft.Stack(
            controls=controls,
            expand=True,
            opacity=0.9,
        )

        return layout

    def _handle_page_change(self, page: "BasePage" = None):
        """处理页面切换"""
        self.current_page = page
        self.content_area.content = page.content
        self.page.update()

    def init_page(self, page: ft.Page):
        """初始化页面"""
        self.page = page
        self.platform = self.page.platform.value

        self._init_theme()  # 先初始化主题

        # 创建内容区域（使用第一个页面作为初始内容）
        first_page = next(iter(self.pages.values()))
        self.content_area = ft.Container(
            content=first_page.content,
            expand=True,
            bgcolor=self.theme_colors.bg_color,
        )

        self._init_window()  # 初始化窗口

        # 创建主容器
        self.main_container = ft.Container(
            content=self._create_layout(),
            # bgcolor=self.theme_colors.bg_color,
            border_radius=10,
            expand=True,
            data="window-resizable",
            image=ft.DecorationImage(src=self.config.get("Theme", "background_image"), fit=ft.ImageFit.FILL),
            # image_fit=ft.ImageFit.FILL,
        )

        # 添加主容器到页面
        self.page.add(self.main_container)

        # 更新所有组件的主题配色
        self._update_theme(self.config.get("Theme", "mode"))

        # 显示第一个页面
        self.nav_rail.show_first_page()

        self.page.update()

    def _register_page(self, nav_item: Dict, page):
        """
        注册页面和对应的导航项

        :param nav_item: 导航项配置，例如 {"icon": Icons.HOME, "name": "主页"}
        :param page: 页面实例
        """
        index = len(self.pages)
        self.pages[index] = page

        # 如果导航栏已经创建，将页面添加到导航栏
        if self.nav_rail:
            self.nav_rail.add_page(name=nav_item["name"], page_class=page, icon=nav_item["icon"], is_bottom=nav_item.get("is_bottom", False))

    def _update_theme(self, theme_mode: str):
        """更新主题"""
        self.config.set("Theme", "mode", theme_mode)

        # 更新主题模式
        if theme_mode == "system":
            self.page.theme_mode = ft.ThemeMode.DARK if self.page.platform_brightness == "dark" else ft.ThemeMode.LIGHT
            is_dark = self.page.platform_brightness == "dark"
        else:
            self.page.theme_mode = ft.ThemeMode.DARK if theme_mode == "dark" else ft.ThemeMode.LIGHT
            is_dark = theme_mode == "dark"

        # 更新主题颜色
        self.theme_colors = ThemeColors(is_dark=is_dark)
        self.theme_colors.current_color = self.page.theme.color_scheme_seed

        # 更新导航栏的主题颜色
        if self.nav_rail:
            self.nav_rail.update_theme(self.theme_colors)

        # 更新 macOS 标题栏颜色
        # if self.page.platform.value == "macos":
        #     self.page.window.title_bar_buttons_color = self.theme_colors.text_color

        # 更新所有页面的主题
        for page in self.pages.values():
            page.theme_colors = self.theme_colors
            page.theme_mode = theme_mode
            page.content = page.build()  # 重新构建页面内容

        # 更新当前页面内容
        if self.content_area and self.nav_rail and self.nav_rail.current_page:
            current_page = self.nav_rail.pages[self.nav_rail.current_page]
            self.content_area.content = current_page.content
            self.content_area.bgcolor = self.theme_colors.bg_color

        # 更新主容器
        self.main_container.content = self._create_layout()
        self.main_container.image.src = self.config.get("Theme", "background_image")
        self.main_container.image.fit = ft.ImageFit.FILL
        self.page.update()

    def register_settings_page(self):
        """
        注册设置页面
        :param config_manager: 配置管理器实例
        """
        from app.pages.settings import SettingsPage

        # 注册设置页面
        self._register_page(nav_item={"icon": ft.Icons.SETTINGS_ROUNDED, "name": "设置", "is_bottom": True}, page=SettingsPage(theme_colors=self.theme_colors, theme_mode=self.config.get("Theme", "mode"), on_theme_changed=self._update_theme, page=self.page, app=self, config_manager=self.config))

    def register_pages(self, pages: List[Dict]):
        """
        注册默认页面
        :param pages: 页面配置列表，每个配置包含 icon, name, page_class
        """
        # 注册页面
        for page_info in pages:
            self._register_page(nav_item={"icon": page_info["icon"], "name": page_info["name"], "is_bottom": page_info.get("is_bottom", False)}, page=page_info["page_class"](theme_colors=self.theme_colors, theme_mode=self.config.get("Theme", "mode"), page=self.page, app=self))

    def switch_page(self, page_name: str) -> bool:
        """
        切换到指定页面
        :param page_name: 页面名称
        :return: 是否切换成功
        """
        if self.nav_rail:
            return self.nav_rail.switch_to(page_name)
        return False
