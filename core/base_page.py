from abc import ABC, abstractmethod
from typing import Callable
from flet import Container, Column, Text, padding, margin, Page
from .theme import ThemeColors

class BasePage(ABC):
    def __init__(self, on_theme_changed: Callable = None, theme_colors: ThemeColors = None, theme_mode: str = "dark", title: str = "", page: Page = None):
        self.on_theme_changed = on_theme_changed
        self.theme_colors = theme_colors or ThemeColors()
        self.theme_mode = theme_mode
        self.title = title
        self.page = page
        self.content = self.build()
    
    def build_title(self) -> Container:
        """构建统一的标题栏"""
        return Container(
            content=Text(
                self.title,
                size=23,
                color=self.theme_colors.text_color,
            ),
            padding=padding.only(top=10, bottom=10, left=30),
            bgcolor=self.theme_colors.nav_color,
            margin=margin.only(left=-10, bottom=20),
            width=5000,
        )

    @abstractmethod
    def build_content(self) -> Column:
        """子类实现此方法来构建页面主要内容"""
        pass

    def build(self) -> Container:
        """构建完整的页面布局"""
        return Container(
            content=Column(
                controls=[
                    self.build_title(),  # 标题部分
                    Container(  # 内容部分
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

    def update_theme(self, theme_colors: ThemeColors, theme_mode: str):
        self.theme_colors = theme_colors
        self.theme_mode = theme_mode
        self.content = self.build() 