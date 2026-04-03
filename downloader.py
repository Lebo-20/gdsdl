import os
import asyncio
import subprocess
import logging
from api import get_play_url

logger = logging.getLogger(__name__)

async def download_m3u8(url: str, output_path: str, retries: int = 3):
    """
    Downloads M3U8 stream to a single MP4 file using FFmpeg with internal retry mechanism
    and headers for bypassing duration limits and protection.
    """
    # Essential FlickReels headers for full duration bypass
    headers_str = (
        "Referer: https://www.flickreels.net/\r\n"
        "Origin: https://www.flickreels.net/\r\n"
    )
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"

    for attempt in range(1, retries + 1):
        try:
            command = [
                "ffmpeg", "-y",
                "-headers", headers_str,
                "-user_agent", user_agent,
                "-i", url,
                "-c", "copy",
                "-bsf:a", "aac_adtstoasc",
                "-loglevel", "error",
                output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return True
            
            error_msg = stderr.decode().strip()
            logger.warning(f"Attempt {attempt} failed for {output_path}: {error_msg}")
        except Exception as e:
            logger.error(f"Error on attempt {attempt} downloading {output_path}: {e}")
        
        if attempt < retries:
            # Wait with exponential backoff (2, 4, 6 seconds)
            await asyncio.sleep(2 * attempt)
            
    return False

async def download_all_episodes(episodes: list, download_dir: str, semaphore_count: int = 3):
    """
    Downloads all episodes concurrently.
    Ensures consistent mapping of episode data to filenames via local function parameters.
    """
    os.makedirs(download_dir, exist_ok=True)
    semaphore = asyncio.Semaphore(semaphore_count)

    async def single_task(ep_data: dict):
        """
        Local function that processes one episode independently.
        """
        # Ensure we bind local values early to avoid race conditions/leaks
        current_index = ep_data.get('index', 0)
        book_id = ep_data.get('bookId')
        chapter_id = ep_data.get('id')
        
        # Format filename using local index
        ep_num_str = str(current_index).zfill(3)
        filename = f"episode_{ep_num_str}.mp4"
        filepath = os.path.join(download_dir, filename)

        async with semaphore:
            logger.info(f"🚀 Downloading episode {current_index} → {filename}")
            
            # Extract URL or fetch if missing (locked)
            multi_videos = ep_data.get('multiVideos', [])
            cdn_url = ep_data.get('cdn')
            final_url = None

            if not multi_videos and not cdn_url and book_id and chapter_id:
                logger.info(f"Fetching play URL for locked episode {current_index}...")
                play_info = await get_play_url(chapter_id, book_id)
                if play_info:
                    multi_videos = play_info.get('multiVideos', [])
                    cdn_url = play_info.get('cdn')

            # Quality selection logic
            if multi_videos:
                # Prioritize 720p or 1080p
                best = next((v for v in multi_videos if v.get('type') == '720p'), None)
                if not best:
                    best = next((v for v in multi_videos if v.get('type') == '1080p'), None)
                if not best:
                    best = multi_videos[0]
                final_url = best.get('filePath') or best.get('url')
            elif cdn_url:
                final_url = cdn_url

            if not final_url:
                logger.error(f"❌ No URL found for episode {current_index}")
                return False

            # Wrap URL in local Node.js Proxy to bypass duration and CORS locks
            # The proxy ensures all headers and segments are handled correctly
            proxied_url = f"http://localhost:3000/proxy?url={final_url}"
            
            # Execute download with retry logic
            success = await download_m3u8(proxied_url, filepath)
            
            if success:
                logger.info(f"✅ Downloaded: {filename}")
            else:
                logger.error(f"❌ FAILED after retries: {filename}")
            
            return success

    # Use explicit task creation to bind 'ep' correctly to each 'single_task' call
    tasks = [single_task(ep) for ep in episodes]
    results = await asyncio.gather(*tasks)
    
    return all(results)
