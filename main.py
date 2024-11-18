import asyncio
import json
import sys
import os
from playwright.async_api import async_playwright
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


async def search_flights(origin, destination, date):
    url = f"https://www.kayak.com/flights/{origin}-{destination}/{date}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, wait_until="networkidle")

        # Wait for and accept cookies if the banner appears
        try:
            await page.click('[id^=onetrust-accept]', timeout=5000)
        except:
            print("No cookie banner found or couldn't be clicked.")

        # Wait for flight results to load
        await page.wait_for_selector('div[data-resultid]', timeout=60000)

        # Scroll to load all results
        for _ in range(5):  # Adjust the number of scrolls as needed
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(2)

        # Extract flight data
        flights = await page.evaluate('''
            () => {
                const flightElements = document.querySelectorAll('div[data-resultid]');
                return Array.from(flightElements).map(el => {
                    return {
                        airline: el.querySelector('div[dir="auto"]')?.textContent.trim(),
                        times: el.querySelector('.vmXl-mod-variant-large')?.textContent.trim(),
                        price: el.querySelector('.f8F1-price-text')?.textContent.trim(),
                        stops: el.querySelector('.JWEO-stops-text')?.textContent.trim(),
                        layover_airport: el.querySelector('.JWEO .c_cgF-mod-variant-default span')?.textContent.trim(),
                        duration: el.querySelector('.xdW8 .vmXl-mod-variant-default')?.textContent.trim(),
                        origin: el.querySelector('.EFvI div:first-child span')?.textContent.trim(),
                        destination: el.querySelector('.EFvI div:last-child span')?.textContent.trim(),
                        fare_type: el.querySelector('.DOum-name')?.textContent.trim(),
                        provider: el.querySelector('.M_JD-provider-name')?.textContent.trim()
                    };
                });
            }
        ''')
        # Capture a screenshot
        await page.screenshot(path=f"debug_files/flight_search_{origin}_{destination}_{date}.png")
        # Save the HTML content
        html_content = await page.content()
        with open(f"debug_files/flight_search_{origin}_{destination}_{date}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        await browser.close()
        return flights


def main():
    if len(sys.argv) != 4:
        print("Usage: python flight_scraper.py ORIGIN DESTINATION DATE")
        print("Example: python flight_scraper.py NYC LAX 2024-12-01")
        sys.exit(1)

    origin = sys.argv[1]
    destination = sys.argv[2]
    date = sys.argv[3]

    flights = asyncio.run(search_flights(origin, destination, date))

    if flights:
        output_file = 'flight_list.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Flight List\n\n")
            for idx, flight in enumerate(flights, 1):
                f.write(f"## Flight {idx}\n")
                f.write(f"- **Airline:** {flight.get('airline', 'N/A')}\n")
                f.write(f"- **Times:** {flight.get('times', 'N/A')}\n")
                f.write(f"- **Duration:** {flight.get('duration', 'N/A')}\n")
                f.write(f"- **Origin:** {flight.get('origin', 'N/A')}\n")
                f.write(f"- **Destination:** {flight.get('destination', 'N/A')}\n")
                f.write(f"- **Stops:** {flight.get('stops', 'N/A')}\n")
                f.write(f"- **Layover Airport:** {flight.get('layover_airport', 'N/A')}\n")
                f.write(f"- **Price:** {flight.get('price', 'N/A')}\n")
                f.write(f"- **Fare Type:** {flight.get('fare_type', 'N/A')}\n")
                f.write(f"- **Provider:** {flight.get('provider', 'N/A')}\n\n")
        print(f"Flight list saved to '{output_file}'.")
    else:
        print("No flights found or an error occurred.")


if __name__ == "__main__":
    main()
