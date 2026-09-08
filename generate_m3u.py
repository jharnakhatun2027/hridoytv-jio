import requests

API_URL = "https://sports.hridoytv.workers.dev"

def fetch_and_generate():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=20)
        response.raise_for_status()
        content = response.text

        # যদি Cloudflare HTML পেজ রিটার্ন করে
        if "<!DOCTYPE html>" in content or "<html" in content:
            print("Error: Cloudflare blocked the request with HTML page.")
            return

        lines = content.splitlines()
        new_m3u = []
        
        for line in lines:
            new_m3u.append(line)
            # চ্যানেল লিংকের সাথে User-Agent হেডার যুক্ত করা
            if line.startswith("#EXTINF"):
                new_m3u.append('#EXTVLCOPT:http-user-agent="Mozilla/5.0"')

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(new_m3u))
            
        print("playlist.m3u updated with headers.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_generate()
