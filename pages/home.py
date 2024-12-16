from flet import Column, Container, Row, Text, IconButton, Icons, ProgressBar, ListTile, Icon, padding, border_radius
from core.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(title="主页", **kwargs)

    def build_content(self) -> Column:
        return Column(
            controls=[
                self._build_stats_section(),
                self._build_actions_section(),
                self._build_progress_section(),
                self._build_activities_section(),
            ],
            scroll="auto",
            spacing=0,
        )

    def _build_stats_section(self) -> Container:
        return Container(
            content=Row(
                controls=[
                    Container(
                        content=Column([
                            Text("Statistics", color=self.theme_colors.text_color, size=20),
                            Text("125", color=self.theme_colors.text_color, size=40, weight="bold"),
                            Text("Active Projects", color=self.theme_colors.text_color, size=14),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        padding=20,
                        border_radius=border_radius.all(10),
                        width=200,
                        height=150,
                    ),
                    Container(
                        content=Column([
                            Text("Tasks", color=self.theme_colors.text_color, size=20),
                            Text("42", color=self.theme_colors.text_color, size=40, weight="bold"),
                            Text("Pending Tasks", color=self.theme_colors.text_color, size=14),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        padding=20,
                        border_radius=border_radius.all(10),
                        width=200,
                        height=150,
                    ),
                ],
                spacing=20,
            ),
            padding=20,
        )

    def _build_actions_section(self) -> Container:
        return Container(
            content=Row(
                controls=[
                    IconButton(
                        icon=Icons.ADD_CIRCLE,
                        icon_color=self.theme_colors.text_color,
                        icon_size=30,
                        tooltip="Add New",
                    ),
                    IconButton(
                        icon=Icons.FAVORITE,
                        icon_color="red",
                        icon_size=30,
                        tooltip="Favorite",
                    ),
                    IconButton(
                        icon=Icons.SHARE,
                        icon_color=self.theme_colors.text_color,
                        icon_size=30,
                        tooltip="Share",
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )

    def _build_progress_section(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    Text("Project Progress", size=20, color=self.theme_colors.text_color),
                    ProgressBar(
                        width=400,
                        value=0.7,
                        color="blue",
                        bgcolor=self.theme_colors.card_color,
                    ),
                    Text("70% Completed", size=14, color=self.theme_colors.text_color),
                ],
                spacing=10,
            ),
            padding=20,
        )

    def _build_activities_section(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    Text("Recent Activities", size=20, color=self.theme_colors.text_color),
                    Container(
                        content=Column([
                            ListTile(
                                leading=Icon(Icons.CALENDAR_MONTH),
                                title=Text("Team Meeting", color=self.theme_colors.text_color),
                                subtitle=Text("10:00 AM", color=self.theme_colors.text_color),
                            ),
                            ListTile(
                                leading=Icon(Icons.WORK),
                                title=Text("Project Review", color=self.theme_colors.text_color),
                                subtitle=Text("2:30 PM", color=self.theme_colors.text_color),
                            ),
                            ListTile(
                                leading=Icon(Icons.PERSON),
                                title=Text("Client Meeting", color=self.theme_colors.text_color),
                                subtitle=Text("4:00 PM", color=self.theme_colors.text_color),
                            ),
                        ]),
                        bgcolor=self.theme_colors.card_color,
                        border_radius=border_radius.all(10),
                        padding=10,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )