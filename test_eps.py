import asyncio
from api import get_hot_dramas, get_all_episodes
import json

async def main():
    hot = await get_hot_dramas()
    if not hot:
        print("No hot dramas found.")
        return
    for drama in hot[:2]:
        bid = str(drama.get("bookId") or drama.get("action"))
        name = drama.get("bookName") or drama.get("tags")
        print(f"Checking {name} ({bid})...")
        eps = await get_all_episodes(bid)
        print(f"Total episodes found: {len(eps)}")
        if eps:
             print(f"Indices: {[e.get('index') for e in eps[:20]]}")
             if len(eps) > 20:
                 print(f"Last index: {eps[-1].get('index')}")
        print("-" * 20)

if __name__ == "__main__":
    asyncio.run(main())
