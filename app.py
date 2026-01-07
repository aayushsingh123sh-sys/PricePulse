from flask import Flask, jsonify, render_template, request
import sqlite3
from engine import track_product, simulate_history, setup_database
import statistics
import os

app = Flask(__name__)

if not os.path.exists('pricepulse.db'):
    setup_database()

def get_db_connection():
    conn = sqlite3.connect('pricepulse.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        track_product(request.json.get('url')) 
        return jsonify({"message": "Tracked!"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/simulate-history', methods=['POST'])
def simulate():
    try:
        simulate_history(request.json.get('url'))
        return jsonify({"message": "Done!"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    if os.path.exists('pricepulse.db'):
        os.remove('pricepulse.db') 
        setup_database()
    return jsonify({"message": "Cleared"})

@app.route('/api/products')
def get_products():
    conn = get_db_connection()
    
    last_book = conn.execute("SELECT id FROM products ORDER BY id DESC LIMIT 1").fetchone()
    
    history_rows = conn.execute("SELECT DISTINCT name FROM products").fetchall()
    search_history = [row['name'] for row in history_rows]
    
    if not last_book:
        conn.close()
        return jsonify({"history": [], "search_history": search_history})

    last_id = last_book['id']

    query = '''
        SELECT products.name, products.image_url, products.rating, products.description,
               prices.price, prices.scraped_at 
        FROM prices 
        JOIN products ON prices.product_id = products.id
        WHERE prices.product_id = ? 
        ORDER BY prices.scraped_at ASC
    '''
    rows = conn.execute(query, (last_id,)).fetchall()
    conn.close()

    results = [dict(row) for row in rows]
    
    for r in results:
        r['price'] = round(r['price'], 2)

    latest = results[-1]
    book_details = {
        "name": latest['name'],
        "image": latest['image_url'],
        "rating": latest['rating'],
        "desc": latest['description']
    }

    prices = [r['price'] for r in results]
    
    stats = {
        "max": round(max(prices), 2),
        "min": round(min(prices), 2),
        "avg": round(statistics.mean(prices), 2)
    }
    
    prediction_prices = []
    if len(results) > 5:
        x_values = list(range(len(results))) 
        y_values = prices
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        slope = numerator / denominator
        intercept = y_mean - (slope * x_mean)
        last_day_index = x_values[-1]
        for i in range(1, 8):
            pred = (slope * (last_day_index + i)) + intercept
            prediction_prices.append(round(pred, 2))

    return jsonify({
        "history": results, 
        "prediction": prediction_prices,
        "stats": stats,
        "book_details": book_details,
        "search_history": search_history 
    })

if __name__ == '__main__':
    app.run(debug=True)
