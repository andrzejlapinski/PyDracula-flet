import flet as ft
from core.base_page import BasePage
from config.version import VERSION, APP_DESCRIPTION, GITHUB_URL

class SettingsPage(BasePage):
    def __init__(self, config_manager=None, **kwargs):
        self.config_manager = config_manager
        super().__init__(title="设置", **kwargs)

    def build_content(self) -> ft.Column:
        def on_theme_change(e):
            if self.on_theme_changed:
                self.on_theme_changed(e.control.value)
            if self.config_manager:
                self.config_manager.set("Theme", "mode", e.control.value)

        def on_language_change(e):
            if self.config_manager:
                self.config_manager.set("App", "language", e.control.value)

        def on_nav_extended_change(e):
            if self.config_manager:
                self.config_manager.set("Theme", "nav_rail_extended", str(e.control.value))

        def on_window_size_change(e):
            if self.config_manager:
                try:
                    value = int(e.control.value)
                    self.config_manager.set("Window", e.control.data, str(value))
                except ValueError:
                    pass

        return ft.Column(
            controls=[
                # 主题设置
                self.build_section(
                    "主题设置",
                    ft.Column(
                        controls=[
                            ft.Text("主题模式", size=16, color=self.theme_colors.text_color),
                            ft.RadioGroup(
                                content=ft.Column(
                                    controls=[
                                        ft.Radio(value="dark", label="深色主题"),
                                        ft.Radio(value="light", label="浅色主题"),
                                        ft.Radio(value="system", label="跟随系统"),
                                    ]
                                ),
                                value=self.theme_mode,
                                on_change=on_theme_change,
                            ),
                            ft.Container(height=20),
                            ft.Text("导航栏", size=16, color=self.theme_colors.text_color),
                            ft.Switch(
                                label="默认展开导航栏",
                                value=self.config_manager.get("Theme", "nav_rail_extended", "true").lower() == "true",
                                on_change=on_nav_extended_change,
                            ),
                        ],
                    ),
                ),
                self.build_section(
                    "窗口设置",
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.TextField(
                                                label="默认宽度",
                                                value=self.config_manager.get("Window", "width", "1300"),
                                                width=150,
                                                data="width",
                                                on_change=on_window_size_change,
                                            ),
                                            ft.TextField(
                                                label="默认高度",
                                                value=self.config_manager.get("Window", "height", "800"),
                                                width=150,
                                                data="height",
                                                on_change=on_window_size_change,
                                            ),
                                        ],
                                        spacing=20,
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.TextField(
                                                label="最小宽度",
                                                value=self.config_manager.get("Window", "min_width", "500"),
                                                width=150,
                                                data="min_width",
                                                on_change=on_window_size_change,
                                            ),
                                            ft.TextField(
                                                label="最小高度",
                                                value=self.config_manager.get("Window", "min_height", "400"),
                                                width=150,
                                                data="min_height",
                                                on_change=on_window_size_change,
                                            ),
                                        ],
                                        spacing=20,
                                    ),
                                ],
                                spacing=20,
                            ),
                        ],
                        spacing=20,
                    ),
                ),
                # 添加关于部分
                self.build_section(
                    "关于",
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "PyDracula",
                                                size=30,
                                                weight="bold",
                                                color=self.theme_colors.text_color,
                                            ),
                                            ft.Text(
                                                f"Version {VERSION}",
                                                size=16,
                                                color=self.theme_colors.text_color,
                                                opacity=0.8,
                                            ),
                                        ],
                                    ),
                                    ft.Container(expand=True),
                                    ft.TextButton(
                                        "访问 GitHub",
                                        icon=ft.Icons.OPEN_IN_NEW,
                                        url=GITHUB_URL,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                APP_DESCRIPTION,
                                size=14,
                                color=self.theme_colors.text_color,
                                opacity=0.7,
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.COPYRIGHT,
                                                    color=self.theme_colors.text_color,
                                                    opacity=0.5,
                                                    size=16,
                                                ),
                                                ft.Text(
                                                    "2024 calg",
                                                    size=14,
                                                    color=self.theme_colors.text_color,
                                                    opacity=0.5,
                                                ),
                                            ],
                                            spacing=5,
                                        ),
                                    ),
                                    ft.Container(expand=True),
                                    ft.TextButton(
                                        "检查更新",
                                        icon=ft.Icons.SYSTEM_UPDATE,
                                        on_click=self._check_updates,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=10,
                    ),
                ),
            ],
            scroll="auto",
            spacing=20,
        )

    def _check_updates(self, e):
        """检查更新"""
        pass