import requests
import json

API_URL = "https://sports.hridoytv.workers.dev"

def fetch_and_generate():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError:
            # যদি এপিআই সরাসরি m3u ফরম্যাট প্রদান করে
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Direct M3U response saved.")
            return

        m3u_content = ["#EXTM3U\n"]
        
        # JSON অ্যারে অথবা অবজেক্ট থেকে চ্যানেল লিস্ট এক্সট্র্যাক্ট করা
        channels = data if isinstance(data, list) else data.get("channels", data.get("data", []))
        
        for ch in channels:
            name = ch.get("name") or ch.get("title") or "Unknown Channel"
            logo = ch.get("logo") or ch.get("icon") or ""
            group = ch.get("group") or ch.get("category") or "Sports"
            url = ch.get("url") or ch.get("link") or ch.get("stream") or ""
            
            if url:
                m3u_content.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n')

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.writelines(m3u_content)
            
        print("playlist.m3u successfully generated!")

    except Exception as e:
        print(f"Error fetching channel data: {e}")

if __name__ == "__main__":
    fetch_and_generate()
