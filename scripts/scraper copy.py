import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import random

# Create necessary directories if they don't exist
if not os.path.exists('../data'):
    os.makedirs('../data')
if not os.path.exists('../logs'):
    os.makedirs('../logs')

# Setup logging
logging.basicConfig(filename='../logs/scraping.log', level=logging.INFO)

# Function to randomly choose a proxy from proxies.txt file
def get_random_proxy():
    with open('../proxies.txt', 'r') as file:
        proxies = file.readlines()
    return random.choice(proxies).strip()

# URL to scrape
url = 'http://facebook.com'

# Optionally use proxies
proxy = get_random_proxy()
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

try:
    # Make the HTTP request using proxies
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()  # Raise error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    data = [item.text for item in soup.find_all('p')]  # Extract paragraphs
    
    # Save data to CSV file
    df = pd.DataFrame(data, columns=['Content'])
    df.to_csv('../data/scraped_data.csv', index=False)
    
    logging.info(f"Successfully scraped data from {url}")

except Exception as e:
    logging.error(f"Failed to scrape {url}: {e}")
