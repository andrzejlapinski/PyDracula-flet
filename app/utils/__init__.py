# 工具包

# 可自定义获取歌词和封面的方法

import asyncio
import os
import traceback
from typing import Dict, Optional
import aiohttp
import urllib.parse
import re
from mutagen.id3 import ID3, USLT, TIT2, TPE1, TALB, TSRC, COMM
from mutagen.id3 import ID3NoHeaderError

import aiofiles

def format_song_name(filename):
    """
    格式化歌曲名称，去除序号和扩展名
    例如：'04.白鸽乌鸦相爱的戏码.mp3' -> '白鸽乌鸦相爱的戏码'
    """
    # 先去除扩展名
    name_without_extension = filename.rsplit(".", 1)[0]
    # 去除序号（假设序号格式为：数字+点，如：01.）
    parts = name_without_extension.split(".", 1)
    if len(parts) > 1 and parts[0].isdigit():
        return parts[1].strip()
    return name_without_extension.strip()

def parse_lyrics(lyrics_text):
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

async def fetch_cover(song_name, artist_name=None):
    print(f"获取歌曲图片url: https://api.lrc.cx/cover?title={song_name}")

    encoded_name = urllib.parse.quote(song_name)
    encoded_artist = urllib.parse.quote(artist_name) if artist_name else None

    cover_url = f"https://api.lrc.cx/cover?title={encoded_name}"
    if encoded_artist:
        cover_url += f"&artist={encoded_artist}"

    async with aiohttp.ClientSession() as session:
        async with session.get(cover_url) as response:
            if response.status == 200:
                return response.url
            else:
                return "images/default_cover.jpg"

async def fetch_lyrics(song_name, artist_name=None):
    print(f"获取歌词url:    https://api.lrc.cx/lyrics?title={song_name}")

    encoded_name = urllib.parse.quote(song_name)
    encoded_artist = urllib.parse.quote(artist_name) if artist_name else None

    lyrics_url = f"https://api.lrc.cx/lyrics?title={encoded_name}"
    if encoded_artist:
        lyrics_url += f"&artist={encoded_artist}"

    async with aiohttp.ClientSession() as session:
        async with session.get(lyrics_url) as response:
            if response.status == 200:
                lyrics_text = await response.text()
                return parse_lyrics(lyrics_text)
            else:
                return [(0, "歌词未找到")]

async def fetch_lyrics_and_cover(song_name: str, artist_name: str = None):
    SEARCH_URL = "https://api.timelessq.com/music/tencent/search"
    LYRIC_URL = "https://api.timelessq.com/music/tencent/lyric"
    print(f"API: https://api.timelessq.com 获取歌词和封面: \n - 歌曲：{song_name}， \n - 歌手：{artist_name if artist_name else ''} \n")

    cover_url = "images/default_cover.jpg"
    lyrics = [(0, "歌词未找到")]

    async with aiohttp.ClientSession() as session:
        try:
            # Search for the song
            async with session.get(SEARCH_URL, params={"keyword": song_name}) as search_response:
                search_data: Dict = await search_response.json()
                first_song = search_data.get("data", {}).get("list", [])[0]
                songmid = first_song.get("songmid", None)
                cover_url = first_song.get("albumcover", cover_url)

                if not songmid:
                    print("未找到 songmid")
                    return cover_url, lyrics

            # Fetch lyrics using songmid
            async with session.get(LYRIC_URL, params={"songmid": songmid}) as lyric_response:
                lyric_data: Dict = await lyric_response.json()
                lyric = lyric_data.get("data", {}).get("lyric")
                lyrics = parse_lyrics(lyric) if lyric else [(0, "歌词未找到")]

        except Exception as e:
            traceback.print_exc()
            print(f"获取歌词和封面失败: {e}")

    return cover_url, lyrics


async def download_cover(session: aiohttp.ClientSession, url: str) -> Optional[bytes]:
    """异步下载专辑封面"""
    if not url:
        return None
        
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"封面下载失败，状态码：{response.status}")
                return None
                
            if 'image/' not in response.headers.get('Content-Type', ''):
                print("响应内容不是图片类型")
                return None
                
            return await response.read()
            
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"封面下载异常: {str(e)}")
        return None

async def save_lyrics(song_path: str, lyrics: str) -> Optional[str]:
    """保存歌词到本地文件"""
    try:
        lyrics_dir = os.path.dirname(song_path)
        os.makedirs(lyrics_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(song_path))[0]
        lyric_path = os.path.join(lyrics_dir, f"{base_name}.lrc")
        
        async with aiofiles.open(lyric_path, "w", encoding="utf-8") as f:
            await f.write(lyrics)
            
        return lyric_path
        
    except Exception as e:
        print(f"歌词保存失败: {str(e)}")
        return None

