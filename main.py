import flet as ft
from app.app import App, AppConfig
from app.pages.calc import CalcPage
from app.pages.home import HomePage
from app.pages.sub_navigation_bar.app import SubNavigationBar
from app.pages.inputs import InputsPage
from app.pages.carousel import CarouselPage
from app.pages.stack_page import StackPage
from app.config.config_manager import ConfigManager
from app.pages.todo import TodoPage


def main(page: ft.Page):
    # 设置资源目录
    page.assets_dir = "assets"
    
    # 设置语言
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("en","Us"),ft.Locale("zh","CN")],
        current_locale=ft.Locale("zh", "CN")
    )
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 创建应用配置
    config = AppConfig()
    config.app_title = config_manager.get("App", "title", "PyDracula")
    config.theme_mode = config_manager.get("Theme", "mode", "dark")
    config.background_image = config_manager.get("Theme", "background_image", "images/backgrounds/background1.jpg")
    config.window_width = int(config_manager.get("Window", "width", "1300"))
    config.window_height = int(config_manager.get("Window", "height", "800"))
    config.window_min_width = int(config_manager.get("Window", "min_width", "800"))
    config.window_min_height = int(config_manager.get("Window", "min_height", "600"))
    
    # 设置字体和主题色
    font_family = config.font_dict.get(page.platform.value, ["Roboto"])[0]
    theme_color = config_manager.get("Theme", "color", ft.Colors.BLUE)

    page.theme = ft.Theme(
        color_scheme_seed=theme_color,
        font_family=font_family
    )

    # 创建应用实例
    app = App(page=page, config=config)
    
    # 定义默认页面, 可以通过自定义 "is_bottom": True 来创建底部按钮
    pages = [
        {"icon": ft.Icons.HOME_ROUNDED, "name": "主页", "page_class": HomePage},
        # 要创建其他带子导航的页面, 可以直接复制 sub_navigation_bar 文件夹,然后重命名
        {"icon": ft.Icons.WIDGETS_ROUNDED, "name": "子导航", "page_class": SubNavigationBar},
        {"icon": ft.Icons.INPUT_ROUNDED, "name": "输入控件", "page_class": InputsPage},
        {"icon": ft.Icons.SLIDESHOW_ROUNDED, "name": "轮播图", "page_class": CarouselPage},
        {"icon": ft.Icons.STACKED_BAR_CHART, "name": "Stack", "page_class": StackPage},
        {"icon": ft.Icons.CHECK_CIRCLE_ROUNDED, "name": "todo", "page_class": TodoPage},
        {"icon": ft.Icons.CALCULATE, "name": "计算器", "page_class": CalcPage},
    ]
    
    # 注册页面
    app.register_pages(pages)
    app.register_settings_page(config_manager)
    app.init_page(page)

if __name__ == "__main__":
    ft.app(target=main)
