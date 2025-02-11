import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from urllib.parse import urljoin
from textblob import TextBlob

# Initialize Streamlit app
st.title("EvolvedCollections: Trading Card Price Tracker & Sentiment Analysis")

# -----------------------------
# 🎴 TCGPlayer Web Scraper
# -----------------------------
st.header("Search for Trading Card Prices")

search_term = st.text_input("Enter the name of a trading card:")

def scrape_tcgplayer(search_term):
    base_url = "https://shop.tcgplayer.com"
    ua = UserAgent()
    
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',
    }
    
    search_url = urljoin(base_url, "/productcatalog/product/show")
    params = {'ProductName': search_term, 'newSearch': 'true', 'sortBy': 'marketPrice'}

    time.sleep(random.uniform(1, 3))  # Random delay to mimic human behavior
    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        cards = []

        product_listings = soup.find_all('li', class_='product-list-item')

        for item in product_listings:
            try:
                card = {
                    'name': item.find('span', class_='product__name').get_text(strip=True),
                    'price': item.find('span', class_='product__market-price--value').get_text(strip=True),
                }
                cards.append(card)
            except AttributeError:
                continue
        
        return cards
    else:
        return None

# Button to trigger search
if st.button("Search for Prices"):
    if search_term:
        results = scrape_tcgplayer(search_term)
        if results:
            for card in results[:3]:  # Show only first 3 results for now
                st.write(f"**{card['name']}** - Price: {card['price']}")
        else:
            st.error("No results found or error occurred.")
    else:
        st.warning("Please enter a card name to search.")

# -----------------------------
# 💬 Sentiment Analysis Feature
# -----------------------------
st.header("Analyze Chatbot Review Sentiment")

user_review = st.text_area("Enter a chatbot review:")

if st.button("Analyze Sentiment"):
    if user_review:
        analysis = TextBlob(user_review)
        sentiment_score = analysis.sentiment.polarity  # -1 (negative) to 1 (positive)

        if sentiment_score > 0.2:
            sentiment = "Positive"
        elif sentiment_score < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        st.write(f"**Sentiment:** {sentiment} (Score: {sentiment_score:.2f})")
    else:
        st.warning("Please enter a review before analyzing.")

# -----------------------------
# 📲 PWA Support (Manifest & Service Worker)
# -----------------------------
st.markdown(
    """
    <script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
        .then(() => console.log("Service Worker Registered"));
    }
    </script>
    """,
    unsafe_allow_html=True
)
