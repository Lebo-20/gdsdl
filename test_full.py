import httpx
import asyncio

async def test_full_response():
    BASE_URL = "https://goodshort.dramabos.my.id"
    AUTH_CODE = "A8D6AB170F7B89F2182561D3B32F390D"
    book_id = "31001276247"
    url = f"{BASE_URL}/chapters/{book_id}"
    params = {
        "lang": "in",
        "code": AUTH_CODE,
        # "size": 100 # Let's try without first
    }
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(url, params=params)
        data = response.json()
        print(f"Keys in root: {data.keys()}")
        if data.get("success"):
            data_inner = data.get("data", {})
            print(f"Keys in data: {data_inner.keys()}")
            print(f"Total entries in list: {len(data_inner.get('list', []))}")
            if "total" in data_inner:
                print(f"Declared total: {data_inner['total']}")

if __name__ == "__main__":
    asyncio.run(test_full_response())
