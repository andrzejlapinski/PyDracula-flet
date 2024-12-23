import flet as ft
from core.base_page import BasePage


class WidgetsPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(title="组件", **kwargs)

    def build_content(self) -> ft.Column:
        column = ft.Column(
            controls=[
                self.build_section("填充按钮", self._build_filled_buttons()),
                self.build_section("浮动操作按钮", self._build_floating_buttons()),
                self.build_section("图标按钮", self._build_icon_buttons()),
                self.build_section("菜单按钮", self._build_menu_buttons()),
                self.build_section("轮廓按钮", self._build_outlined_buttons()),
                self.build_section("分段按钮", self._build_segmented_buttons()),
                self.build_section("文本按钮", self._build_text_buttons()),
            ],
            scroll="auto",
            spacing=20,
        )

        return column

    def _build_filled_buttons(self) -> ft.Container:
        """填充按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.FilledButton(text="基本按钮"),
                    ft.FilledButton(
                        text="带图标的按钮",
                        icon=ft.Icons.ADD,
                    ),
                    ft.FilledButton(
                        text="禁用按钮",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )
        return container

    def _build_floating_buttons(self) -> ft.Container:
        """浮动操作按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        tooltip="添加",
                    ),
                    ft.FloatingActionButton(
                        text="Extended",
                        icon=ft.Icons.ADD,
                        tooltip="扩展的浮动按钮",
                    ),
                    ft.FloatingActionButton(
                        icon=ft.Icons.EDIT,
                        bgcolor=ft.Colors.GREEN,
                        tooltip="编辑",
                    ),
                ],
                spacing=10,
            ),
        )
        return container
    def _build_icon_buttons(self) -> ft.Container:
        """图标按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE_BORDER,
                        icon_color="red",
                        icon_size=30,
                        tooltip="收藏",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SHARE,
                        icon_size=30,
                        tooltip="分享",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=30,
                        tooltip="删除",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )
        return container
    def _build_menu_buttons(self) -> ft.Container:
        """菜单按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.PopupMenuButton(
                        icon=ft.Icons.MENU,
                        items=[
                            ft.PopupMenuItem(text="选项 1"),
                            ft.PopupMenuItem(text="选项 2"),
                            ft.PopupMenuItem(text="选项 3"),
                        ],
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="设置",
                                icon=ft.Icons.SETTINGS,
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                text="删除",
                                icon=ft.Icons.DELETE,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.PopupMenuButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ARROW_DROP_DOWN),
                                    ft.Text("更多选项"),
                                ],
                            ),
                            items=[
                                ft.PopupMenuItem(text="子选项 1"),
                                ft.PopupMenuItem(text="子选项 2"),
                            ],
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=ft.border_radius.all(4),
                        padding=ft.padding.all(8),
                    ),
                ],
                spacing=10,
            ),
        )
        return container
    def _build_outlined_buttons(self) -> ft.Container:
        """轮廓按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.OutlinedButton(text="基本轮廓按钮"),
                    ft.OutlinedButton(
                        text="带图标",
                        icon=ft.Icons.SETTINGS,
                    ),
                    ft.OutlinedButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )
        return container
    def _build_segmented_buttons(self) -> ft.Container:
        """分段按钮示例"""
        container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    text="日",
                                    icon=ft.Icons.CALENDAR_VIEW_DAY,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=0),
                                    ),
                                ),
                                ft.OutlinedButton(
                                    text="周",
                                    icon=ft.Icons.CALENDAR_VIEW_WEEK,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=0),
                                    ),
                                ),
                                ft.OutlinedButton(
                                    text="月",
                                    icon=ft.Icons.CALENDAR_VIEW_MONTH,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(
                                            radius=0),
                                    ),
                                ),
                            ],
                            spacing=0,
                        ),
                        border=ft.border.all(1, ft.Colors.BLUE),
                        border_radius=ft.border_radius.all(4),
                    ),
                ],
                spacing=10,
            ),
        )
        return container
    def _build_text_buttons(self) -> ft.Container:
        """文本按钮示例"""
        self.container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.TextButton(text="基本文本按钮"),
                    ft.TextButton(
                        text="带图标",
                        icon=ft.Icons.INFO,
                    ),
                    ft.TextButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )
        return self.container
