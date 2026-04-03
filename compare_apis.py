import httpx
import asyncio

async def fetch_shortmax():
    url = "https://shortmax.dramabos.my.id/api/v1/popular"
    params = {"lang": "id", "page": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        if r.status_code == 200:
            return r.json().get("data", {}).get("list", [])
        return []

async def fetch_goodshort():
    url = "https://goodshort.dramabos.my.id/home"
    params = {"lang": "in", "channel": "-1", "page": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        if r.status_code == 200:
            data = r.json().get("data", {})
            records = data.get("records", [])
            items = []
            for rec in records:
                items.extend(rec.get("items", []))
            return items
        return []

async def main():
    sm = await fetch_shortmax()
    gs = await fetch_goodshort()
    
    print(f"Shortmax items: {len(sm)}")
    print(f"GoodShort items: {len(gs)}")
    
    sm_titles = set(d.get("bookName") or d.get("title") for d in sm)
    gs_titles = set(d.get("bookName") or d.get("title") for d in gs)
    
    only_sm = sm_titles - gs_titles
    print(f"Titles only in Shortmax: {len(only_sm)}")
    for t in list(only_sm)[:5]:
        print(f" - {t}")

if __name__ == "__main__":
    asyncio.run(main())
