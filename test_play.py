import asyncio
from api import get_play_url
import json

async def main():
    # Example ID for Istri CEO-ku Keren Sekali (locked episode 63)
    book_id = "31000896384"
    chapter_id = "10810156" 
    
    play_data = await get_play_url(chapter_id, book_id)
    if not play_data:
        print("No play data.")
        return
        
    print(f"Keys: {play_data.keys()}")
    multi = play_data.get("multiVideos", [])
    print(f"Multi length: {len(multi)}")
    for i, v in enumerate(multi):
        print(f"[{i}] Type: {v.get('type')}, URL: {v.get('filePath')[:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
