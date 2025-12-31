import sqlite3
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime, timedelta

def setup_database():
    conn = sqlite3.connect('pricepulse.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                     (id INTEGER PRIMARY KEY, name TEXT, url TEXT UNIQUE, 
                      image_url TEXT, rating TEXT, description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS prices 
                     (id INTEGER PRIMARY KEY, product_id INTEGER, price REAL, scraped_at DATE DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_book_details(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 1. Price Conversion (GBP -> INR)
    price_text = soup.find('p', class_='price_color').text
    price_gbp = float(price_text.replace('£', ''))
    price_inr = round(price_gbp * 108, 2) # Converting £1 to ₹108
    
    title = soup.find('h1').text
    
    # 2. Image
    relative_img = soup.find('div', class_='item active').find('img')['src']
    image_url = "http://books.toscrape.com/" + relative_img.replace("../", "")
    
    # 3. Rating
    rating_classes = soup.find('p', class_='star-rating')['class']
    rating_map = {'One': '⭐', 'Two': '⭐⭐', 'Three': '⭐⭐⭐', 'Four': '⭐⭐⭐⭐', 'Five': '⭐⭐⭐⭐⭐'}
    rating = rating_map.get(rating_classes[1], '⭐')
    
    # 4. Description
    desc_header = soup.find('div', id='product_description')
    description = "No description available."
    if desc_header:
        description = desc_header.find_next_sibling('p').text[:200] + "..."

    return title, price_inr, image_url, rating, description

def track_product(url):
    details = get_book_details(url)
    title, price, img, rating, desc = details
    
    conn = sqlite3.connect('pricepulse.db')
    cursor = conn.cursor()
    
    cursor.execute("""INSERT OR IGNORE INTO products 
                      (name, url, image_url, rating, description) 
                      VALUES (?, ?, ?, ?, ?)""", (title, url, img, rating, desc))
    
    cursor.execute("SELECT id FROM products WHERE url = ?", (url,))
    product_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO prices (product_id, price) VALUES (?, ?)", (product_id, price))
    
    conn.commit()
    conn.close()

def simulate_history(url):
    details = get_book_details(url)
    title, current_price, img, rating, desc = details
    
    conn = sqlite3.connect('pricepulse.db')
    cursor = conn.cursor()
    
    cursor.execute("""INSERT OR IGNORE INTO products 
                      (name, url, image_url, rating, description) 
                      VALUES (?, ?, ?, ?, ?)""", (title, url, img, rating, desc))
    cursor.execute("SELECT id FROM products WHERE url = ?", (url,))
    product_id = cursor.fetchone()[0]
    
    base_price = current_price
    for i in range(30, 0, -1):
        fake_date = datetime.now() - timedelta(days=i)
        change = random.uniform(-100, 100) # Fluctuate by ₹100
        fake_price = max(100, base_price + change)
        cursor.execute('''INSERT INTO prices (product_id, price, scraped_at) 
                          VALUES (?, ?, ?)''', (product_id, fake_price, fake_date))
    
    conn.commit()
    conn.close()