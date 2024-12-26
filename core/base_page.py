import flet as ft
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any, Optional
from .theme import ThemeColors
from core.config_manager import ConfigManager


class BasePage(ABC):
    def __init__(self,
                on_theme_changed: Callable = None,
                theme_colors: ThemeColors = None,
                theme_mode: str = "dark",
                title: str = "",
                page: ft.Page = None,
                has_sub_nav: bool = False
        ):
        
        self.on_theme_changed = on_theme_changed
        self.theme_colors = theme_colors or ThemeColors()
        self.theme_mode = theme_mode
        self.title = title
        self.page = page
        self._is_rebuilding = False  # 添加重建标志
        self._state = {}  # 添加状态存储
        self.proxies = None  # 添加代理设置
        self.has_sub_nav = has_sub_nav  # 是否启用子导航
        
        self.config_manager = ConfigManager()
        self.content = self.build()
        
    def show_dialog(self, message: str, title: str = "提示"):
        """
        显示弹窗提示，可自定义动作

        了解更多请访问
        url: https://flet.qiannianlu.com/docs/controls/alertdialog
        """
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            # actions=[
            #     ft.TextButton("确定", on_click=lambda _: self.page.open(None)),
            #     ft.TextButton("取消", on_click=lambda _: self.page.open(None))
            #     ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialog)
        self.page.update()

    def save_state(self):
        """保存页面状态，子类可以重写此方法来保存额外的状态"""
        state = {}
        # 只保存控件的值，让样式跟随主题
        for control_name, control in vars(self).items():
            if isinstance(control, (ft.TextField, ft.Dropdown, ft.RadioGroup, ft.Text)):
                state[control_name] = control.value
            elif isinstance(control, ft.ListView):
                state[control_name] = [c for c in control.controls]
            elif isinstance(control, ft.FloatingActionButton):
                state[control_name] = control.content
        return state

    def restore_state(self, state):
        """恢复页面状态，子类可以重写此方法来恢复额外的状态"""
        # 只恢复控件的值，让样式跟随主题
        for control_name, value in state.items():
            if hasattr(self, control_name):
                control = getattr(self, control_name)
                if isinstance(control, (ft.TextField, ft.Dropdown, ft.RadioGroup, ft.Text)):
                    control.value = value
                elif isinstance(control, ft.ListView):
                    control.controls = value

    def update_theme(self, theme_colors: ThemeColors, theme_mode: str):
        """更新主题时的处理"""
        self._is_rebuilding = True  # 设置重建标志

        # 保存当前状态
        self._state = self.save_state()

        # 更新主题
        self.theme_colors = theme_colors
        self.theme_mode = theme_mode

        # 重建页面
        self.content = self.build()

        # 恢复状态
        self.restore_state(self._state)

        self._is_rebuilding = False  # 清除重建标志

    def is_rebuilding(self) -> bool:
        """检查页面是否正在重建"""
        return getattr(self, '_is_rebuilding', False)

    def build_title(self) -> ft.Container:
        """构建统一的标题栏"""
        container = ft.Container(
            content=ft.Text(
                self.title,
                size=23,
                color=self.theme_colors.text_color,
            ),
            padding=ft.padding.only(top=10, bottom=10, left=30),
            bgcolor=self.theme_colors.nav_color,
            margin=ft.margin.only(bottom=20) if not self.has_sub_nav else ft.margin.only(bottom=0),
            width=5000,
        )
        return container

    @abstractmethod
    def build_content(self) -> ft.Column:
        """子类实现此方法来构建页面主要内容"""
        pass

    def build(self) -> ft.Container:
        """构建完整的页面布局"""
        container = ft.Container(
            content=ft.Column(
                controls=[
                    self.build_title(),
                    ft.Container(
                        content=self.build_content(),
                        expand=True,
                        bgcolor=self.theme_colors.bg_color,
                    ),
                ],
                spacing=0,
                scroll="none",
            ),
            expand=True,
            bgcolor=self.theme_colors.bg_color,
        )
        return container

    def build_section(self, title: str = None, content: ft.Control = None, expand=False) -> ft.Container:
        """构建一个带标题的部分"""
        controls = []

        if title:
            title_text = ft.Text(title, size=22, weight="bold",
                            color=self.theme_colors.text_color)
            controls.append(title_text)

        if content:
            if not isinstance(content, ft.Container):
                content = ft.Container(
                    content=content,
                    expand=True,
                )
            controls.append(content)

        section_content = ft.Column(
            controls=controls,
            spacing=10,
        )

        container = ft.Container(
            content=section_content,
            bgcolor=self.theme_colors.card_color,
            padding=20 if title else 10,
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, self.theme_colors.divider_color),
            margin=ft.padding.symmetric(horizontal=10, vertical=5),
            expand=expand,
        )

        return container

    def get_proxies(self):
        """
        获取代理设置
        
        如果配置文件中没有设置代理，则返回None
        
        return 
            {"http": proxy_url, "https": proxy_url}
            {"http": None, "https": None}
        """
        enabled_str = self.config_manager.get("Proxy", "enabled", False)
        proxy_url = self.config_manager.get("Proxy", "url", None)

        enabled = enabled_str.lower() == "true"
        
        if enabled and proxy_url:
            self.proxies = {"http": proxy_url, "https": proxy_url}
        else:
            self.proxies = {"http": None, "https": None}

        return self.proxies