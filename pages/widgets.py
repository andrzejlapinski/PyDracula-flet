from flet import (
    Column, Container, Row, Text, padding, border_radius,
    ElevatedButton, FilledButton, FloatingActionButton, IconButton,
    MenuItemButton, OutlinedButton, PopupMenuButton, SegmentedButton,
    SubmenuButton, TextButton, Icon, Icons, PopupMenuItem,
    Colors, alignment, MainAxisAlignment, border, ButtonStyle, RoundedRectangleBorder
)
from core.base_page import BasePage

class WidgetsPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(title="组件", **kwargs)

    def build_content(self) -> Column:
        return Column(
            controls=[
                self._build_section("填充按钮", self._build_filled_buttons()),
                self._build_section("浮动操作按钮", self._build_floating_buttons()),
                self._build_section("图标按钮", self._build_icon_buttons()),
                self._build_section("菜单按钮", self._build_menu_buttons()),
                self._build_section("轮廓按钮", self._build_outlined_buttons()),
                self._build_section("分段按钮", self._build_segmented_buttons()),
                self._build_section("文本按钮", self._build_text_buttons()),
            ],
            scroll="auto",
            spacing=20,
        )

    def _build_section(self, title: str, content: Container) -> Container:
        """构建一个带标题的部分"""
        return Container(
            content=Column(
                controls=[
                    Text(title, size=20, weight="bold", color=self.theme_colors.text_color),
                    content,
                ],
                spacing=10,
            ),
            bgcolor=self.theme_colors.card_color,
            padding=30,
            border_radius=border_radius.all(10),
            border=border.all(1, self.theme_colors.divider_color),  # 添加轮廓线
            margin=padding.symmetric(horizontal=20),
        )

    def _build_filled_buttons(self) -> Container:
        """填充按钮示例"""
        return Container(
            content=Row(
                controls=[
                    FilledButton(text="基本按钮"),
                    FilledButton(
                        text="带图标的按钮",
                        icon=Icons.ADD,
                    ),
                    FilledButton(
                        text="禁用按钮",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_floating_buttons(self) -> Container:
        """浮动操作按钮示例"""
        return Container(
            content=Row(
                controls=[
                    FloatingActionButton(
                        icon=Icons.ADD,
                        tooltip="添加",
                    ),
                    FloatingActionButton(
                        text="Extended",
                        icon=Icons.ADD,
                        tooltip="扩展的浮动按钮",
                    ),
                    FloatingActionButton(
                        icon=Icons.EDIT,
                        bgcolor=Colors.GREEN,
                        tooltip="编辑",
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_icon_buttons(self) -> Container:
        """图标按钮示例"""
        return Container(
            content=Row(
                controls=[
                    IconButton(
                        icon=Icons.FAVORITE_BORDER,
                        icon_color="red",
                        icon_size=30,
                        tooltip="收藏",
                    ),
                    IconButton(
                        icon=Icons.SHARE,
                        icon_size=30,
                        tooltip="分享",
                    ),
                    IconButton(
                        icon=Icons.DELETE,
                        icon_size=30,
                        tooltip="删除",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_menu_buttons(self) -> Container:
        """菜单按钮示例"""
        return Container(
            content=Row(
                controls=[
                    # 基本的弹出菜单
                    PopupMenuButton(
                        icon=Icons.MENU,
                        items=[
                            PopupMenuItem(text="选项 1"),
                            PopupMenuItem(text="选项 2"),
                            PopupMenuItem(text="选项 3"),
                        ],
                    ),
                    # 带图标的弹出菜单
                    PopupMenuButton(
                        icon=Icons.MORE_VERT,
                        items=[
                            PopupMenuItem(
                                text="设置",
                                icon=Icons.SETTINGS,
                            ),
                            PopupMenuItem(),  # 分隔线
                            PopupMenuItem(
                                text="删除",
                                icon=Icons.DELETE,
                            ),
                        ],
                    ),
                    # 自定义样式的弹出菜单
                    Container(
                        content=PopupMenuButton(
                            content=Row(
                                controls=[
                                    Icon(Icons.ARROW_DROP_DOWN),
                                    Text("更多选项"),
                                ],
                            ),
                            items=[
                                PopupMenuItem(text="子选项 1"),
                                PopupMenuItem(text="子选项 2"),
                            ],
                        ),
                        border=border.all(1, Colors.BLUE),
                        border_radius=border_radius.all(4),
                        padding=padding.all(8),
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_outlined_buttons(self) -> Container:
        """轮廓按钮示例"""
        return Container(
            content=Row(
                controls=[
                    OutlinedButton(text="基本轮廓按钮"),
                    OutlinedButton(
                        text="带图标",
                        icon=Icons.SETTINGS,
                    ),
                    OutlinedButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_segmented_buttons(self) -> Container:
        """分段按钮示例"""
        return Container(
            content=Row(
                controls=[
                    # 使用多个按钮模拟分段按钮
                    Container(
                        content=Row(
                            controls=[
                                OutlinedButton(
                                    text="日",
                                    icon=Icons.CALENDAR_VIEW_DAY,
                                    style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                                OutlinedButton(
                                    text="周",
                                    icon=Icons.CALENDAR_VIEW_WEEK,
                                    style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                                OutlinedButton(
                                    text="月",
                                    icon=Icons.CALENDAR_VIEW_MONTH,
                                    style=ButtonStyle(
                                        shape=RoundedRectangleBorder(radius=0),
                                    ),
                                ),
                            ],
                            spacing=0,
                        ),
                        border=border.all(1, Colors.BLUE),
                        border_radius=border_radius.all(4),
                    ),
                ],
                spacing=10,
            ),
        )

    def _build_text_buttons(self) -> Container:
        """文本按钮示例"""
        return Container(
            content=Row(
                controls=[
                    TextButton(text="基本文本按钮"),
                    TextButton(
                        text="带图标",
                        icon=Icons.INFO,
                    ),
                    TextButton(
                        text="禁用",
                        disabled=True,
                    ),
                ],
                spacing=10,
            ),
        ) 