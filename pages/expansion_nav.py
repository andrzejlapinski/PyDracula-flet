import flet as ft
from core.base_page import BasePage


class ExpansionNavPage(BasePage):
    def __init__(self, **kwargs):
        # 在调用父类初始化之前设置状态变量
        self.selected_item = None
        self.is_expanded = True
        super().__init__(title="ExpansionTile导航示例", **kwargs)
        
    def create_nav_item(self, text: str, icon: ft.Icons, selected: bool = False):
        return ft.ListTile(
            leading=ft.Icon(
                icon,
                color=ft.Colors.BLUE if selected else self.theme_colors.text_color,
                size=20,
            ),
            title=ft.Text(
                text,
                color=ft.Colors.BLUE if selected else self.theme_colors.text_color,
                weight=ft.FontWeight.W_500 if selected else None,
                size=14,
                visible=self.is_expanded,
            ),
            selected=selected,
            on_click=lambda e: self.handle_item_click(e, text),
        )
        
    def handle_item_click(self, e, text: str):
        """处理菜单项点击事件"""
        # 更新之前选中项的状态
        if self.selected_item:
            self.selected_item.selected = False
            self.selected_item.leading.color = self.theme_colors.text_color
            self.selected_item.title.color = self.theme_colors.text_color
            self.selected_item.title.weight = None
            
        # 更新当前选中项的状态
        e.control.selected = True
        e.control.leading.color = ft.Colors.BLUE
        e.control.title.color = ft.Colors.BLUE
        e.control.title.weight = ft.FontWeight.W_500
        self.selected_item = e.control
        
        # 更新页面
        self.page.update()
        print(f"Clicked {text}")
        
    def toggle_menu(self, e):
        """切换菜单展开/收起状态"""
        self.is_expanded = not self.is_expanded
        nav_container = e.control.data
        
        # 更新宽度
        nav_container.width = 250 if self.is_expanded else 60
        
        # 更新所有文本的可见性
        for control in nav_container.content.controls:
            if isinstance(control, ft.Container) and isinstance(control.content, ft.Row):
                # 处理标题行
                title = control.content.controls[0]
                title.visible = self.is_expanded
            elif isinstance(control, ft.ExpansionTile):
                # 处理ExpansionTile的标题和副标题
                control.title.visible = self.is_expanded
                control.subtitle.visible = self.is_expanded
                # 处理子菜单项
                for item in control.controls:
                    if isinstance(item, ft.ListTile):
                        item.title.visible = self.is_expanded
                        
        # 更新页面
        self.page.update()

    def build_content(self) -> ft.Column:
        # 创建导航菜单
        nav_menu = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Navigation Menu",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=self.theme_colors.text_color,
                                visible=self.is_expanded,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.MENU,
                                icon_color=self.theme_colors.text_color,
                                on_click=self.toggle_menu,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.only(left=16, right=8, top=8, bottom=8),
                ),
                ft.ExpansionTile(
                    leading=ft.Icon(
                        ft.Icons.MAIL_OUTLINE,
                        color=ft.Colors.BLUE,
                    ),
                    title=ft.Text(
                        "Navigation One",
                        color=ft.Colors.BLUE,
                        visible=self.is_expanded,
                    ),
                    subtitle=ft.Text(
                        "Home related items",
                        color=self.theme_colors.text_color,
                        size=12,
                        visible=self.is_expanded,
                    ),
                    bgcolor=self.theme_colors.card_color,
                    initially_expanded=True,
                    controls=[
                        self.create_nav_item("Item 1", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Option 1", ft.Icons.CIRCLE_OUTLINED, selected=True),
                        self.create_nav_item("Option 2", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Item 2", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Option 3", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Option 4", ft.Icons.CIRCLE_OUTLINED),
                    ],
                ),
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.APPS_OUTLINED),
                    title=ft.Text(
                        "Navigation Two",
                        visible=self.is_expanded,
                    ),
                    subtitle=ft.Text(
                        "System settings",
                        color=self.theme_colors.text_color,
                        size=12,
                        visible=self.is_expanded,
                    ),
                    bgcolor=self.theme_colors.card_color,
                    controls=[
                        self.create_nav_item("Option 5", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Option 6", ft.Icons.CIRCLE_OUTLINED),
                    ],
                ),
                ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED),
                    title=ft.Text(
                        "Navigation Three",
                        visible=self.is_expanded,
                    ),
                    subtitle=ft.Text(
                        "Additional settings",
                        color=self.theme_colors.text_color,
                        size=12,
                        visible=self.is_expanded,
                    ),
                    bgcolor=self.theme_colors.card_color,
                    controls=[
                        self.create_nav_item("Option 7", ft.Icons.CIRCLE_OUTLINED),
                        self.create_nav_item("Option 8", ft.Icons.CIRCLE_OUTLINED),
                    ],
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

        # 创建导航容器
        nav_container = ft.Container(
            content=nav_menu,
            width=250,
            bgcolor=self.theme_colors.card_color,
            border=ft.border.only(
                right=ft.BorderSide(1, self.theme_colors.divider_color)
            ),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        
        # 将导航容器引用存储到按钮的data属性中
        nav_menu.controls[0].content.controls[1].data = nav_container

        # 创建示例内容
        content = ft.Column(
            controls=[
                self.build_section(
                    title="ExpansionTile导航示例",
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                nav_container,
                                ft.Container(
                                    content=ft.Text(
                                        "Main Content Area",
                                        size=32,
                                        color=self.theme_colors.text_color,
                                    ),
                                    expand=True,
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            expand=True,
                        ),
                        padding=0,
                        expand=True,
                    ),
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

        return content 