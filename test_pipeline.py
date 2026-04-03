import asyncio
import os
import tempfile
import shutil
from api import get_drama_detail, get_all_episodes
from downloader import download_all_episodes
from merge import merge_episodes

# A book ID from the API to test
test_book_id = "31001330007" # Already in processed.json, but we can test it anyway

async def test_run():
    print(f"Testing download for {test_book_id}...")
    
    # Detail
    detail = await get_drama_detail(test_book_id)
    if not detail:
        print("Failed to get detail.")
        return
        
    book = detail.get("book", {})
    title = book.get("bookName", f"test_{test_book_id}")
    print(f"Drama: {title}")
    
    # Episodes
    episodes = await get_all_episodes(test_book_id)
    if not episodes:
        print("No episodes found.")
        return
        
    print(f"Total episodes: {len(episodes)}")
    
    # Let's just download the first episode for speed
    test_eps = episodes[:1]
    
    temp_dir = tempfile.mkdtemp(prefix="test_bot_")
    video_dir = os.path.join(temp_dir, "episodes")
    os.makedirs(video_dir, exist_ok=True)
    
    try:
        success = await download_all_episodes(test_eps, video_dir)
        if success:
            print("Download successful!")
            output_path = os.path.join(temp_dir, "test_output.mp4")
            merge_success = merge_episodes(video_dir, output_path)
            if merge_success:
                print(f"Merge successful! Output at {output_path}")
                print(f"File size: {os.path.getsize(output_path)} bytes")
            else:
                print("Merge failed.")
        else:
            print("Download failed.")
            
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    asyncio.run(test_run())
