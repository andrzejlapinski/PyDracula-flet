import flet as ft
from core.base_page import BasePage
from config.version import VERSION, APP_DESCRIPTION, GITHUB_URL
import requests
import asyncio

class SettingsPage(BasePage):
    def __init__(self, config_manager=None, app=None, **kwargs):
        self.config_manager = config_manager
        self.app = app  # 保存app引用
        self.proxy_test_text = None
        self.proxy_url = None
        self.proxy_controls = None
        self.proxy_switch = None
        super().__init__(title="设置", **kwargs)

    def _build_theme_settings(self) -> ft.Container:
        """构建主题设置部分"""
        # 主题模式和主题色选择
        theme_mode_row = ft.Row([
            ft.Text("主题模式", size=16, color=self.theme_colors.text_color),
            ft.Container(width=20),
            ft.SegmentedButton(
                segments=[
                    ft.Segment(
                        value="light",
                        label=ft.Text("浅色"),
                        icon=ft.Icon(ft.Icons.LIGHT_MODE),
                    ),
                    ft.Segment(
                        value="dark",
                        label=ft.Text("深色"),
                        icon=ft.Icon(ft.Icons.DARK_MODE),
                    ),
                    ft.Segment(
                        value="system",
                        label=ft.Text("跟随系统"),
                        icon=ft.Icon(ft.Icons.BRIGHTNESS_AUTO),
                    ),
                ],
                selected={self.theme_mode},
                on_change=lambda e: self._handle_theme_change(e),
            ),
        ], alignment=ft.MainAxisAlignment.START)

        # 主题色选择
        current_color = self.config_manager.get("Theme", "color", ft.Colors.BLUE)
        theme_colors_row = ft.Row([
            ft.Text("主题色", size=16, color=self.theme_colors.text_color),
            ft.Container(width=20),
            ft.Dropdown(
                width=200,
                value=current_color,
                content_padding=ft.padding.symmetric(horizontal=10),
                options=[
                    ft.dropdown.Option(
                        key=color,
                        content=ft.Row([
                            ft.Icon(ft.Icons.COLOR_LENS, color=color),
                            ft.Text(name, color=self.theme_colors.text_color)
                        ])
                    )
                    for name, color in [
                        ("蓝色", ft.Colors.BLUE.value),
                        ("绿色", ft.Colors.GREEN.value),
                        ("红色", ft.Colors.RED.value),
                        ("紫色", ft.Colors.PURPLE.value),
                        ("橙色", ft.Colors.ORANGE.value),
                        ("粉色", ft.Colors.PINK.value),
                        ("青色", ft.Colors.CYAN.value)
                    ]
                ],
                on_change=lambda e: self._handle_theme_color_change(e.data),
                select_icon=ft.Icons.CHECK,
                select_icon_enabled_color=self.theme_colors.text_color,
            ),
        ], alignment=ft.MainAxisAlignment.START)

        # 导航栏设置部分
        nav_rail_settings = ft.Row([
            ft.Text("导航栏", size=16, color=self.theme_colors.text_color),
            ft.Container(width=20),
            ft.Switch(
                label="默认展开",
                value=self.config_manager.get("Theme", "nav_rail_extended", "true").lower() == "true",
                on_change=lambda e: self._handle_nav_rail_change(e),
            ),
        ], alignment=ft.MainAxisAlignment.START)

        return self.build_section(
            "主题设置",
            ft.Column([
                theme_mode_row,
                ft.Container(height=20),
                theme_colors_row,
                ft.Container(height=20),
                nav_rail_settings,
            ], spacing=0)
        )

    def _build_proxy_settings(self) -> ft.Container:
        """构建代理设置部分"""
        # 代理开关
        self.proxy_switch = ft.Switch(
            label="启用代理",
            value=self.config_manager.get("Proxy", "enabled", "false").lower() == "true",
            on_change=lambda e: self._handle_proxy_change(e),
        )

        # 代理地址输入框
        self.proxy_url = ft.TextField(
            label="代理地址",
            value=self.config_manager.get("Proxy", "url", ""),
            hint_text="例如: http://127.0.0.1:7890",
            on_change=lambda e: self._handle_proxy_url_change(e),
        )

        # 测试按钮和结果文本
        self.proxy_test_text = ft.Text("", size=14, color=self.theme_colors.text_color)
        test_button = ft.ElevatedButton(
            "测试代理",
            icon=ft.Icons.NETWORK_CHECK,
            on_click=self._test_proxy,
        )

        # 创建一个容器来包含代理URL输入框、测试按钮和结果文本
        self.proxy_controls = ft.Column([
            ft.Row(
                [self.proxy_url, test_button, self.proxy_test_text],
                spacing=20,
            ),
        ], spacing=10, expand=True)

        return self.build_section(
            "代理设置",
            ft.Column([
                self.proxy_switch,
                self.proxy_controls,
            ], spacing=20, expand=True),
            expand=True
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
            self._build_proxy_settings(),
            self._build_window_settings(),
            self._build_about_section(),
        ], scroll="auto", spacing=20)

    # 事件处理方法
    def _handle_theme_change(self, e):
        if self.on_theme_changed:
            self.on_theme_changed(e.control.selected.pop())
        if self.config_manager:
            self.config_manager.set("Theme", "mode", e.control.selected.pop())

    def _handle_theme_color_change(self, color: str):
        """处理主题色变更"""
        if not color:
            return
        self.page.theme = ft.Theme(
            color_scheme_seed=color,
            font_family="Microsoft YaHei UI" if self.page.platform != "macos" else None
        )
        if self.config_manager:
            self.config_manager.set("Theme", "color", color)
        self.page.update()

    def _handle_nav_rail_change(self, e):
        """处理导航栏展开状态变更"""
        if self.config_manager:
            is_extended = e.control.value
            self.config_manager.set("Theme", "nav_rail_extended", str(is_extended))
            # 更新当前窗口的导航栏状态
            if self.app:
                self.app.update_nav_rail_state(is_extended)

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

    def _handle_proxy_change(self, e):
        if self.config_manager:
            enabled = e.control.value
            self.config_manager.set("Proxy", "enabled", str(enabled))

    def _handle_proxy_url_change(self, e):
        if self.config_manager:
            proxy_url = e.control.value
            self.config_manager.set("Proxy", "url", proxy_url)

    async def _test_proxy(self, e):
        if not self.proxy_test_text:
            return

        self.proxy_test_text.value = "正在测试..."
        self.proxy_test_text.color = self.theme_colors.text_color
        self.page.update()

        try:
            # 使用 asyncio.to_thread 在后台线程中运行同步的 requests 调用
            def make_request():
                return requests.get("http://ip-api.com/json/", proxies=self.get_proxies(), timeout=10)

            response = await asyncio.to_thread(make_request)
            data = response.json()
            
            if response.status_code == 200:
                self.proxy_test_text.value = f"当前IP: {data.get('query', 'Unknown')} ({data.get('country', 'Unknown')})"
                self.proxy_test_text.color = self.theme_colors.text_color
            else:
                self.proxy_test_text.value = "测试失败: 无法获取IP信息"
                self.proxy_test_text.color = self.theme_colors.text_color
                
        except Exception as ex:
            self.proxy_test_text.value = f"测试失败: {str(ex)}"
            self.proxy_test_text.color = self.theme_colors.text_color
            
        self.page.update()