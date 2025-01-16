import os
import re
import random
import math
import urllib.parse
import asyncio
import aiohttp
import flet as ft
from app.base_page import BasePage

class MusicPlayer(BasePage):
    def __init__(self, **kwargs):
        self.current_index = 0
        self.is_playing = False
        self.shuffle_mode = False
        self.repeat_mode = False

        self.current_lyrics = "歌词未找到"
        self.current_cover = "images/default_cover.jpg"
        
        self.is_animating = False
        self.rotation_animation_task = None
    
        
        self.music_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "musics")
        try:
            self.music_files = sorted([f for f in os.listdir(self.music_dir) if f.endswith(".mp3")])
        except FileNotFoundError:
            self.music_files = []
            print(f"Error: Music directory not found at {self.music_dir}")
        
        # 避免重复创建的控件应该放在 __init__ 中
        self.audio = ft.Audio(src=self.get_current_song(), on_position_changed=self.update_progress_ui, on_state_changed=self.update_play_state)
        
        super().__init__(title="音乐播放器", **kwargs)
        # Add the audio control to the overlay so it's always available
        self.page.overlay.append(self.audio)
        print("音乐播放器初始化完成")

    def format_song_name(self, filename):
        
        name_without_extension = filename.rsplit('.', 1)[0]
        return name_without_extension.split('.', 1)[-1].strip()

    def update(self):
        if self.music_files:
            self.current_song_text.value = self.format_song_name(self.music_files[self.current_index])
            self.album_cover.foreground_image_src = self.current_cover
        self.page.update()

    def get_current_song(self):
        if not self.music_files:
            return "assets/musics"
        return os.path.join(self.music_dir, self.music_files[self.current_index])

    async def async_update_lyrics_and_cover(self):
        if not self.music_files:
            return
        song_name = self.format_song_name(self.music_files[self.current_index])
        encoded_name = urllib.parse.quote(song_name)
        print(f"获取歌曲图片url: https://api.lrc.cx/cover?title={song_name}")
        print(f"获取歌词url: https://api.lrc.cx/lyrics?title={song_name}")
        
        async with aiohttp.ClientSession() as session:
            # Fetch cover
            cover_url = f"https://api.lrc.cx/cover?title={encoded_name}"
            async with session.get(cover_url) as response:
                self.current_cover = response.url if response.status == 200 else "images/default_cover.jpg"

            # Fetch lyrics
            lyrics_url = f"https://api.lrc.cx/lyrics?title={encoded_name}"
            async with session.get(lyrics_url) as response:
                lyrics_text = await response.text() if response.status == 200 else "歌词未找到"
                self.current_lyrics = self.parse_lyrics(lyrics_text)
                # 给歌词添加7个空行, 用于显示在屏幕中间
                self.current_lyrics = [(0, "")]*7 + self.current_lyrics
        
                # Update the lyrics display
        self.update_lyrics()
        # Now update the UI with the new data
        self.update()
    
    def parse_lyrics(self, lyrics_text):
        lyrics_lines = lyrics_text.split('\n')
        parsed_lyrics = []
        
        for line in lyrics_lines:
            if line:
                time_match = re.match(r"\[(\d+):(\d+)\.(\d+)\](.*)", line)
                if time_match:
                    minutes, seconds, milliseconds, text = time_match.groups()
                    start_time = int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)
                    parsed_lyrics.append((start_time, text.strip()))
        
        return sorted(parsed_lyrics, key=lambda x: x[0])  # Sort by start time


    def update_lyrics(self):
        # Clear existing lyrics
        self.lyrics_text.controls.clear()
        
        # Add all lyrics to the Column
        for i, (_, text) in enumerate(self.current_lyrics):
            self.lyrics_text.controls.append(ft.Text(text, size=18, key=str(i), expand=True, text_align=ft.TextAlign.CENTER))
        self.page.update()

    def update_lyrics_display(self, position):
        # Find the last line whose start time is less than or equal to the current position
        current_line = next((i for i, (start, _) in reversed(list(enumerate(self.current_lyrics))) if start <= position), -1)
        
        if current_line == -1:
            current_line = 0

        # Highlight and scroll to the current line
        for i, text_control in enumerate(self.lyrics_text.controls):
            text_control.color = self.theme_colors.accent_color if i == current_line else None
            text_control.weight = ft.FontWeight.BOLD if i == current_line else ft.FontWeight.NORMAL
            text_control.size = 22 if i == current_line else 18
            # text_control.bgcolor = ft.colors.WHITE if i == current_line else None

        # Scroll to the current line
        if current_line >= 7:
            self.lyrics_text.scroll_to(key=str(current_line-7), duration=500)
        
        self.page.update()

    def rotate_album_cover(self):
        if not self.is_animating and self.is_playing:
            self.is_animating = True
            self.page.run_task(self.rotation_animation)
        elif not self.is_playing:
            self.stop_rotation()

    async def rotation_animation(self):
        while self.is_animating:
            self.album_cover_rotation_angle += math.radians(1)  # Increment by 1 degree in radians
            self.album_cover.rotate = ft.transform.Rotate(self.album_cover_rotation_angle)
            self.page.update()
            await asyncio.sleep(0.016)  # Approximately 60 FPS
        
        # self.album_cover_rotation_angle = 0  # Reset rotation angle when animation stops
        # self.album_cover.rotate = ft.transform.Rotate(0)  # Reset rotation to 0
        # self.page.update()

    def stop_rotation(self):
        if self.is_animating:
            self.is_animating = False
            self.page.update()  # Update to stop animation

    def toggle_play_pause(self, e):
        if self.is_playing:
            self.audio.pause()
            self.stop_rotation()  # Stop the rotation when pausing
        else:
            self.audio.play()
        self.is_playing = not self.is_playing
        self.update_play_button()
        self.rotate_album_cover()  # Start the rotation when playing
        self.update()

    def update_play_button(self):
        self.play_button.icon = ft.Icons.PAUSE if self.is_playing else ft.Icons.PLAY_ARROW
        self.page.update()

    def next_song(self, e):
        if not self.music_files:
            return
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.music_files) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.music_files)
        self.set_new_song()

    def previous_song(self, e):
        if not self.music_files:
            return
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.music_files) - 1)
        else:
            self.current_index = (self.current_index - 1) % len(self.music_files)
        self.set_new_song()

    def set_new_song(self):
        # Stop the current song before changing
        if self.is_playing:
            self.toggle_play_pause(None)
        
        # Set the new song source immediately
        self.audio.src = self.get_current_song()

        self.toggle_play_pause(None)
        
        # Asynchronously fetch and update lyrics and cover
        self.page.run_task(self.async_update_lyrics_and_cover)
        
        # Update UI to reflect the new song (even if lyrics and cover aren't loaded yet)
        self.update()

    def build_content(self):

        self.album_cover_rotation_angle = 0
        self.album_cover = ft.CircleAvatar(
            foreground_image_src="images/default_cover.jpg",  # Default cover
            width=60,
            height=60,
            content=ft.Icon(ft.Icons.MUSIC_NOTE, size=40),
            rotate=ft.transform.Rotate(0),  # Initial rotation is 0
            animate_rotation=ft.animation.Animation(16, "linear")  # Smooth linear animation over 1 second for each 360 degrees
        )

        self.current_song_text = ft.Text(
            self.format_song_name(self.music_files[self.current_index]) if self.music_files else "无可用歌曲",
            size=14,
            weight=ft.FontWeight.BOLD,
            width=200,
            overflow=ft.TextOverflow.ELLIPSIS,
            max_lines=1
        )

        # Scrollable lyrics
        self.lyrics_text = ft.Column(
            width=400,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        )

        self.progress = ft.Slider(
            min=0,
            max=1,
            value=0,
            on_change=self.seek,
            disabled=not self.music_files,
            width=400
        )

        self.time_display = ft.Text("00:00 / 00:00", size=12)

        self.play_button = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.toggle_play_pause,
            icon_size=32,
            icon_color=self.theme_colors.accent_color
        )

        self.volume_slider = ft.Slider(
            min=0,
            max=1,
            value=0.5,
            on_change=self.set_volume,
            width=150,
        )

        shuffle_button = ft.IconButton(
            icon=ft.Icons.SHUFFLE,
            on_click=self.toggle_shuffle,
            icon_size=24,
            tooltip="随机播放"
            
        )

        repeat_button = ft.IconButton(
            icon=ft.Icons.REPEAT,
            on_click=self.toggle_repeat,
            icon_size=24,
            tooltip="重复列表"
        )

        control_buttons = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, on_click=self.previous_song, icon_size=24, icon_color=self.theme_colors.accent_color),
                self.play_button,
                ft.IconButton(icon=ft.Icons.SKIP_NEXT, on_click=self.next_song, icon_size=24, icon_color=self.theme_colors.accent_color)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        additional_controls = ft.Row(
            controls=[shuffle_button, repeat_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        player_bar = ft.Container(
            content=ft.Row(
                controls=[
                    self.album_cover,
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.current_song_text,
                                    control_buttons,
                                    self.volume_slider
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True
                            ),
                            ft.Row(
                                controls=[
                                    self.progress,
                                    self.time_display,
                                    additional_controls
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True
                            )
                        ],
                        spacing=5,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=10,
            bgcolor=self.theme_colors.card_color,
            border_radius=ft.border_radius.only(top_left=10, top_right=10),
        )

        playlist_with_lyrics = ft.Row(
            controls=[
                self.build_playlist(),
                # 竖向分割线
                ft.VerticalDivider(1),
                ft.Container(
                    content=self.lyrics_text,
                    alignment=ft.alignment.center_left,
                    width=400,
                    padding=ft.padding.only(left=10),
                )
            ],
            expand=True
        )
        
        self.page.run_task(self.async_update_lyrics_and_cover)

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("播放列表", size=20, weight=ft.FontWeight.BOLD),
                            playlist_with_lyrics
                        ],
                        spacing=10
                    ),
                    expand=True,
                    padding=20,
                    border_radius=ft.border_radius.all(10),
                ),
                player_bar
            ],
            spacing=0,
            expand=True
        )

    def build_playlist(self):
        return ft.ListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(f"{i+1}. {self.format_song_name(song)}"),
                    on_click=lambda e, idx=i: self.select_song(e, idx)
                ) for i, song in enumerate(self.music_files)
            ],
            expand=True,
        )

    def select_song(self, e, index):
        self.current_index = index
        self.set_new_song()

    def seek(self, e):
        if self.audio.src and self.audio.get_duration() > 0:
            position = int(self.progress.value * self.audio.get_duration())
            self.audio.seek(position)
            self.update_time_display(position, self.audio.get_duration())
            self.page.update()

    def set_volume(self, e):
        if self.audio:
            self.audio.volume = e.control.value
            self.update()

    def update_time_display(self, position, duration):
        self.time_display.value = f"{self.format_time(position)} / {self.format_time(duration)}"
        self.page.update()

    def format_time(self, milliseconds):
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_progress_ui(self, e):
        if self.audio and self.audio.src:
            duration = self.audio.get_duration()
            if duration > 0:
                position = self.audio.get_current_position()
                self.progress.value = position / duration
                self.update_time_display(position, duration)
                
                # Update lyrics display based on current position
                self.update_lyrics_display(position)
                
                self.page.update()

    def update_play_state(self, e):
        if e.data == "completed" and not self.repeat_mode:
            self.next_song(e)
        self.page.update()

    def toggle_shuffle(self, e):
        self.shuffle_mode = not self.shuffle_mode
        e.control.icon = ft.Icons.SHUFFLE if not self.shuffle_mode else ft.Icons.SHUFFLE_ON
        self.page.update()

    def toggle_repeat(self, e):
        self.repeat_mode = not self.repeat_mode
        e.control.icon = ft.Icons.REPEAT if not self.repeat_mode else ft.Icons.REPEAT_ON
        self.page.update()