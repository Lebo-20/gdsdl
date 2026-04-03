import httpx
import asyncio
import json

async def test_home():
    BASE_URL = "https://goodshort.dramabos.my.id"
    url = f"{BASE_URL}/home"
    params = {
        "lang": "in",
        "channel": "-1",
        "page": 1,
        "size": 50
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params)
        data = response.json()
        raw_data = data.get("data", {})
        if isinstance(raw_data, dict):
            records = raw_data.get("records", [])
            for i, rec in enumerate(records):
                inner_data = rec.get("data", [])
                if inner_data:
                    title = rec.get("title") or "Untitled Section"
                    print(f"[{i}] {title}: Data items: {len(inner_data)}")
                    for item in inner_data[:2]:
                         name = item.get("bookName") or item.get("tags")
                         print(f"  - {name}")

if __name__ == "__main__":
    asyncio.run(test_home())
