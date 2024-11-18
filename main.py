import asyncio
import json
import sys
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


async def search_flights(origin, destination, date):
    url = f"https://www.kayak.com/flights/{origin}-{destination}/{date}"

    # Updated schema based on the new HTML structure
    schema = {
        "name": "Flight Results",
        "baseSelector": "li.hJSA-item",  # Updated selector to target each flight item
        "fields": [
            {"name": "airline", "selector": ".c3J0r-container .c5iUd-leg-carrier img", "type": "attr", "attr": "alt"},
            {"name": "departure_time", "selector": ".VY2U .vmXl-mod-variant-large span:nth-of-type(1)", "type": "text"},
            {"name": "arrival_time", "selector": ".VY2U .vmXl-mod-variant-large span:nth-of-type(3)", "type": "text"},
            {"name": "duration", "selector": ".xdW8 .vmXl-mod-variant-default", "type": "text"},
            {"name": "stops", "selector": ".JWEO .JWEO-stops-text", "type": "text"},
            {"name": "price", "selector": ".zx8F-price-tile .f8F1-price-text", "type": "text"},
            {"name": "fare_type", "selector": ".DOum-option .DOum-name", "type": "text"},
            {"name": "provider", "selector": ".M_JD-provider-name", "type": "text"},
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    async with AsyncWebCrawler(
        verbose=True,
        headless=False,              # Set to False for debugging
        screenshot=True,             # Enable screenshot capture
        magic=True,                  # Enable anti-detection features
        simulate_user=True,
        override_navigator=True,
    ) as crawler:
        # Create a directory to store screenshots and debug files
        debug_dir = "debug_files"
        os.makedirs(debug_dir, exist_ok=True)

        try:
            result = await crawler.arun(
                url=url,
                extraction_strategy=extraction_strategy,
                wait_for="#listWrapper",  # Updated wait selector
                js_code=[
                    # Accept cookies if the consent popup appears
                    "document.querySelector('[id^=onetrust-accept]')?.click();",
                    "document.querySelector('.consent-button')?.click();",
                    # Scroll to the bottom to load more results
                    "window.scrollTo(0, document.body.scrollHeight);",
                ],
                page_timeout=180000,          # Increase timeout to 3 minutes
                delay_before_return_html=5.0, # Wait 5 seconds before capturing content
                bypass_cache=True
            )

            # Save a screenshot for debugging
            screenshot_path = os.path.join(debug_dir, f"flight_search_{origin}_{destination}_{date}.png")
            if result.screenshot:
                with open(screenshot_path, "wb") as f:
                    f.write(result.screenshot)
                print(f"Screenshot saved to {screenshot_path}")
            else:
                print("No screenshot captured.")

            if result.success:
                flights = json.loads(result.extracted_content)
                return flights
            else:
                print(f"Error: {result.error_message}")
                # Save the HTML content for debugging
                html_path = os.path.join(debug_dir, f"error_{origin}_{destination}_{date}.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(result.html)
                print(f"HTML content saved to {html_path} for debugging.")
                return []

        except Exception as e:
            print(f"Exception occurred: {e}")
            return []


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
                f.write(f"- **Departure Time:** {flight.get('departure_time', 'N/A')}\n")
                f.write(f"- **Arrival Time:** {flight.get('arrival_time', 'N/A')}\n")
                f.write(f"- **Duration:** {flight.get('duration', 'N/A')}\n")
                f.write(f"- **Stops:** {flight.get('stops', 'N/A')}\n")
                f.write(f"- **Price:** {flight.get('price', 'N/A')}\n")
                f.write(f"- **Fare Type:** {flight.get('fare_type', 'N/A')}\n")
                f.write(f"- **Provider:** {flight.get('provider', 'N/A')}\n\n")
        print(f"Flight list saved to '{output_file}'.")
    else:
        print("No flights found or an error occurred.")


if __name__ == "__main__":
    main()
