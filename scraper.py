# Hell yeah it worked 

import os
import requests
from bs4 import BeautifulSoup
import time

# Base URL of the Amazon product reviews page
base_url = 'https://www.amazon.in/Philips-AC0920-Purifier-Allergens-Bedrooms/dp/B0DB83LFM3/ref=sr_1_3?crid=3KCTILLP9T2DL&dib=eyJ2IjoiMSJ9.J2hFaN8qk-VQiCg8vA2Fz0PP_wNJpy6OtmZhRLvboVO64MWeeExAgzp_Be1Mhy62x6BZJbP-s2J4R-aEOKbyN0WEDSoQgD9dBFG6ZcaA_vwFwbBQV1dxMDpfvjCEwhoUuiLUkw4wyCh5a_SXOEd5OMY-gCcVdXc-mfNbFf7izgNNoEWh40iVNujS2PEc-qWwJczvFT9LK031sIpQALjHxme_j0J2owxzlj1Cz7dc-JQ.73EHnukWVJnS2-Rpdr0J2Ld_2R-YYwzxqG-dFmNE-2w&dib_tag=se&keywords=airpurifier%2Bfor%2Bhome&qid=1732040581&sprefix=airpuri%2Caps%2C252&sr=8-3&th=1'  # Replace with the actual product's review page

# Create a directory to store the review files
folder_name = 'scraped_reviews'
os.makedirs(folder_name, exist_ok=True)

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

# Function to scrape reviews from a single page
def scrape_reviews(page_url, output_file):
    response = requests.get(page_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('span', {'data-hook': 'review-body'})
        if reviews:
            for idx, review in enumerate(reviews):
                review_text = review.get_text(strip=True)
                output_file.write(f"Review:\n{review_text}\n\n")
            return True  # Indicate that reviews were found
        else:
            return False  # No reviews on this page
    else:
        print(f"Failed to retrieve page {page_url}. Status code: {response.status_code}")
        return False

# Pagination handling
page_number = 1
file_name = 'amazon_all_reviews.txt'
output_file_path = os.path.join(folder_name, file_name)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    while True:
        print(f"Scraping page {page_number}...")
        page_url = f'{base_url}?pageNumber={page_number}'
        has_reviews = scrape_reviews(page_url, output_file)
        if not has_reviews:
            print("No more reviews found.")
            break  # Exit the loop if no reviews found on the page
        page_number += 1
        time.sleep(2)  # Respectful delay to avoid getting blocked

print(f"Saved all reviews to {output_file_path}")