async def update_song_metadata(song_name: str, song_path: str, increment_index: bool = False) -> Optional[dict]:
    """
    完整元数据更新流程
    Args:
        song_name: 歌曲名称
        song_path: 歌曲文件路径
        increment_index: 是否递增index选择下一个搜索结果，默认False
    Returns:
        包含更新结果的字典，包括元数据信息
    TSRC格式: "index:songmid" 例如 "0:12345678"
    """
    # 前置检查
    if not os.path.exists(song_path):
        print(f"文件路径不存在: {song_path}")
        return None

    try:
        # 读取当前的TSRC信息，获取上一次的index
        current_index = 0
        try:
            audio = ID3(song_path)
            if "TSRC" in audio:
                tsrc_data = audio["TSRC"].text[0]
                if ":" in tsrc_data:
                    current_index = int(tsrc_data.split(":")[0])
                    if increment_index:
                        current_index += 1  # 只有在increment_index为True时才递增
        except (ID3NoHeaderError, ValueError, IndexError):
            pass

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            # 搜索歌曲
            search_url = "https://api.timelessq.com/music/tencent/search"
            async with session.get(search_url, params={"keyword": song_name}) as resp:
                if resp.status != 200:
                    print(f"搜索失败: {resp.status}")
                    return None
                    
                data = await resp.json()
                song_list = data.get("data", {}).get("list", [])

                if not song_list:
                    print("无搜索结果")
                    return None

            # 如果current_index超出列表范围，重置为0
            if current_index >= len(song_list):
                current_index = 0
                
            song = song_list[current_index]
            songmid = song.get("songmid")
            if not songmid:
                print("缺少 songmid")
                return None

            # 获取封面URL
            cover_url = song.get("albumcover", "")

            # 获取歌词
            lyric_url = f"https://api.timelessq.com/music/tencent/lyric?songmid={songmid}"
            lyric_text = ""
            try:
                async with session.get(lyric_url) as resp:
                    if resp.status == 200:
                        lyric_data = await resp.json()
                        lyric_text = lyric_data.get("data", {}).get("lyric", "")
            except Exception as e:
                print(f"歌词获取失败: {str(e)}")

            # 保存歌词
            lyric_path = await save_lyrics(song_path, lyric_text) if lyric_text else None

            # 更新ID3标签
            try:
                try:
                    audio = ID3(song_path)
                except ID3NoHeaderError:
                    audio = ID3()

                # 使用Frame对象设置标签
                audio.add(TIT2(encoding=3, text=[song.get("songname", "")]))     # 标题
                audio.add(TPE1(encoding=3, text=[s["name"] for s in song.get("singer", [])]))  # 艺术家
                audio.add(TALB(encoding=3, text=[song.get("albumname", "")]))    # 专辑
                # 存储index和songmid
                audio.add(TSRC(encoding=3, text=[f"{current_index}:{songmid}"]))  # 索引:ISRC

                # 添加封面URL作为注释
                if cover_url:
                    audio.add(COMM(
                        encoding=3,
                        lang='eng',
                        desc='CoverURL',
                        text=cover_url
                    ))

                # 添加歌词
                if lyric_text:
                    audio.add(USLT(
                        encoding=3,
                        lang='chi',
                        desc='Lyrics',
                        text=lyric_text
                    ))

                audio.save(song_path)
                print(f"元数据更新成功: {song['songname']}, 歌词路径: {lyric_path}")
                print(f"当前选择的是第 {current_index + 1}/{len(song_list)} 个搜索结果")    
                return {
                    "title": song.get("songname", ""),
                    "artist": ", ".join(s["name"] for s in song.get("singer", [])),
                    "album": song.get("albumname", ""),
                    "isrc": f"{current_index}:{songmid}",
                    "cover_url": cover_url,
                    "lyrics": lyric_text
                }

            except Exception as e:
                traceback.print_exc()
                print(f"ID3标签更新失败: {str(e)}")
                return None

    except Exception as e:
        print(f"处理流程异常: {str(e)}")
        return None

async def read_song_metadata(song_path: str, increment_index: bool = False) -> Optional[dict]:
    """
    读取歌曲元数据，如果元数据不存在则从API获取并更新。
    Args:
        song_path: 歌曲文件路径
        increment_index: 是否递增index选择下一个搜索结果，默认False
    Returns:
        包含元数据的字典
    """
    if not os.path.exists(song_path):
        print(f"文件不存在: {song_path}")
        return None

    try:
        audio = ID3(song_path)
    except ID3NoHeaderError:
        audio = None
    except Exception as e:
        print(f"读取ID3失败: {str(e)}")
        return None

    metadata = {
        "title": "",
        "artist": "",
        "album": "",
        "isrc": "",
        "cover_url": "",
        "lyrics": ""
    }
    
    if audio and not increment_index:
        # 读取基础元数据
        try:
            metadata["title"] = audio["TIT2"].text[0] if "TIT2" in audio else ""
            metadata["artist"] = ", ".join(audio["TPE1"].text) if "TPE1" in audio else ""
            metadata["album"] = audio["TALB"].text[0] if "TALB" in audio else ""
            metadata["isrc"] = audio["TSRC"].text[0] if "TSRC" in audio else ""
            
            # 读取封面URL
            try:
                for comm in audio.getall("COMM"):
                    if comm.desc == "CoverURL":
                        metadata["cover_url"] = comm.text[0]
                        break
            except Exception as e:
                print(f"读取封面URL失败: {str(e)}")

            # 读取歌词
            if "USLT::'eng'" in audio:
                metadata["lyrics"] = audio["USLT::'eng'"].text
            elif "USLT::'chi'" in audio:
                metadata["lyrics"] = audio["USLT::'chi'"].text
            else:
                uslt = audio.getall("USLT")
                if uslt:
                    metadata["lyrics"] = uslt[0].text

            # 如果所有必要的元数据都存在，直接返回
            if all([metadata["title"], metadata["artist"], metadata["album"], metadata["isrc"], metadata["cover_url"], metadata["lyrics"]]):
                return metadata

        except KeyError as e:
            print(f"缺失标签: {str(e)}")

    # 如果需要更新元数据（increment_index=True 或 元数据不完整）
    filename = os.path.basename(song_path)
    song_name = format_song_name(filename)
    
    # 直接从API获取新的元数据
    return await update_song_metadata(song_name, song_path, increment_index)