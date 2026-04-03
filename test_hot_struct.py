import httpx
import asyncio
import json

async def test_hot():
    BASE_URL = "https://goodshort.dramabos.my.id"
    url = f"{BASE_URL}/hot"
    params = {"lang": "in"}
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params)
        data = response.json()
        print(f"Hot Success: {data.get('success')}")
        raw_data = data.get("data")
        print(f"Hot Data type: {type(raw_data)}")
        if isinstance(raw_data, list):
            print(f"Hot List length: {len(raw_data)}")
            if len(raw_data) > 0:
                 print(f"Hot First item keys: {raw_data[0].keys() if isinstance(raw_data[0], dict) else 'Not a dict'}")

if __name__ == "__main__":
    asyncio.run(test_hot())
