import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape product listings
def scrape_product_listings(url, num_pages):
    all_products = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in product_list:
            product_data = {}
            try:
                product_data['Product URL'] = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
                product_data['Product Name'] = product.find('span', {'class': 'a-size-medium'}).text.strip()
                product_data['Product Price'] = product.find('span', {'class': 'a-offscreen'}).text.strip()
                product_data['Rating'] = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
                product_data['Number of Reviews'] = product.find('span', {'class': 'a-size-base'}).text.strip().replace(',', '')
            except:
                continue

            all_products.append(product_data)

    return all_products

# Set the URL and number of pages to scrape
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
num_pages = 20

# Scrape product listings
product_listings = scrape_product_listings(url, num_pages)

# Create a DataFrame from the scraped data
df_product_listings = pd.DataFrame(product_listings)

# Export the DataFrame to a CSV file
df_product_listings.to_csv('product_listings.csv', index=False)

# Scrape additional product details
def scrape_product_details(url_list):
    product_details = []

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_data = {}

        try:
            product_data['Product URL'] = url
            product_data['Description'] = soup.find('div', {'id': 'feature-bullets'}).text.strip()
            product_data['ASIN'] = soup.find('div', {'data-asin': True})['data-asin']
            product_data['Product Description'] = soup.find('div', {'id': 'productDescription'}).text.strip()
            product_data['Manufacturer'] = soup.find('a', {'id': 'bylineInfo'}).text.strip()
        except:
            continue

        product_details.append(product_data)

    return product_details

# Get a list of product URLs from the product listings
product_urls = df_product_listings['Product URL'].tolist()

# Scrape additional product details
product_details = scrape_product_details(product_urls[:200])  # Limiting to 200 URLs

# Create a DataFrame from the scraped data
df_product_details = pd.DataFrame(product_details)

# Export the DataFrame to a CSV file
df_product_details.to_csv('product_details.csv', index=False)
