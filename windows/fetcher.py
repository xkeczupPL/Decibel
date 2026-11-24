import os
import sys
import re
import yt_dlp

if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
else:
    exe_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

OFFLINE_FOLDER = os.path.join(exe_dir, 'offline_music')
os.makedirs(OFFLINE_FOLDER, exist_ok=True)

def search_music(query, page=1):
    ile = page * 10
    start = (page - 1) * 10
    ydl_opts = {'quiet': True, "extract_flat": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{ile}:{query}", download=False)
        results = []
        for entry in info['entries'][start:ile]:
            results.append({
                "title": entry.get("title"),
                "url": entry.get("url"),
                "artist": entry.get("channel") or entry.get("uploader") or ""
            })
        return results

def get_audio_url(video_id):
    if not video_id.startswith("http"):
        video_id = f"https://youtube.com/watch?v={video_id}"
    ydl_opts = {'quiet': True, "format": 'bestaudio/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_id, download=False)
        return {
            "url": info['url'],
            "artist": info.get('artist') or info.get('uploader') or "",
            "track": info.get('track') or info.get('title') or ""
        }

def download_music(video_id, title):
    if not video_id.startswith("http"):
        video_id = f"https://youtube.com/watch?v={video_id}"
    czysta_nazwa = re.sub(r'[\\/*?:"<>|]', "", title)
    sciezka = os.path.join(OFFLINE_FOLDER, f"{czysta_nazwa}.%(ext)s")
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': sciezka
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_id])
    return True

def list_offline_music():
    tracks = []
    for plik in os.listdir(OFFLINE_FOLDER):
        if plik.lower().endswith(('.m4a', '.mp3', '.webm', '.opus', '.ogg')):
            pelna_sciezka = os.path.abspath(os.path.join(OFFLINE_FOLDER, plik))
            file_url = 'file:///' + pelna_sciezka.replace('\\', '/')
            tracks.append({
                "title": os.path.splitext(plik)[0],
                "url": file_url
            })
    return tracks
