import requests

API_URL = "https://sports.hridoytv.workers.dev/playlist.m3u"
WORKER_DOMAIN = "sports.hridoytv.workers.dev"
ORIGINAL_DOMAIN = "live.balajibroadband.com:3500"

def generate_custom_m3u():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=25)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        new_m3u = []
        
        for line in lines:
            # অরিজিনাল সার্ভার ডোমেইন বদলে আপনার Worker ডোমেইন বসানো
            if ORIGINAL_DOMAIN in line:
                line = line.replace(ORIGINAL_DOMAIN, WORKER_DOMAIN)
                line = line.replace("http://", "https://")
            
            # এক্সট্রা সার্ভিস ডোমেইন থাকলে তা রূপান্তর করা
            if "live.balajibroadband.com" in line:
                line = line.replace("live.balajibroadband.com", WORKER_DOMAIN)
                line = line.replace("http://", "https://")

            # প্রতিটি চ্যানেলের জন্য প্রয়োজনীয় প্লেয়ার প্রোপার্টি যোগ করা
            if line.startswith("#EXTINF"):
                new_m3u.append(line)
                new_m3u.append('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"')
                new_m3u.append('#KODIPROP:inputstream.adaptive.manifest_type=mpd')
            else:
                new_m3u.append(line)

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
            
        print("playlist.m3u formatted for ExoPlayer / OTT Navigator successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_custom_m3u()
