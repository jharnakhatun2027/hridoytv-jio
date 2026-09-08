import requests

API_URL = "https://sports.hridoytv.workers.dev/playlist.m3u"
WORKER_BASE = "https://sports.hridoytv.workers.dev"

def build_perfect_m3u():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36",
        "Referer": "https://sports.hridoytv.workers.dev/"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=25)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        new_m3u = []
        
        user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36"
        referer = "https://sports.hridoytv.workers.dev/"
        
        for line in lines:
            if line.startswith("#EXTINF"):
                new_m3u.append(line)
                # OTT Navigator, TiviMate ও VLC প্লেয়ারের জন্য সিকিউরিটি হেডার ইনজেক্ট করা
                new_m3u.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
                new_m3u.append(f'#EXTVLCOPT:http-referrer={referer}')
                new_m3u.append(f'#EXTHTTP:{{"headers":{{"Referer":"{referer}","User-Agent":"{user_agent}"}}}}')
                new_m3u.append(f'#KODIPROP:inputstream.adaptive.stream_headers=Referer={referer}&User-Agent={user_agent}')
            elif line.strip() and not line.startswith("#"):
                url = line.strip()
                # সরাসরি সার্ভার লিংক থাকলে তা Worker লিংকে রূপান্তর করা
                if "live.balajibroadband.com:3500" in url:
                    url = url.replace("http://live.balajibroadband.com:3500", WORKER_BASE)
                elif "live.balajibroadband.com" in url:
                    url = url.replace("http://live.balajibroadband.com", WORKER_BASE)
                
                new_m3u.append(url)
            else:
                new_m3u.append(line)

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
            
        print("M3U successfully generated with stream headers!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    build_perfect_m3u()
