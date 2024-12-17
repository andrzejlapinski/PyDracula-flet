from flet import (
    Column, Container, Row, Text, RadioGroup, Radio, 
    padding, border_radius, Switch, Dropdown, dropdown,
    TextField, ElevatedButton, Icons, VerticalDivider,
    TextButton, MainAxisAlignment, Icon
)
from core.base_page import BasePage
from config.version import VERSION, APP_DESCRIPTION, GITHUB_URL

class SettingsPage(BasePage):
    def __init__(self, config_manager=None, **kwargs):
        self.config_manager = config_manager
        super().__init__(title="设置", **kwargs)

    def build_content(self) -> Column:
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

        return Column(
            controls=[
                # 主题设置
                self.build_section(
                    "主题设置",
                    Column(
                        controls=[
                            Text("主题模式", size=16, color=self.theme_colors.text_color),
                            RadioGroup(
                                content=Column(
                                    controls=[
                                        Radio(value="dark", label="深色主题"),
                                        Radio(value="light", label="浅色主题"),
                                        Radio(value="system", label="跟随系统"),
                                    ]
                                ),
                                value=self.theme_mode,
                                on_change=on_theme_change,
                            ),
                            Container(height=20),
                            Text("导航栏", size=16, color=self.theme_colors.text_color),
                            Switch(
                                label="默认展开导航栏",
                                value=self.config_manager.get("Theme", "nav_rail_extended", "true").lower() == "true",
                                on_change=on_nav_extended_change,
                            ),
                        ],
                    ),
                ),
                self.build_section(
                    "窗口设置",
                    Row(
                        controls=[
                            # Dropdown(
                            #     label="界面语言",
                            # width=200,
                            # options=[
                            #     dropdown.Option("zh_CN", "简体中文"),
                            #     dropdown.Option("en_US", "English"),
                            # ],
                            # value=self.config_manager.get("App", "language", "zh_CN"),
                            # on_change=on_language_change,
                            # ),
                            Column(
                                controls=[
                                    Row(
                                        controls=[
                                            TextField(
                                                label="默认宽度",
                                                value=self.config_manager.get("Window", "width", "1300"),
                                                width=150,
                                                data="width",
                                                on_change=on_window_size_change,
                                            ),
                                            TextField(
                                                label="默认高度",
                                                value=self.config_manager.get("Window", "height", "800"),
                                                width=150,
                                                data="height",
                                                on_change=on_window_size_change,
                                            ),
                                        ],
                                        spacing=20,
                                    ),
                                    Row(
                                        controls=[
                                            TextField(
                                                label="最小宽度",
                                                value=self.config_manager.get("Window", "min_width", "500"),
                                                width=150,
                                                data="min_width",
                                                on_change=on_window_size_change,
                                            ),
                                            TextField(
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
                    Column(
                        controls=[
                            Row(
                                controls=[
                                    Column(
                                        controls=[
                                            Text(
                                                "PyDracula",
                                                size=30,
                                                weight="bold",
                                                color=self.theme_colors.text_color,
                                            ),
                                            Text(
                                                f"Version {VERSION}",
                                                size=16,
                                                color=self.theme_colors.text_color,
                                                opacity=0.8,
                                            ),
                                        ],
                                    ),
                                    Container(expand=True),
                                    TextButton(
                                        "访问 GitHub",
                                        icon=Icons.OPEN_IN_NEW,
                                        url=GITHUB_URL,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            Container(height=20),
                            Text(
                                APP_DESCRIPTION,
                                size=14,
                                color=self.theme_colors.text_color,
                                opacity=0.7,
                            ),
                            Container(height=10),
                            Row(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                Icon(
                                                    Icons.COPYRIGHT,
                                                    color=self.theme_colors.text_color,
                                                    opacity=0.5,
                                                    size=16,
                                                ),
                                                Text(
                                                    "2024 clarencejh",
                                                    size=14,
                                                    color=self.theme_colors.text_color,
                                                    opacity=0.5,
                                                ),
                                            ],
                                            spacing=5,
                                        ),
                                    ),
                                    Container(expand=True),
                                    TextButton(
                                        "检查更新",
                                        icon=Icons.SYSTEM_UPDATE,
                                        on_click=self._check_updates,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
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
        # 这里可以添加检查更新的逻辑
        # 例如：
        # 1. 从远程服务器获取最新版本
        # 2. 与当前版本比较
        # 3. 显示更新对话框
        pass 