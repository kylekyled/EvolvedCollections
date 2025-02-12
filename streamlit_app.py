def scrape_tcgplayer(search_term):
    base_url = "https://www.tcgplayer.com/search/magic/product"
    ua = UserAgent()
    
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',
    }

    # Format search URL correctly
    search_url = f"{base_url}?q={search_term.replace(' ', '+')}"

    response = requests.get(search_url, headers=headers)

    # ✅ Debugging: Print first 1000 characters of HTML response
    print(response.text[:1000])  

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = []

        product_listings = soup.find_all('div', class_='search-result__content')

        for item in product_listings:
            try:
                card = {
                    'name': item.find('span', class_='search-result__title').get_text(strip=True),
                    'price': item.find('span', class_='search-result__market-price').get_text(strip=True),
                }
                cards.append(card)
            except AttributeError:
                continue
        
        return cards
    else:
        return None
