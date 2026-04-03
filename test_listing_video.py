import asyncio
from api import get_all_episodes
import json

async def main():
    bid = "31001267802" # A new drama with locks at 15+
    eps = await get_all_episodes(bid)
    
    if len(eps) > 15:
        ep15 = eps[15]
        print(f"Episode {ep15.get('index')} (ID: {ep15.get('id')}):")
        print(f"MultiVideos: {len(ep15.get('multiVideos', []))}")
        print(f"CDN: {ep15.get('cdn')}")
        
        if not ep15.get('multiVideos') and not ep15.get('cdn'):
            print("Video data MISSING in chapters API for episode 15+.")
        else:
            print("Video data FOUND in chapters API for episode 15+.")

if __name__ == "__main__":
    asyncio.run(main())
