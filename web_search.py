from ddgs import DDGS
from crawl4ai import AsyncWebCrawler
import asyncio

def duckduckgo_search(query, max_results=5): # You can change how many web sources are scraped per search request from here 
    results = []
    print("I searched : " + query + " in the web")
    try:
        with DDGS() as ddgs: # creates a DuckDuckGo search client and automatically cleans it up when finished
            for r in ddgs.text( # ddgs.text() contains the results
                f"{query}",
                max_results=max_results
            ):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body")
                })
    except Exception as e:
        print(f"[WARN] DuckDuckGo search failed: {e}")
    return results

async def crawl_urls(urls):
    async with AsyncWebCrawler() as crawler:

        async def fetch(url):
            try:
                result = await crawler.arun(url=url)
                if result.success:
                    return result.markdown[:800]
            except Exception as e:
                print(f"[WARN] Crawl failed for {url}: {e}")
            return None

        tasks = [fetch(url) for url in urls]
        return await asyncio.gather(*tasks)


def search_and_crawl(query, max_results=5):
    search_results = duckduckgo_search(query, max_results=max_results)
    urls = [r["url"] for r in search_results]

    contents = asyncio.run(crawl_urls(urls))

    return [
        {
            "title": r["title"],
            "url": r["url"],
            "snippet": r["snippet"],
            "full_content": c
        }
        for r, c in zip(search_results, contents)
    ]

def build_web_context(web_results):
    if not web_results:
        return ""
    parts = []
    for r in web_results:
        content = r.get("full_content") or r.get("snippet") or ""
        parts.append(f"[Web] {r['title']}\nURL: {r['url']}\n{content[:3000]}")
    return "\n---\n".join(parts) # the seperator is --- on its own line