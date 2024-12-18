import flet as ft
from core.base_page import BasePage
from config.version import VERSION, APP_DESCRIPTION, GITHUB_URL

class SettingsPage(BasePage):
    def __init__(self, config_manager=None, **kwargs):
        self.config_manager = config_manager
        super().__init__(title="设置", **kwargs)

    def _build_theme_settings(self) -> ft.Container:
        """构建主题设置部分"""
        # 主题模式部分
        theme_mode_group = ft.Column([
            ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value="dark", label="深色主题"),
                    ft.Radio(value="light", label="浅色主题"),
                    ft.Radio(value="system", label="跟随系统"),
                ]),
                value=self.theme_mode,
                on_change=lambda e: self._handle_theme_change(e),
            ),
        ])

        # 导航栏设置部分
        nav_rail_settings = ft.Column([
            ft.Text("导航栏", size=16, color=self.theme_colors.text_color),
            ft.Switch(
                label="默认展开导航栏",
                value=self.config_manager.get("Theme", "nav_rail_extended", "true").lower() == "true",
                on_change=lambda e: self._handle_nav_rail_change(e),
            ),
        ])

        return self.build_section(
            "主题设置",
            ft.Column([theme_mode_group, ft.Container(height=20), nav_rail_settings])
        )

    def _build_window_settings(self) -> ft.Container:
        """构建窗口设置部分"""
        # 默认尺寸设置
        default_size = ft.Row([
            ft.TextField(
                label="默认宽度",
                value=self.config_manager.get("Window", "width", "1300"),
                width=150,
                data="width",
                on_change=lambda e: self._handle_window_size_change(e),
            ),
            ft.TextField(
                label="默认高度",
                value=self.config_manager.get("Window", "height", "800"),
                width=150,
                data="height",
                on_change=lambda e: self._handle_window_size_change(e),
            ),
        ], spacing=20)

        # 最小尺寸设置
        min_size = ft.Row([
            ft.TextField(
                label="最小宽度",
                value=self.config_manager.get("Window", "min_width", "500"),
                width=150,
                data="min_width",
                on_change=lambda e: self._handle_window_size_change(e),
            ),
            ft.TextField(
                label="最小高度",
                value=self.config_manager.get("Window", "min_height", "400"),
                width=150,
                data="min_height",
                on_change=lambda e: self._handle_window_size_change(e),
            ),
        ], spacing=20)

        return self.build_section(
            "窗口设置",
            ft.Column([default_size, min_size], spacing=20)
        )

    def _build_about_section(self) -> ft.Container:
        """构建关于部分"""
        # 头部信息
        header = ft.Row([
            ft.Column([
                ft.Text("PyDracula", size=30, weight="bold", color=self.theme_colors.text_color),
                ft.Text(f"Version {VERSION}", size=16, color=self.theme_colors.text_color, opacity=0.8),
            ]),
            ft.Container(expand=True),
            ft.TextButton("访问 GitHub", icon=ft.Icons.OPEN_IN_NEW, url=GITHUB_URL),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # 底部信息
        footer = ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.COPYRIGHT, color=self.theme_colors.text_color, opacity=0.5, size=16),
                    ft.Text("2024 calg", size=14, color=self.theme_colors.text_color, opacity=0.5),
                ], spacing=5),
            ),
            ft.Container(expand=True),
            ft.TextButton("检查更新", icon=ft.Icons.SYSTEM_UPDATE, on_click=self._check_updates),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return self.build_section(
            "关于",
            ft.Column([
                header,
                ft.Container(height=20),
                ft.Text(APP_DESCRIPTION, size=14, color=self.theme_colors.text_color, opacity=0.7),
                ft.Container(height=10),
                footer,
            ], spacing=10)
        )

    def build_content(self) -> ft.Column:
        """构建页面内容"""
        return ft.Column([
            self._build_theme_settings(),
            self._build_window_settings(),
            self._build_about_section(),
        ], scroll="auto", spacing=20)

    # 事件处理方法
    def _handle_theme_change(self, e):
        if self.on_theme_changed:
            self.on_theme_changed(e.control.value)
        if self.config_manager:
            self.config_manager.set("Theme", "mode", e.control.value)

    def _handle_nav_rail_change(self, e):
        if self.config_manager:
            self.config_manager.set("Theme", "nav_rail_extended", str(e.control.value))

    def _handle_window_size_change(self, e):
        if self.config_manager:
            try:
                value = int(e.control.value)
                self.config_manager.set("Window", e.control.data, str(value))
            except ValueError:
                pass

    def _check_updates(self, e):
        """检查更新"""
        pass