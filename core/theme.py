from dataclasses import dataclass

@dataclass
class ThemeColors:
    current_color: str = ""
    def __init__(self, is_dark: bool = True):
        if is_dark:
            self.title_bar_color = "#1E1E2E"
            self.bg_color = "#171721"
            self.nav_color = "#22222E"
            self.sub_nav_color = "#2A2A3C"
            self.card_color = "#262636"
            self.divider_color = "#34344A"
            self.text_color = "#E2E2E6"
            self.accent_color = "#7C5CFF"
            self.secondary_accent = "#FF7A93"
        else:
            # 保持浅色主题不变，因为您对它已经满意
            self.title_bar_color = "#FFFFFF"
            self.bg_color = "#F7F9FC"
            self.nav_color = "#FFFFFF"
            self.sub_nav_color = "#EDF2F7"
            self.card_color = "#FFFFFF"
            self.divider_color = "#E2E8F0"
            self.text_color = "#2D3748"
            self.accent_color = "#4C6FFF"
            self.secondary_accent = "#FF6B6B"