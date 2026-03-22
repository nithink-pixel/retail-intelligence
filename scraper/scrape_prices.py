import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

def scrape_books(max_pages=5):
    """
    Scrapes book prices from books.toscrape.com
    Returns a pandas DataFrame with all scraped data
    """
    all_books = []
    url = START_URL
    page_num = 1

    while url and page_num <= max_pages:
        print(f"Scraping page {page_num}...")

        # Step 1: Download the webpage
        response = requests.get(url)

        # Step 2: Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 3: Find all book cards on the page
        books = soup.find_all("article", class_="product_pod")

        # Step 4: Extract data from each book card
        for book in books:
            title = book.find("h3").find("a")["title"]
            price_text = book.find("p", class_="price_color").text
            price = float(price_text.replace("£", "").replace("Â", "").strip())
            rating_word = book.find("p", class_="star-rating")["class"][1]
            availability = book.find("p", class_="instock").text.strip()

            all_books.append({
                "title": title,
                "price_gbp": price,
                "rating": rating_word,
                "availability": availability,
                "scraped_at": datetime.now().isoformat(),
                "page": page_num
            })

        # Step 5: Find the "next" button to go to next page
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_page = next_btn.find("a")["href"]
            url = BASE_URL + next_page
            page_num += 1
        else:
            url = None

    df = pd.DataFrame(all_books)
    print(f"\nDone! Scraped {len(df)} books across {page_num-1} pages.")
    return df


if __name__ == "__main__":
    df = scrape_books(max_pages=5)
    print(df.head(10))
    print(f"\nPrice range: £{df['price_gbp'].min()} - £{df['price_gbp'].max()}")
    print(f"Average price: £{df['price_gbp'].mean():.2f}")