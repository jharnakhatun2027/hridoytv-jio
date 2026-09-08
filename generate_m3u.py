import requests

# আপনার Worker ও মূল সার্ভারের তথ্য
API_URL = "https://sports.hridoytv.workers.dev/playlist.m3u"
WORKER_URL = "https://sports.hridoytv.workers.dev"
ORIGINAL_SERVER = "http://live.balajibroadband.com:3500"

def fetch_and_generate():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=25)
        response.raise_for_status()
        
        content = response.text
        
        # M3U ফাইলের ভেতরের সব সরাসরি সার্ভার লিঙ্ক আপনার Cloudflare Worker দিয়ে রিপ্লেস করা
        content = content.replace(ORIGINAL_SERVER, WORKER_URL)
        content = content.replace("http://live.balajibroadband.com", WORKER_URL)
        
        # প্লেলিস্টে যদি হেডার না থাকে তবে User-Agent ফোর্সেবলি যোগ করার চেষ্টা করা
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("playlist.m3u updated with proxied stream URLs successfully!")

    except Exception as e:
        print(f"Error fetching and modifying M3U: {e}")

if __name__ == "__main__":
    fetch_and_generate()
