import httpx
import asyncio
import json

async def test_home_raw():
    BASE_URL = "https://goodshort.dramabos.my.id"
    url = f"{BASE_URL}/home"
    params = {
        "lang": "in",
        "channel": "-1",
        "page": 1,
        "size": 20
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, params=params)
        data = response.json()
        print(f"Success: {data.get('success')}")
        # Save to file to inspect
        with open("home_raw.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Raw saved to home_raw.json")

if __name__ == "__main__":
    asyncio.run(test_home_raw())
