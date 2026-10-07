import time
import requests
from bs4 import BeautifulSoup
import pandas as pd




# Base URL for books.toscrape.com pagination
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

books_data = []
page = 1
TARGET_ROWS = 1000

print("Starting Web Scraping Process")

while len(books_data) < TARGET_ROWS and page <= 50:
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        break

    html_content = response.text

    # Parse HTML and extract book details using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")

    for book in book_elements:
        title_tag = book.h3.find("a")
        title = title_tag["title"] if "title" in title_tag.attrs else title_tag.text

        price = book.find("p", class_="price_color").get_text(strip=True)

        availability = book.find("p", class_="instock availability").get_text(strip=True)
        
        rating_classes = book.find("p", class_="star-rating")["class"]
        rating = [c for c in rating_classes if c != "star-rating"][0] if len(rating_classes) > 1 else "None"

        books_data.append({
            "ID": len(books_data) + 1,
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability
        })

        # top condition when reaching 1,000 rows
        if len(books_data) >= TARGET_ROWS:
            break

    print(f"Scraped Page {page}/50 — Collected {len(books_data)} total books.")
    page += 1
    time.sleep(0.1)

# Save results to CSV using pandas
df = pd.DataFrame(books_data)
df.to_csv("books_dataset.csv", index=False, encoding="utf-8-sig")

print(f"\nTask Complete! Extracted {len(df)} rows and saved to 'books_dataset.csv'.")
print("\nFirst 5 rows preview:")
print(df.head())