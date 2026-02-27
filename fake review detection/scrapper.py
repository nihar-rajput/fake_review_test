from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re

def clean_filename(name):
    # Remove invalid filename characters
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name[:50]  # limit length

def scrape_amazon(asin, pages=5):

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.amazon.in")
    print("Login to Amazon manually.")
    input("Press ENTER after login...")

    # 🔥 Open product page first to get product name
    product_url = f"https://www.amazon.in/dp/{asin}"
    driver.get(product_url)
    time.sleep(5)

    try:
        product_title = driver.find_element(By.ID, "productTitle").text.strip()
    except:
        product_title = "Amazon_Product"

    print("Product Name:", product_title)

    clean_name = clean_filename(product_title)

    all_reviews = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        review_url = f"https://www.amazon.in/product-reviews/{asin}?pageNumber={page}"
        driver.get(review_url)
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        reviews = driver.find_elements(By.CSS_SELECTOR, "span[data-hook='review-body']")

        for r in reviews:
            text = r.text.strip()
            if text:
                all_reviews.append(text)

    driver.quit()

    df = pd.DataFrame(all_reviews, columns=["review"])

    filename = f"{clean_name}_reviews.csv"
    df.to_csv(filename, index=False)

    print("Saved as:", filename)
    print("Total reviews:", len(all_reviews))


if __name__ == "__main__":
    asin = input("Enter ASIN: ")
    scrape_amazon(asin)