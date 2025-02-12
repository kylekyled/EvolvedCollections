import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def scrape_tcgplayer(search_term):
    # Configure retry strategy
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Updated headers with browser-like behavior
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.tcgplayer.com/',
        'Connection': 'keep-alive'
    }

    # Encoded search URL
    search_url = f"https://www.tcgplayer.com/search/magic/product?q={requests.utils.quote(search_term)}&view=grid"

    try:
        response = session.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Debugging: Save HTML to file
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = []

        # Updated selector for 2023 layout
        product_listings = soup.select('div.search-result[data-testid="search-result"]')

        for item in product_listings:
            try:
                name = item.select_one('h2.search-result__title > a').get_text(strip=True)
                price_section = item.select_one('div.search-result__market-price')
                
                # Handle multiple price scenarios
                if price_section:
                    price = price_section.select_one('span:not(.label)').get_text(strip=True)
                else:
                    price = "N/A"

                cards.append({
                    'name': name,
                    'price': price.replace('Market Price\n', '').strip()
                })
            except (AttributeError, TypeError) as e:
                print(f"Error parsing item: {e}")
                continue

        return cards

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage example
if __name__ == "__main__":
    results = scrape_tcgplayer("Black Lotus")
    if results:
        print(f"Found {len(results)} cards:")
        for card in results:
            print(f"{card['name']}: {card['price']}")
