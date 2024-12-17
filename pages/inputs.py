from flet import (
    Column, Container, Row, Text, padding, border_radius,
    TextField, Dropdown, Checkbox, Radio, Switch, Slider,
    dropdown, IconButton, Icons, Colors, alignment,
    MainAxisAlignment, TimePicker, ElevatedButton
)
from core.base_page import BasePage

class InputsPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(title="输入控件", **kwargs)

    def _handle_time_entry_mode_change(self, e):
        """处理输入模式变化"""
        if hasattr(self, 'time_mode_text'):
            self.time_mode_text.value = f"输入模式变更为: {e.entry_mode}"
            self.time_mode_text.update()

    def build_content(self) -> Column:
        return Column(
            controls=[
                self.build_section("文本输入", self._build_text_inputs()),
                self.build_section("下拉选择", self._build_dropdowns()),
                self.build_section("复选框", self._build_checkboxes()),
                self.build_section("单选框", self._build_radios()),
                self.build_section("开关", self._build_switches()),
                self.build_section("滑块", self._build_sliders()),
                ],
            scroll="auto",
            spacing=20,
        )
        
    def _build_text_inputs(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    TextField(
                        label="基本输入框",
                        hint_text="请输入...",
                    ),
                    TextField(
                        label="带图标的输入框",
                        hint_text="搜索...",
                        prefix_icon=Icons.SEARCH,
                        suffix_icon=Icons.CLEAR,
                    ),
                    TextField(
                        label="密码输入框",
                        password=True,
                        can_reveal_password=True,
                    ),
                    TextField(
                        label="多行输入框",
                        multiline=True,
                        min_lines=3,
                        max_lines=5,
                    ),
                ],
                spacing=20,
            ),
        )

    def _build_dropdowns(self) -> Container:
        """下拉选择示例"""
        return Container(
            content=Row(
                controls=[
                    # 基本下拉框
                    Dropdown(
                        label="基本下拉框",
                        options=[
                            dropdown.Option("选项1"),
                            dropdown.Option("选项2"),
                            dropdown.Option("选项3"),
                        ],
                        width=200,
                    ),
                    # 使用前缀图标的下拉框
                    Dropdown(
                        label="带图标的下拉框",
                        prefix_icon=Icons.SETTINGS,
                        options=[
                            dropdown.Option("编辑"),
                            dropdown.Option("删除"),
                            dropdown.Option("保存"),
                        ],
                        width=200,
                    ),
                    # 禁用状态的下拉框
                    Dropdown(
                        label="禁用状态",
                        options=[
                            dropdown.Option("选项1"),
                            dropdown.Option("选项2"),
                        ],
                        width=200,
                        disabled=True,
                    ),
                ],
                spacing=20,
            ),
        )

    def _build_checkboxes(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    Checkbox(label="基本复选框"),
                    Checkbox(label="默认选中", value=True),
                    Checkbox(label="三态复选框", tristate=True),
                    Checkbox(label="禁用状态", disabled=True),
                ],
                spacing=10,
            ),
        )

    def _build_radios(self) -> Container:
        return Container(
            content=Row(
                controls=[
                    Radio(value="option1", label="选项1"),
                    Radio(value="option2", label="选项2"),
                    Radio(value="option3", label="选项3", disabled=True),
                ],
                spacing=10,
            ),
        )

    def _build_switches(self) -> Container:
        return Container(
            content=Row(
                controls=[
                    Switch(label="基本开关"),
                    Switch(label="默认开启", value=True),
                    Switch(label="禁用状态", disabled=True),
                ],
                spacing=20,
            ),
        )

    def _build_sliders(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    Slider(
                        min=0,
                        max=100,
                        value=40,
                        label="{value}%",
                    ),
                    Slider(
                        min=0,
                        max=100,
                        value=60,
                        divisions=10,
                        label="{value}",
                    ),
                ],
                spacing=20,
            ),
        )