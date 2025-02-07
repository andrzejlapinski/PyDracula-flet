import os
import random
import math
import asyncio
import flet as ft
from app.base import BasePage
from typing import TYPE_CHECKING

from app.utils import read_song_metadata, format_song_name

if TYPE_CHECKING:
    from app.app import App


class MusicPlayer(BasePage):
    def __init__(self, app, **kwargs):
        self.app: "App" = app
        self.title = "音乐播放器"

        # 从配置加载设置
        self.is_playing = False
        self.shuffle_mode = self.app.config.Music.shuffle_mode
        self.repeat_mode = self.app.config.Music.repeat_mode
        self.single_repeat_mode = self.app.config.Music.single_repeat_mode

        self.current_lyrics = "歌词未找到"
        self.current_cover = self.app.config.Music.default_cover

        self.is_animating = False
        self.rotation_animation_task = None
        self.current_index = 0
        self.mute = False
        # 初始化音乐目录和播放列表
        self.music_dir = os.path.join(self.app.config.main_path, self.app.config.Music.music_dir)

        # 确保音乐目录存在
        if not os.path.exists(self.music_dir):
            try:
                os.makedirs(self.music_dir)
                print(f"创建音乐目录: {self.music_dir}")
            except Exception as e:
                print(f"创建音乐目录失败: {str(e)}")

        self.playlists = self.get_all_playlists()
        self.all_songs = self.get_all_songs()

        # 如果没有任何歌曲，使用空状态
        if not self.all_songs:
            print("没有找到任何音乐文件")
            self.current_playlist = "所有歌曲"
            self.audio = ft.Audio()  # 创建空的音频控件
            super().__init__(title=self.title, app=app, **kwargs)
            return

        # 设置当前播放列表
        self.current_playlist = self.app.config.Music.current_playlist
        if self.current_playlist not in self.playlists and self.current_playlist != "所有歌曲":
            self.current_playlist = "所有歌曲"
            self.app.config.set("Music", "current_playlist", "所有歌曲")

        # 初始化播放列表状态
        self._init_playlist_states()

        # 恢复上次播放的歌曲
        self._restore_last_playback_state()

        # 初始化音频控件
        self.audio = ft.Audio(src=self.get_current_song(), volume=self.app.config.Music.volume, on_position_changed=self.update_progress_ui, on_state_changed=self.update_play_state)

        # 调用父类初始化
        super().__init__(title=self.title, app=app, **kwargs)

        # 添加音频控件到页面
        self.page.overlay.append(self.audio)
        self.page.update()

        # 使用 page.run_task 来延迟执行 seek 操作
        if self.app.config.Music.last_position > 0:
            self.page.run_task(self._restore_playback_position)

        print("音乐播放器初始化完成")

    async def _restore_playback_position(self):
        """恢复播放位置"""
        try:
            await asyncio.sleep(0.1)  # 给予一点时间让音频控件完全初始化
            self.audio.seek(self.app.config.Music.last_position)
        except Exception as e:
            print(f"恢复播放位置失败: {str(e)}")

    def _init_playlist_states(self):
        """初始化所有播放列表状态"""
        playlist_states = self.app.config.Music.playlist_states

        # 确保所有歌单都有状态记录
        for playlist in ["所有歌曲"] + list(self.playlists.keys()):
            if playlist not in playlist_states:
                playlist_states[playlist] = {"last_song_path": "", "last_position": 0}

        self.app.config.set("Music", "playlist_states", playlist_states)

    def _restore_last_playback_state(self):
        """恢复上次的播放状态"""
        playlist_states = self.app.config.Music.playlist_states
        current_playlist_state = playlist_states.get(self.current_playlist, {})
        last_song_path = current_playlist_state.get("last_song_path", "")

        # 验证歌曲是否存在于当前播放列表
        if last_song_path:
            songs = self.all_songs if self.current_playlist == "所有歌曲" else self.playlists.get(self.current_playlist, [])
            try:
                self.current_index = [os.path.abspath(s) for s in songs].index(os.path.abspath(last_song_path))
            except ValueError:
                # 如果歌曲不在列表中，从头开始播放
                self.current_index = 0
                if songs:
                    current_playlist_state["last_song_path"] = songs[0]
                else:
                    current_playlist_state["last_song_path"] = ""
                current_playlist_state["last_position"] = 0
        else:
            self.current_index = 0

    def _save_playlist_state(self):
        """保存当前播放列表状态"""
        try:
            current_song = self.get_current_song()
            # 只有在音频控件已添加到页面后才获取位置
            if hasattr(self, "page") and self.page and self.audio:
                try:
                    current_position = self.audio.get_current_position()
                except AssertionError:
                    current_position = 0
            else:
                current_position = 0

            playlist_states = self.app.config.Music.playlist_states
            playlist_states[self.current_playlist] = {"last_song_path": current_song, "last_position": current_position}

            self.app.config.set("Music", "playlist_states", playlist_states)
            self.app.config.set("Music", "current_song_path", current_song)
            self.app.config.set("Music", "last_position", current_position)
        except Exception as e:
            print(f"保存播放状态时出错: {str(e)}")

    def get_all_playlists(self):
        """获取所有播放列表"""
        playlists = {}
        try:
            if not os.path.exists(self.music_dir):
                print(f"音乐目录不存在: {self.music_dir}")
                return playlists

            for root, dirs, files in os.walk(self.music_dir):
                mp3_files = [f for f in files if f.lower().endswith(".mp3")]
                if mp3_files:
                    playlist_name = os.path.basename(root) if root != self.music_dir else "默认歌单"
                    playlist_files = sorted([os.path.join(root, f) for f in mp3_files], key=lambda f: f.lower())
                    playlists[playlist_name] = playlist_files

        except Exception as e:
            print(f"获取播放列表时出错: {str(e)}")

        return playlists

    def get_all_songs(self):
        """获取所有歌曲"""
        all_songs = []
        try:
            for playlist in self.playlists.values():
                all_songs.extend(playlist)
        except Exception as e:
            print(f"获取所有歌曲时出错: {str(e)}")

        return sorted(all_songs, key=lambda x: os.path.basename(x).lower()) if all_songs else []

    def get_current_song(self):
        """获取当前歌曲路径"""
        try:
            if not self.all_songs:
                return ""

            if self.current_playlist == "所有歌曲":
                if 0 <= self.current_index < len(self.all_songs):
                    return self.all_songs[self.current_index]
            else:
                playlist_songs = self.playlists.get(self.current_playlist, [])
                if 0 <= self.current_index < len(playlist_songs):
                    return playlist_songs[self.current_index]

            # 如果索引无效，重置为第一首歌
            self.current_index = 0
            if self.current_playlist == "所有歌曲":
                return self.all_songs[0] if self.all_songs else ""
            return self.playlists.get(self.current_playlist, [""])[0]

        except Exception as e:
            print(f"获取当前歌曲路径时出错: {str(e)}")

            return ""

    def update(self):
        if self.current_playlist == "所有歌曲":
            current_song_path = self.all_songs[self.current_index]
        else:
            current_song_path = self.playlists[self.current_playlist][self.current_index]

        self.current_song_text.value = format_song_name(os.path.basename(current_song_path))

        self.page.update()

    async def async_update_lyrics_and_cover(self, increment_index: bool = False):
        if self.current_playlist == "所有歌曲":
            song_path = self.all_songs[self.current_index]
        else:
            song_path = self.playlists[self.current_playlist][self.current_index]

        # 获取歌曲元数据
        metadata = await read_song_metadata(song_path, increment_index)
        if metadata:
            # 更新标题
            if metadata["title"]:
                self.current_song_text.value = metadata["title"]
            else:
                self.current_song_text.value = format_song_name(os.path.basename(song_path))

            self.current_song_singer.value = metadata.get("artist", "未知")
            self.current_song_album.value = metadata.get("album", "未知")
            self.refresh_button.text = metadata.get("isrc", "未知")

            # 更新封面
            if metadata["cover_url"]:
                self.current_cover = metadata["cover_url"]
            else:
                self.current_cover = "images/default_cover.jpg"
            self.album_cover.foreground_image_src = self.current_cover

            # 更新歌词
            if metadata["lyrics"]:
                from app.utils import parse_lyrics

                self.current_lyrics = [(0, "")] * 7 + parse_lyrics(metadata["lyrics"])
            else:
                self.current_lyrics = [(0, "歌词未找到")]
        else:
            # 如果获取元数据失败，使用默认值
            self.current_song_text.value = format_song_name(os.path.basename(song_path))
            self.current_cover = "images/default_cover.jpg"
            self.current_lyrics = [(0, "歌词未找到")]

        # 更新界面
        self.update_lyrics()
        self.update()

    def update_lyrics(self):
        # Clear existing lyrics
        self.lyrics_text.controls.clear()

        # Add all lyrics to the Column
        for i, (_, text) in enumerate(self.current_lyrics):
            self.lyrics_text.controls.append(ft.Text(text, size=18, key=str(i), expand=True, text_align=ft.TextAlign.CENTER))
        self.page.update()

    def update_lyrics_display(self, position):
        # Find the last line whose start time is less than or equal to the current position
        if self.app.current_page.title == self.title:
            current_line = next((i for i, (start, _) in reversed(list(enumerate(self.current_lyrics))) if start <= position), -1)

            if current_line == -1:
                current_line = 0

            # Highlight and scroll to the current line
            for i, text_control in enumerate(self.lyrics_text.controls):
                text_control.color = self.theme_colors.accent_color if i == current_line else None
                text_control.weight = ft.FontWeight.BOLD if i == current_line else ft.FontWeight.NORMAL
                text_control.size = 22 if i == current_line else 18

            # Scroll to the current line
            if current_line >= 7:
                self.lyrics_text.scroll_to(key=str(current_line - 7), duration=100)

            self.page.update()
        else:
            pass

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
        """播放下一首歌曲"""
        if self.current_playlist == "所有歌曲":
            songs_list = self.all_songs
        else:
            songs_list = self.playlists.get(self.current_playlist, [])

        if not songs_list:
            return

        # 保存当前索引，以便更新UI
        old_index = self.current_index

        # 根据播放模式选择下一首歌曲
        if self.shuffle_mode:
            # 随机模式下，避免重复播放当前歌曲
            if len(songs_list) > 1:
                new_index = self.current_index
                while new_index == self.current_index:
                    new_index = random.randint(0, len(songs_list) - 1)
                self.current_index = new_index
            else:
                self.current_index = 0
        else:
            self.current_index = (self.current_index + 1) % len(songs_list)

        # 更新UI中的高亮显示
        self._update_song_highlight(old_index, self.current_index)

        # 播放新歌曲
        self.set_new_song()

    def previous_song(self, e):
        """播放上一首歌曲"""
        if self.current_playlist == "所有歌曲":
            songs_list = self.all_songs
        else:
            songs_list = self.playlists.get(self.current_playlist, [])

        if not songs_list:
            return

        # 保存当前索引，以便更新UI
        old_index = self.current_index

        # 根据播放模式选择上一首歌曲
        if self.shuffle_mode:
            # 随机模式下，避免重复播放当前歌曲
            if len(songs_list) > 1:
                new_index = self.current_index
                while new_index == self.current_index:
                    new_index = random.randint(0, len(songs_list) - 1)
                self.current_index = new_index
            else:
                self.current_index = 0
        else:
            self.current_index = (self.current_index - 1) % len(songs_list)

        # 更新UI中的高亮显示
        self._update_song_highlight(old_index, self.current_index)

        # 播放新歌曲
        self.set_new_song()

    def _get_song_key(self, song_path: str) -> str:
        """生成歌曲的唯一key"""
        # 使用相对路径作为key，确保唯一性
        rel_path = os.path.relpath(os.path.abspath(song_path), self.music_dir)
        # 替换特殊字符，确保key的有效性
        safe_key = rel_path.replace("/", "_").replace("\\", "_").replace(".", "_")
        return f"song_{safe_key}"

    def _update_playlist_view(self):
        """更新播放列表视图"""
        # Reset all playlist highlights
        for tile in self.playlist_list.controls:
            tile.title.color = None
            tile.bgcolor = "transparent"

        # Highlight the selected playlist
        for tile in self.playlist_list.controls:
            if tile.title.value == self.current_playlist:
                tile.title.color = self.theme_colors.accent_color
                tile.bgcolor = self.theme_colors.card_color
                break

        # Get songs for the selected playlist
        if self.current_playlist == "所有歌曲":
            songs = self.all_songs
        else:
            songs = self.playlists.get(self.current_playlist, [])

        # Update the song list view
        self.current_playlist_view.controls = [
            ft.ListTile(
                key=self._get_song_key(song),  # 使用唯一的key
                title=ft.Text(f"{i + 1}. {format_song_name(os.path.basename(song))}", color=self.theme_colors.accent_color if i == self.current_index else None),
                bgcolor=self.theme_colors.card_color if i == self.current_index else "transparent",
                on_click=lambda e, song=song: self.select_song(e, song),
            )
            for i, song in enumerate(songs)
        ]

        self.page.update()

    def _update_song_highlight(self, old_index: int, new_index: int):
        """更新歌曲列表中的高亮显示，并滚动到当前播放的歌曲"""
        try:
            # 获取当前正在播放的歌曲路径
            current_song = self.get_current_song()
            current_song_abs = os.path.abspath(current_song)

            # 获取当前显示的播放列表中的歌曲
            if self.current_playlist == "所有歌曲":
                playlist_songs = self.all_songs
            else:
                playlist_songs = self.playlists.get(self.current_playlist, [])

            # 检查当前播放的歌曲是否在显示的列表中
            song_in_current_view = current_song_abs in [os.path.abspath(s) for s in playlist_songs]

            # 移除旧的高亮
            if 0 <= old_index < len(self.current_playlist_view.controls):
                old_tile = self.current_playlist_view.controls[old_index]
                old_tile.bgcolor = "transparent"
                old_tile.title.color = None

            # 添加新的高亮
            if 0 <= new_index < len(self.current_playlist_view.controls):
                new_tile = self.current_playlist_view.controls[new_index]
                new_tile.bgcolor = self.theme_colors.card_color
                new_tile.title.color = self.theme_colors.accent_color

                # 只有当歌曲在当前显示的列表中时才滚动
                if song_in_current_view:
                    # 使用歌曲的唯一key进行滚动
                    self.current_playlist_view.scroll_to(
                        key=self._get_song_key(current_song),
                        duration=300,  # 滚动动画持续时间（毫秒）
                    )

            self.page.update()
        except Exception as e:
            print(f"更新歌曲高亮显示时出错: {str(e)}")

    def set_new_song(self):
        """设置新的歌曲"""
        # Stop the current song before changing
        if self.is_playing:
            self.toggle_play_pause(None)

        # 重置进度条
        self.progress.value = 0
        self.page.update()

        # Set the new song source immediately
        current_song = self.get_current_song()
        self.audio.src = current_song

        # 保存播放状态
        self._save_playlist_state()

        self.toggle_play_pause(None)

        # Asynchronously fetch and update lyrics and cover
        self.page.run_task(self.async_update_lyrics_and_cover)

        # Update UI to reflect the new song
        self.update()

    def show_playlist(self, playlist_name):
        """切换播放列表视图，不影响当前播放"""
        # 如果是同一个播放列表，只更新显示
        if self.current_playlist == playlist_name:
            self._update_playlist_view()
            return

        # 保存当前播放列表状态（但不切换播放）
        if hasattr(self, "page") and self.page:
            self._save_playlist_state()

        # 暂存当前播放状态
        previous_playlist = self.current_playlist
        previous_index = self.current_index

        # 获取新播放列表的歌曲
        if playlist_name == "所有歌曲":
            new_songs = self.all_songs
        else:
            new_songs = self.playlists.get(playlist_name, [])

        # 如果新播放列表为空，不进行切换
        if not new_songs:
            print(f"播放列表 {playlist_name} 为空")
            return

        # 切换到新播放列表
        self.current_playlist = playlist_name

        # 如果新列表中包含当前播放的歌曲，保持该歌曲的索引
        current_song = self.get_current_song()
        if current_song:
            try:
                # 尝试在新列表中找到当前歌曲
                self.current_index = [os.path.abspath(s) for s in new_songs].index(os.path.abspath(current_song))
            except ValueError:
                # 如果新列表中没有当前歌曲，设置为第一首歌
                self.current_index = 0
                # 不恢复到原来的播放列表，而是显示新列表
                print(f"当前歌曲在新播放列表中未找到，从第一首开始显示")
        else:
            # 如果当前没有播放的歌曲，从第一首开始
            self.current_index = 0

        # 更新界面显示
        self._update_playlist_view()

        # 保存当前播放列表设置（但不影响播放状态）
        self.app.config.set("Music", "current_playlist", self.current_playlist)

    def build_content(self):
        """构建播放器界面"""
        try:
            # 如果没有任何歌曲，显示提示信息
            if not self.all_songs:
                return ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("没有找到任何音乐文件", size=20, color=self.theme_colors.accent_color),
                            ft.Text(f"请将音乐文件放入 {self.music_dir} 目录", size=16),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                )

            # 正常构建播放器界面
            self.album_cover_rotation_angle = 0
            self.album_cover = ft.CircleAvatar(
                foreground_image_src="images/default_cover.jpg",  # Default cover
                width=60,
                height=60,
                content=ft.Icon(ft.Icons.MUSIC_NOTE, size=40),
                rotate=ft.transform.Rotate(0),  # Initial rotation is 0
                animate_rotation=ft.animation.Animation(16, "linear"),  # Smooth linear animation over 1 second for each 360 degrees，
            )

            self.current_song_text = ft.Text(
                format_song_name(os.path.basename(self.get_current_song())) if self.current_playlist in self.playlists or self.current_playlist == "所有歌曲" else "无可用歌曲",
                size=14,
                weight=ft.FontWeight.BOLD,
                width=200,
                overflow=ft.TextOverflow.ELLIPSIS,
                max_lines=1,
                color=self.theme_colors.accent_color,
                selectable=True,
            )

            # 歌手
            self.current_song_singer = ft.Text("歌手", size=12, weight=ft.FontWeight.NORMAL, width=200, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, color=self.theme_colors.secondary_accent, selectable=True, tooltip="歌手")
            # 专辑
            self.current_song_album = ft.Text("专辑", size=12, weight=ft.FontWeight.NORMAL, width=200, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, color=self.theme_colors.secondary_accent, selectable=True, tooltip="专辑")
            # 刷新按钮
            self.refresh_button = ft.TextButton("刷新歌曲信息", on_click=self.refresh_song_metadata, height=20, tooltip="刷新歌曲信息")

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
                disabled=not self.all_songs,  # Disable if no songs available
                width=400,
            )

            self.time_display = ft.Text("00:00 / 00:00", size=12)

            self.play_button = ft.IconButton(icon=ft.Icons.PLAY_ARROW, on_click=self.toggle_play_pause, icon_size=32, icon_color=self.theme_colors.accent_color)

            self.mute_button = ft.IconButton(icon=ft.Icons.VOLUME_OFF if self.mute else ft.Icons.VOLUME_UP, on_click=self.toggle_mute, icon_size=24, tooltip="静音 快捷键:M", selected=self.mute)

            self.volume_slider = ft.Slider(
                min=0,
                max=1,
                value=self.app.config.Music.volume,  # 使用保存的音量值
                on_change=self.set_volume,
                width=150,
                tooltip="音量 快捷键:上下",
            )

            # 保存按钮为类属性
            self.shuffle_button = ft.IconButton(icon=ft.Icons.SHUFFLE_ON if self.shuffle_mode else ft.Icons.SHUFFLE, on_click=self.toggle_shuffle, icon_size=24, tooltip="随机播放", selected=self.shuffle_mode)

            self.repeat_button = ft.IconButton(icon=ft.Icons.REPEAT_ON if self.repeat_mode else ft.Icons.REPEAT, on_click=self.toggle_repeat, icon_size=24, tooltip="重复列表", selected=self.repeat_mode)

            self.single_repeat_button = ft.IconButton(
                icon=ft.Icons.REPEAT_ONE_ON if self.single_repeat_mode else ft.Icons.REPEAT_ONE, on_click=self.toggle_single_repeat, icon_size=24, tooltip="单曲循环", selected=self.single_repeat_mode
            )

            control_buttons = ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, on_click=self.previous_song, icon_size=24, icon_color=self.theme_colors.accent_color, tooltip="上一首 快捷键:左"),
                    self.play_button,
                    ft.IconButton(icon=ft.Icons.SKIP_NEXT, on_click=self.next_song, icon_size=24, icon_color=self.theme_colors.accent_color, tooltip="下一首 快捷键:右"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )

            additional_controls = ft.Row(controls=[self.shuffle_button, self.repeat_button, self.single_repeat_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

            # Create a ListView for playlists
            self.playlist_list = ft.ListView(
                controls=[
                    ft.ListTile(
                        title=ft.Text(playlist_name, color=self.theme_colors.accent_color if playlist_name == self.current_playlist else None),
                        bgcolor=self.theme_colors.card_color if playlist_name == self.current_playlist else "transparent",
                        on_click=lambda e, playlist_name=playlist_name: self.show_playlist(playlist_name),
                    )
                    for playlist_name in ["所有歌曲"] + list(self.playlists.keys())
                ],
                expand=True,
                width=150,  # Adjust width as needed
            )

            # Placeholder for the current playlist's songs
            self.current_playlist_view = ft.ListView(
                controls=[],
                expand=True,
                width=250,  # Adjust width as needed
            )

            self.show_playlist(self.current_playlist)

            player_bar = ft.Container(
                content=ft.Row(
                    controls=[
                        self.album_cover,
                        ft.Column(
                            controls=[
                                self.current_song_text,
                                self.current_song_singer,
                                self.current_song_album,
                                self.refresh_button,
                            ],
                            width=150,
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(controls=[ft.Container(), control_buttons, ft.Row([self.mute_button, self.volume_slider])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                                ft.Row(controls=[self.progress, self.time_display, additional_controls], spacing=10, alignment=ft.MainAxisAlignment.CENTER, expand=True),
                            ],
                            spacing=5,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                padding=10,
                bgcolor=self.theme_colors.card_color,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
            )

            playlist_with_lyrics = ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("播放列表", size=20, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=self.playlist_list,
                                        padding=ft.padding.only(right=10),
                                    ),
                                    self.current_playlist_view,
                                ],
                                expand=True,
                            ),
                        ],
                        expand=True,
                    ),
                    # 竖向分割线
                    ft.VerticalDivider(1),
                    ft.Container(
                        content=self.lyrics_text,
                        alignment=ft.alignment.center_left,
                        width=400,
                        padding=ft.padding.only(left=10),
                    ),
                ],
                expand=True,
            )

            # 注册快捷键
            self.page.on_keyboard_event = self.register_shortcuts
            self.page.run_task(self.async_update_lyrics_and_cover)

            return ft.Column(
                controls=[
                    ft.Container(
                        content=playlist_with_lyrics,
                        expand=True,
                        padding=20,
                        border_radius=ft.border_radius.all(10),
                    ),
                    player_bar,
                ],
                spacing=0,
                expand=True,
            )
        except Exception as e:
            print(f"构建播放器界面时出错: {str(e)}")
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("构建播放器界面时出错", size=20, color=self.theme_colors.accent_color),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )

    def build_playlist(self, playlist_name):
        if playlist_name == "所有歌曲":
            songs = self.all_songs
        else:
            songs = self.playlists.get(playlist_name, [])

        return ft.ListView(
            controls=[
                ft.ListTile(title=ft.Text(f"{i + 1}. {format_song_name(os.path.basename(song))}"), on_click=lambda e, song=song, playlist_name=playlist_name: self.select_song(e, song, playlist_name))
                for i, song in enumerate(songs)
            ],
            expand=True,
        )

    # Update select_song to highlight the current song
    def select_song(self, e, song_path):
        """选择并播放歌曲"""
        try:
            # 获取绝对路径
            song_path = os.path.abspath(song_path)

            # 根据当前播放列表更新索引
            if self.current_playlist == "所有歌曲":
                all_songs_paths = [os.path.abspath(song) for song in self.all_songs]
                if song_path in all_songs_paths:
                    self.current_index = all_songs_paths.index(song_path)
            else:
                playlist_paths = [os.path.abspath(song) for song in self.playlists[self.current_playlist]]
                if song_path in playlist_paths:
                    self.current_index = playlist_paths.index(song_path)

            # 设置新歌曲
            self.set_new_song()

            # 更新列表视图中的高亮显示
            for tile in self.current_playlist_view.controls:
                tile.bgcolor = "transparent"
                tile.title.color = None

            # 找到并高亮当前播放的歌曲
            current_song_name = format_song_name(os.path.basename(self.get_current_song()))
            for tile in self.current_playlist_view.controls:
                if tile.title.value.split(". ", 1)[1] == current_song_name:
                    tile.bgcolor = self.theme_colors.card_color
                    tile.title.color = self.theme_colors.accent_color
                    break

            self.page.update()

        except Exception as e:
            print(f"选择歌曲时出错: {str(e)}")

    def seek(self, e):
        """跳转进度"""
        if self.audio.src and self.audio.get_duration() > 0:
            # 确保进度值在0-1之间
            progress = max(0, min(self.progress.value, 1.0))
            position = int(progress * self.audio.get_duration())
            self.audio.seek(position)
            self.update_time_display(position, self.audio.get_duration())
            self.page.update()

    def set_volume(self, e):
        """设置音量"""
        try:
            # 使用滑块的value属性并四舍五入到2位小数
            volume = round(self.volume_slider.value, 2)
            # 确保音量在0-1之间
            volume = max(0.0, min(1.0, volume))
            
            if self.audio:
                self.audio.volume = volume
                self.app.config.set("Music", "volume", volume)
                print(f"音量已设置为: {volume:.2f}")
                # 更新滑块显示值，确保显示的也是2位小数
                self.volume_slider.value = volume
                self.update()
                
        except Exception as err:
            print(f"设置音量时出错: {str(err)}")
            # 恢复到之前保存的音量值
            self.volume_slider.value = round(self.app.config.Music.volume, 2)
            self.update()

    def update_time_display(self, position, duration):
        self.time_display.value = f"{self.format_time(position)} / {self.format_time(duration)}"
        self.page.update()

    def format_time(self, milliseconds):
        """格式化时间"""
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_progress_ui(self, e):
        """更新进度条"""
        if self.audio and self.audio.src:
            duration = self.audio.get_duration()
            if duration > 0:
                position = self.audio.get_current_position()
                # 确保进度值不超过最大值
                progress = min(position / duration, 1.0)
                self.progress.value = progress
                self.update_time_display(position, duration)

                # Update lyrics display based on current position
                self.update_lyrics_display(position)

                self.page.update()

    def update_play_state(self, e):
        """更新播放状态"""
        if e.data == "completed":
            # 重置进度条
            self.progress.value = 0
            self.page.update()

            if self.single_repeat_mode:
                # 单曲循环模式下，重新播放当前歌曲
                self.audio.seek(0)
                self.audio.play()
            elif not self.repeat_mode:
                # 非重复模式下，播放下一首
                self.next_song(e)
        self.page.update()

    def toggle_single_repeat(self, e):
        """切换单曲循环模式"""
        self.single_repeat_mode = not self.single_repeat_mode
        self.single_repeat_button.selected = self.single_repeat_mode
        self.single_repeat_button.icon = ft.Icons.REPEAT_ONE_ON if self.single_repeat_mode else ft.Icons.REPEAT_ONE
        self.app.config.set("Music", "single_repeat_mode", self.single_repeat_mode)
        self.page.update()

    def toggle_shuffle(self, e):
        """切换随机播放模式"""
        self.shuffle_mode = not self.shuffle_mode
        self.shuffle_button.selected = self.shuffle_mode
        self.shuffle_button.icon = ft.Icons.SHUFFLE_ON if self.shuffle_mode else ft.Icons.SHUFFLE
        self.app.config.set("Music", "shuffle_mode", self.shuffle_mode)
        self.page.update()

    def toggle_repeat(self, e):
        """切换列表循环模式"""
        self.repeat_mode = not self.repeat_mode
        self.repeat_button.selected = self.repeat_mode
        self.repeat_button.icon = ft.Icons.REPEAT_ON if self.repeat_mode else ft.Icons.REPEAT
        self.app.config.set("Music", "repeat_mode", self.repeat_mode)
        self.page.update()

    def switch_playlist(self, e):
        """切换播放列表"""
        self.current_playlist = e.control.value
        self.current_index = 0  # Reset to the first song when switching playlists
        self.update()

    def refresh_song_metadata(self, e):
        """重新加载当前歌曲的元数据"""
        print("重新加载当前歌曲的元数据")
        self.page.run_task(self.async_update_lyrics_and_cover, increment_index=True)
        self.page.update()

    def register_shortcuts(self, e: ft.KeyboardEvent):
        """注册快捷键"""
        if self.app.current_page.title == self.title:
            if e.key == "Arrow Right":
                self.next_song(e)
            elif e.key == "Arrow Left":
                self.previous_song(e)
            elif e.key == " ":  # 空格键
                self.toggle_play_pause(e)
            elif e.key == "M":  # 按下m键
                self.toggle_mute(e)
            elif e.key == "Arrow Up":
                self.volume_slider.value += 0.1
                self.set_volume(e)
            elif e.key == "Arrow Down":
                self.volume_slider.value -= 0.1
                self.set_volume(e)
    
    def toggle_mute(self, e):
        """切换静音状态"""
        self.mute = not self.mute
        self.mute_button.icon = ft.Icons.VOLUME_OFF if self.mute else ft.Icons.VOLUME_UP
        self.audio.volume = 0 if self.mute else self.app.config.Music.volume
        self.volume_slider.value = 0 if self.mute else self.app.config.Music.volume
        self.show_notification(f"静音状态已切换为: {'静音' if self.mute else '非静音'}")
        self.page.update()
