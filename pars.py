import asyncio
from playwright.async_api import async_playwright
import pandas as pd


async def scrape_hotels_page(browser, url, search_name):

    context = await browser.new_context(locale="en-EN")
    page = await context.new_page()
    
    print(f"[{search_name}] opening page")
    await page.goto(url)

    try:
        await page.click("button:has-text('/Accept all/i')", timeout=3000)
    except:
        pass

    feed = page.locator('div[role="feed"]')
    try:
        await feed.wait_for(timeout=10000)
    except Exception:
        print(f"[{search_name}] not founded")
        await context.close()
        return []


    await feed.hover()

    print(f"[{search_name}] started")

    for i in range(50):
        await page.mouse.wheel(0, 3000)
        await page.wait_for_timeout(1000)
        

        if await page.locator("text=You've reached the end of the list.").is_visible():
            print(f" [{search_name}] Reached the end {i}")
            break

    card_links = feed.locator("a.hfpxzc")
    count = await card_links.count()
    print(f"[{search_name}] placec founded: {count}")
    
    cards = await card_links.all()
    if count == 0:
        print(f"[{search_name}] No cards found. HTML structures might have changed.")
    page_results = []
    
    for card in cards:
        name = await card.get_attribute("aria-label")
        link = await card.get_attribute("href")
        print(page.url)
        page_results.append({
            "category": search_name, 
            "name": name, 
            "link": link
        })
        
    await context.close()
    return page_results


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        tasks = [
            scrape_hotels_page(
                browser, 
                "https://www.google.com/maps/search/hotels+in+oslo?hl=en", 
                "At the center of Oslo"
            ),
            # scrape_hotels_page(
            #     browser, 
            #     "https://www.google.com/maps/search/hotels+in+oslo+near+airport?hl=en", 
            #     "near of the airport"
            # ),
            # scrape_hotels_page(
            #     browser, 
            #     "https://www.google.com/maps/search/budget-friendly+hotels+oslo?hl=en", 
            #     "budget-friendly hotels"
            # ),
            # scrape_hotels_page(
            #     browser, 
            #     "https://www.google.com/maps/search/spa-hotels+oslo?hl=en", 
            #     "spa hotels"
            # ),
            # scrape_hotels_page(
            #     browser, 
            #     "https://www.google.com/maps/search/lux+5+stars+oslo+hotels?hl=en", 
            #     "5 stars hotels"
            # ),
            # scrape_hotels_page(
            #     browser, 
            #     "https://www.google.com/maps/search/hostels+oslo?hl=en", 
            #     "hostels"
            # ),
            
        ]


        raw_results = await asyncio.gather(*tasks)


        final_results = []
        for result_list in raw_results:
            if result_list:
                final_results.extend(result_list)


        if final_results:
            df = pd.DataFrame(final_results)
            df = df.drop_duplicates(subset=["link"],keep="first")
            df.to_excel("hotels.xlsx", index=False)
            print(f"Succesfully saved in excel!: {len(final_results)}")
        else:
            print("no data founded")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())