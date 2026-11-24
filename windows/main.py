import os
import sys
import webview
import json

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    exe_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    exe_dir = base_dir

sys.path.append(base_dir)

from Fetcher.fetcher import search_music, get_audio_url, download_music, list_offline_music

html_path = os.path.join(base_dir, 'interface', 'index.html')
playlists_path = os.path.join(exe_dir, 'playlisty.json')

class Api:
    def search(self, query, page=1):
        return search_music(query, page)

    def get_stream(self, video_id):
        return get_audio_url(video_id)

    def download_offline(self, video_id, title):
        return download_music(video_id, title)

    def get_offline_tracks(self):
        return list_offline_music()

    def save_playlists(self, data):
        with open(playlists_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True

    def load_playlists(self):
        if os.path.exists(playlists_path):
            with open(playlists_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"Ulubione": []}

webview.create_window('Decibel', html_path, js_api=Api(), width=1100, height=700)
webview.start()
