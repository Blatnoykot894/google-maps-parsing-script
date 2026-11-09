# Async Google Maps Hotel Scraper

A simple asynchronous web scraper that extracts hotel names and links from Google Maps using Playwright and Pandas. It uses Python's asyncio to run multiple search queries simultaneously to speed up the process.

## Features

- Concurrent scraping of multiple search URLs.
- Automated infinite scroll handling.
- Duplicates removal based on the link field.
- Results export to an Excel file (.xlsx).

## Requirements

- Python 3.10+
- Playwright
- Pandas
- Openpyxl (required by Pandas for Excel export)

## Installation

Install the required libraries:
```bash
pip install playwright pandas openpyxl
```

Install the browser binaries for Playwright:
```bash
playwright install chromium
```

## Usage

1. Open the script and add your target Google Maps search URLs to the tasks list inside the main function.
2. Run the script:
```bash
python main.py
```

The filtered results will be saved as hotels.xlsx in the project directory.
