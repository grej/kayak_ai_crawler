# Kayak Flight Search Crawler

This project uses Crawl4AI to search for flight information on Kayak.com.

## Description

This Python script automates the process of searching for flights on Kayak.com. It uses the Crawl4AI library to navigate the website, input search parameters, and extract flight information including airlines, departure times, arrival times, and prices.

## Features

- Asynchronous web crawling using Crawl4AI
- Customizable flight search parameters (origin, destination, date)
- Extracts key flight information (airline, departure time, arrival time, price)
- Handles dynamic content loading on Kayak.com

## Prerequisites

- Python 3.10
- Crawl4AI library
- Playwright (automatically installed with Crawl4AI)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/kayak-flight-search.git
   cd kayak-flight-search
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install "crawl4ai @ git+https://github.com/unclecode/crawl4ai.git"
   ```

## Usage

Run the script with Python:

```
python main.py
```

The script will search for flights based on the parameters set in the `main()` function. Modify these parameters in the script to change the search criteria.

## Configuration

Adjust the following variables in `main.py` to customize your search:

- `origin`: Departure airport code
- `destination`: Arrival airport code
- `date`: Date of travel in YYYY-MM-DD format

## Notes

- This script is for educational purposes only. Please respect Kayak's terms of service and robots.txt file.
- Web scraping may be against the terms of service of some websites. Use responsibly.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- Crawl4AI library: [https://github.com/unclecode/crawl4ai](https://github.com/unclecode/crawl4ai)
- Kayak for flight data (not affiliated)
