# PricePulse India 🇮🇳

A full-stack Data Science application that tracks book prices in real-time, converts them to Indian Rupees (₹), and uses Machine Learning to predict future trends.

![Dashboard Preview](static/library_bg.jpg)
*(Note: You can replace this line with a real screenshot of your dashboard later!)*

## 🚀 Features
* **Real-Time Tracking:** Scrapes live data from book retailers using Python & BeautifulSoup.
* **Currency Conversion:** Automatically converts GBP (£) to INR (₹) for Indian users.
* **Price Prediction:** Uses **Linear Regression** to forecast the next 7 days of price trends.
* **Vintage Library UI:** A custom-themed dashboard featuring a "Search Engine" logic that clears data dynamically.
* **Data Persistence:** Uses SQLite to store historical price data and book details.

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js)
* **Database:** SQLite
* **Data Science:** Statistics (Linear Regression), Random Logic (Simulation)

## ⚙️ How to Run
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/PricePulse-India.git](https://github.com/YOUR_USERNAME/PricePulse-India.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    python app.py
    ```
4.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

## 🔮 Future Improvements
* Add email alerts when prices drop.
* Deploy to a cloud platform (Render/AWS).