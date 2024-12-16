import flet as ft
from flet import Icons
from core.app import App, AppConfig
from pages.home import HomePage
from pages.widgets import WidgetsPage
from pages.settings import SettingsPage
from pages.inputs import InputsPage
from core.config_manager import ConfigManager


def main(page: ft.Page):
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
    
    # 创建应用实例
    app = App(config)
    
    # 注册页面和导航项
    app.register_page(
        nav_item={"icon": Icons.HOME_ROUNDED, "label": "主页"},
        page=HomePage(theme_colors=app.theme_colors, theme_mode=config.theme_mode)
    )
    
    app.register_page(
        nav_item={"icon": Icons.WIDGETS_ROUNDED, "label": "按钮组件"},
        page=WidgetsPage(theme_colors=app.theme_colors, theme_mode=config.theme_mode)
    )
    
    app.register_page(
        nav_item={"icon": Icons.INPUT_ROUNDED, "label": "输入控件"},
        page=InputsPage(theme_colors=app.theme_colors, theme_mode=config.theme_mode)
    )
    
    app.register_page(
        nav_item={"icon": Icons.SETTINGS_ROUNDED, "label": "设置"},
        page=SettingsPage(
            theme_colors=app.theme_colors,
            theme_mode=config.theme_mode,
            on_theme_changed=app._update_theme,
            config_manager=config_manager
        )
    )
    
    # 添加退出导航项
    app.add_exit_nav()
    
    # 初始化应用
    app.init_page(page)

if __name__ == "__main__":
    ft.app(target=main)
