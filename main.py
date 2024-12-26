import flet as ft
from core.app import App, AppConfig
from pages.home import HomePage
from pages.sub_navigation_bar.app import SubNavigationBar
from pages.settings import SettingsPage
from pages.inputs import InputsPage
from pages.carousel import CarouselPage
from core.config_manager import ConfigManager


def main(page: ft.Page):
    # 设置资源目录
    page.assets_dir = "assets"
    
    # 如果是macos则不设置字体
    if page.platform.value != "macos":
        # 设置字体, 兼容windows
        page.theme = ft.Theme(font_family="Microsoft YaHei UI")
    
    # # 设置窗口透明度和背景色（实现模糊效果）
    # page.window.opacity = 0.95  # 设置透明度 (0.0 - 1.0)
    # page.window.bgcolor = ft.Colors.with_opacity(0.8, ft.Colors.BLACK)  # 半透明背景
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 创建应用配置
    config = AppConfig()
    config.app_title = config_manager.get("App", "title", "PyDracula")
    config.theme_mode = config_manager.get("Theme", "mode", "dark")
    config.window_width = int(config_manager.get("Window", "width", "1300"))
    config.window_height = int(config_manager.get("Window", "height", "800"))
    config.window_min_width = int(config_manager.get("Window", "min_width", "500"))
    config.window_min_height = int(config_manager.get("Window", "min_height", "400"))
    config.nav_rail_extended = config_manager.get("Theme", "nav_rail_extended", "true").lower() == "true"
    
    # 设置主题色
    theme_color = config_manager.get("Theme", "color", ft.Colors.BLUE)
    page.theme = ft.Theme(color_scheme_seed=theme_color)
    
    # 创建应用实例
    app = App(config)
    
    # 注册页面和导航项, 在这里添加页面
    pages = [
        {"icon": ft.Icons.HOME_ROUNDED, "label": "主页", "page_class": HomePage},
        # 要创建其他带子导航的页面, 可以直接复制 sub_navigation_bar 文件夹,然后重命名
        {"icon": ft.Icons.WIDGETS_ROUNDED, "label": "子导航", "page_class": SubNavigationBar},
        {"icon": ft.Icons.INPUT_ROUNDED, "label": "输入控件", "page_class": InputsPage},
        {"icon": ft.Icons.SLIDESHOW_ROUNDED, "label": "轮播图", "page_class": CarouselPage},
    ]

    for page_info in pages:
        app.register_page(
            nav_item={"icon": page_info["icon"], "label": page_info["label"]},
            page=page_info["page_class"](
                theme_colors=app.theme_colors,
                theme_mode=config.theme_mode,
                page=page
            )
        )
    
    app.register_page(
        nav_item={"icon": ft.Icons.SETTINGS_ROUNDED, "label": "设置"},
        page=SettingsPage(
            theme_colors=app.theme_colors,
            theme_mode=config.theme_mode,
            on_theme_changed=app._update_theme,
            config_manager=config_manager,
            page=page,
            app=app
        )
    )
    
    # 添加退出导航项
    app.add_exit_nav()
    
    # 初始化应用
    app.init_page(page)

if __name__ == "__main__":
    ft.app(target=main)
