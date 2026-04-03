import httpx
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://goodshort.dramabos.my.id"
AUTH_CODE = "A8D6AB170F7B89F2182561D3B32F390D"

async def get_drama_detail(book_id: str):
    url = f"{BASE_URL}/book/{book_id}"
    params = {
        "lang": "in"
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data and data.get("success"):
                return data.get("data", {})
            return None
        except Exception as e:
            logger.error(f"Error fetching drama detail for {book_id}: {e}")
            return None

async def get_all_episodes(book_id: str):
    url = f"{BASE_URL}/chapters/{book_id}"
    all_episodes = []
    page = 1
    size = 500
    
    async with httpx.AsyncClient(timeout=60) as client:
        while True:
            params = {
                "lang": "in",
                "code": AUTH_CODE,
                "page": page,
                "size": size
            }
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                if data and data.get("success"):
                    chapters_data = data.get("data", {})
                    current_list = chapters_data.get("list", [])
                    all_episodes.extend(current_list)
                    
                    # Check if we have more pages (this is a common pattern for such APIs)
                    # If current list is less than size, we probably reached the end.
                    if not current_list or len(current_list) < size:
                        break
                    page += 1
                else:
                    break
            except Exception as e:
                logger.error(f"Error fetching episodes for {book_id} at page {page}: {e}")
                break
    return all_episodes

async def get_hot_dramas():
    url = f"{BASE_URL}/hot"
    params = {"lang": "in"}
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    # Map 'action' as 'bookId' and 'tags' as 'bookName' for compatibility
                    items = data.get("data", [])
                    for item in items:
                        item["bookId"] = item.get("action")
                        item["bookName"] = item.get("tags")
                    return items
            return []
        except Exception as e:
            logger.error(f"Error fetching hot dramas: {e}")
            return []

async def get_home_dramas(page=1, size=50):
    url = f"{BASE_URL}/home"
    params = {
        "lang": "in",
        "channel": "-1",
        "page": page,
        "size": size
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    raw_data = data.get("data", {})
                    all_items = []
                    
                    # The home API returns a 'records' list, each containing an 'items' list
                    records = raw_data.get("records", [])
                    if isinstance(records, list):
                        for rec in records:
                            items = rec.get("items", [])
                            if isinstance(items, list):
                                all_items.extend(items)
                    
                    # Fallback to 'list' if records was empty or not findable
                    if not all_items:
                        all_items = raw_data.get("list", [])
                        
                    return all_items
            return []
        except Exception as e:
            logger.error(f"Error fetching popular dramas: {e}")
            return []

async def search_dramas(query: str, page=1, size=15):
    url = f"{BASE_URL}/search"
    params = {
        "lang": "in",
        "q": query,
        "page": page,
        "size": size
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("data", [])
            return []
        except Exception as e:
            logger.error(f"Error searching dramas for {query}: {e}")
            return []

async def get_play_url(chapter_id: str, book_id: str):
    url = f"{BASE_URL}/play/{chapter_id}"
    params = {
        "bookId": book_id,
        "lang": "in",
        "code": AUTH_CODE
    }
    
    headers = {
        "Referer": "https://www.flickreels.net/",
        "Origin": "https://www.flickreels.net/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data and "data" in data:
                    return data["data"]
            return None
        except Exception as e:
            logger.error(f"Error fetching play url for {chapter_id}: {e}")
            return None
