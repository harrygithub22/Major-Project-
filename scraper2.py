from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Path to your ChromeDriver
CHROME_DRIVER_PATH = 'path_to_chromedriver'  # Replace with the actual path to your chromedriver executable

# Base URL for the product reviews
product_url = 'https://www.amazon.in/Qualiroast-Barbeque-Breifcase-Portable-Accessories/product-reviews/B0B9T8J82W/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'

# Create a directory to store the review files
folder_name = 'scraped_reviews'
os.makedirs(folder_name, exist_ok=True)

# File setup
file_name = 'selenium_amazon_reviews.txt'
output_file_path = os.path.join(folder_name, file_name)

# Initialize Selenium WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get(product_url)

# Scrape reviews
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    while True:
        try:
            # Wait for reviews to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-hook="review-body"]'))
            )
            
            # Extract review texts
            reviews = driver.find_elements(By.CSS_SELECTOR, 'span[data-hook="review-body"]')
            for review in reviews:
                review_text = review.text.strip()
                output_file.write(f"Review:\n{review_text}\n\n")
            
            print("Scraped reviews from current page.")

            # Locate and click the "Next" button
            next_button = driver.find_element(By.CLASS_NAME, 'a-last')
            if 'a-disabled' in next_button.get_attribute('class'):
                print("No more pages.")
                break  # Exit the loop if "Next" button is disabled
            next_button.click()
            time.sleep(3)  # Respectful delay
        except Exception as e:
            print(f"Error: {e}")
            break

# Close the browser
driver.quit()

print(f"Saved all reviews to {output_file_path}")
