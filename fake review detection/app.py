from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import pickle
import string
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import re
import os

app = Flask(__name__)

# ==============================
# LOAD MODEL
# ==============================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

driver = None   # Global Selenium driver


# ==============================
# CLEAN TEXT
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


# ==============================
# EXTRACT ASIN
# ==============================
def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    return None


# ==============================
# LOGIN ROUTE
# ==============================
@app.route("/login")
def login():
    global driver

    if driver is not None:
        return redirect(url_for("home"))

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # Open Amazon in new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://www.amazon.in")

    return redirect(url_for("home"))


# ==============================
# SCRAPE FUNCTION
# ==============================
def scrape_amazon(product_url):
    global driver

    if driver is None:
        return None, "Browser not initialized. Please login again."

    asin = extract_asin(product_url)
    if not asin:
        return None, "Invalid Amazon URL"

    driver.get(product_url)
    time.sleep(7)

    try:
        product_title = driver.find_element(By.ID, "productTitle").text.strip()
    except:
        product_title = "Amazon_Product"

    all_reviews = []

    for page in range(1, 16):
        print(f"Scraping page {page}...")

        review_url = f"https://www.amazon.in/product-reviews/{asin}?pageNumber={page}"
        driver.get(review_url)
        time.sleep(7)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        reviews = driver.find_elements(By.CSS_SELECTOR, "span[data-hook='review-body']")

        for r in reviews:
            text = r.text.strip()
            if text:
                all_reviews.append(text)

        time.sleep(2)

    return all_reviews, product_title


# ==============================
# HOME
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# ANALYZE
# ==============================
@app.route("/analyze", methods=["POST"])
def analyze():
    global driver

    if driver is None:
        return render_template("index.html", error="Please login to Amazon first.")

    try:
        driver.current_url
    except:
        driver = None
        return render_template("index.html", error="Browser closed. Please login again.")

    product_link = request.form["product_link"]

    reviews, product_title = scrape_amazon(product_link)

    if reviews is None:
        return render_template("index.html", error=product_title)

    if len(reviews) == 0:
        return render_template("index.html", error="No reviews found or CAPTCHA detected.")

    df = pd.DataFrame(reviews, columns=["review"])
    df["clean_review"] = df["review"].apply(clean_text)

    X = vectorizer.transform(df["clean_review"])
    predictions = model.predict(X)

    # Convert predictions safely
    df["prediction"] = pd.Series(predictions).astype(str).str.lower()

    total = len(df)

    # Safe counting (works for fake/genuine or 0/1)
    fake_count = sum(
        p in ["fake", "1"] for p in df["prediction"]
    )

    genuine_count = total - fake_count

    fake_percentage = (fake_count / total) * 100
    genuine_percentage = (genuine_count / total) * 100

    # Safe static folder
    static_path = os.path.join(app.root_path, "static")
    if not os.path.exists(static_path):
        os.makedirs(static_path)

    # BAR CHART
    plt.figure()
    plt.bar(["Fake Reviews", "Genuine Reviews"],
            [fake_count, genuine_count])
    plt.title("Fake vs Genuine Review Count")
    plt.savefig(os.path.join(static_path, "bar_chart.png"))
    plt.close()

    # PIE CHART
    plt.figure()
    plt.pie([fake_percentage, genuine_percentage],
            labels=["Fake Reviews", "Genuine Reviews"],
            autopct="%1.1f%%")
    plt.title("Fake vs Genuine Review Percentage")
    plt.savefig(os.path.join(static_path, "pie_chart.png"))
    plt.close()

    # Close browser after analysis
    driver.quit()
    driver = None

    return render_template("index.html",
                           product=product_title,
                           total=total,
                           fake=fake_count,
                           genuine=genuine_count,
                           show_results=True)


# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=8000, threaded=True)
