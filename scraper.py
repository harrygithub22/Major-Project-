import os
import requests
from bs4 import BeautifulSoup
import time

# Base URL of the Amazon product reviews page
base_url = 'https://www.amazon.in/Apple-AirPods-Pro-2nd-Generation/dp/B0BDKD8DVD/ref=sr_1_2_sspa?crid=17C0EKGOBWQHF&dib=eyJ2IjoiMSJ9.JGnSoNaXuJ16jDUnbFr4r0bP-v85sRK319RUmTU9LreaAMGD6qxckBVHucKrdgXYoISqUj8OSnKW5s-16RS92xrYnoUixbhgfY2bWmDHPMWjwEWypd2TDoJKR6vEGNGQBcrD0EAZXRI7df9M8JWmr8JdqxqScWZQSL_236oWDBVe7Upq_x_amB8f2HwnmMjNhU9jFM1_mhPNFMxClZG8j-KKORy5nKDGA7f2DgTiWls.bzFwtk-k5fWBO1pNf1slK9CcPXqb5PW6-Kh6_HFa2y4&dib_tag=se&keywords=airpods&qid=1732221189&sprefix=airpod%2Caps%2C279&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'  # Replace with the actual product's review page

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






# Not working properly but needed 

# import os
# import requests
# from bs4 import BeautifulSoup
# import time

# # Base URL of the Amazon product reviews page
# base_url = 'https://www.amazon.in/Safari-Polyester-Softsided-Suitcase-spartan-75-red-2WH/dp/B00R45W232/ref=zg_m_bs_c_luggage_m_sccl_1/262-8463858-2325600?pd_rd_w=F3Y1z&content-id=amzn1.sym.cde02f8b-0594-439d-9e93-f4cced7ce3ce&pf_rd_p=cde02f8b-0594-439d-9e93-f4cced7ce3ce&pf_rd_r=C649N002WWAJBYW1EBFZ&pd_rd_wg=qTXn7&pd_rd_r=4ad99992-2280-4194-a3a1-ac17cafc9d3e&pd_rd_i=B00R45W232&th=1'  # Replace with the actual product's review page

# # Create a directory to store the review files
# folder_name = 'scraped_reviews'
# os.makedirs(folder_name, exist_ok=True)

# # Headers to mimic a browser visit
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
# }

# # Function to scrape reviews from a single page
# def scrape_reviews(page_url, output_file):
#     response = requests.get(page_url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         reviews = soup.find_all('span', {'data-hook': 'review-body'})
#         if reviews:
#             for idx, review in enumerate(reviews):
#                 review_text = review.get_text(strip=True)
#                 output_file.write(f"Review:\n{review_text}\n\n")
#             return True  # Indicate that reviews were found
#         else:
#             return False  # No reviews on this page
#     else:
#         print(f"Failed to retrieve page {page_url}. Status code: {response.status_code}")
#         return False

# # Pagination handling
# page_number = 1
# file_name = 'amazon_all_reviews_Classic_Mosquito_Net.txt'
# output_file_path = os.path.join(folder_name, file_name)

# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     while True:
#         print(f"Scraping page {page_number}...")
#         page_url = f'{base_url}?pageNumber={page_number}'
#         has_reviews = scrape_reviews(page_url, output_file)
#         if not has_reviews:
#             print("No more reviews found.")
#             break  # Exit the loop if no reviews found on the page
#         page_number += 1
#         time.sleep(2)  # Respectful delay to avoid getting blocked

# print(f"Saved all reviews to {output_file_path}")

