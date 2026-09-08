import requests

# আপনার Worker এর মাধ্যমে টেস্ট করার M3U এন্ডপয়েন্টগুলো
ENDPOINTS = [
    "https://sports.hridoytv.workers.dev/playlist.m3u",
    "https://sports.hridoytv.workers.dev/m3u",
    "https://sports.hridoytv.workers.dev/channels.m3u"
]

def fetch_and_save():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in ENDPOINTS:
        try:
            print(f"Checking: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            
            # যদি উত্তর ২০০ হয় এবং এতে #EXTM3U লেখা থাকে
            if response.status_code == 200 and "#EXTM3U" in response.text:
                with open("playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"Success! Playlist saved from {url}")
                return
        except Exception as e:
            print(f"Error checking {url}: {e}")

    print("Error: Could not fetch valid M3U from provided endpoints.")

if __name__ == "__main__":
    fetch_and_save()
