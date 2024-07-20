import itertools
import asyncio

import httpx
from selectolax.parser import HTMLParser


def get_cb_tasks(client: httpx.AsyncClient, pages: int, url: str):
    
    return [
        client.get(url.format(idx))
        for idx in range(pages)
    ]


def parse_cb_prices(html_text: str) -> list[dict]:
    
    parser = HTMLParser(html_text)
    
    date_tags = parser.css('div[class^=bd] div:first-child')[1:]
    dates = [date.text(strip=True) for date in date_tags]
    
    price_tags = parser.css('div[class^=bd] div:nth-child(2)')[1:]
    prices = [price.text(strip=True) for price in price_tags]
    
    return [
        {'date': date, 'price': price}
        for date, price in zip(dates, prices)
    ]


async def scrape_cb(pages: int):
    
    async with httpx.AsyncClient(timeout=30) as client:
        
        data: list[dict] = []
        
        base_url = 'https://cb.gov.sy/index.php?Last=3332&CurrentPage={}&First=0&page=list&ex=2&dir=exchangerate&lang=1&service=2&sorc=0&lt=0&act=1206'
        
        tasks = get_cb_tasks(client, pages, base_url)
        batches = itertools.batched(tasks, 5)
        
        for batch in batches:
            responses = await asyncio.gather(*batch)
            for response in responses:
                page_data = parse_cb_prices(response.text)
                data += page_data
        
        return data