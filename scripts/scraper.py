# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def scrape_google(name):
    try:
        url = name # url from api.py
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract search results - Typically found in <div class="g">
            search_results = []
            for g in soup.find_all('div', class_='g'):
                title_tag = g.find('h3')
                link_tag = g.find('a')
                content_tag = g.find('span', class_='aCOpRe')  # This class usually contains the snippet/description
                
                if title_tag and link_tag:
                    title = title_tag.text
                    link = link_tag['href']
                    content = content_tag.text if content_tag else "No content available"
                    print(link)
                    search_results.append({
                        'title': title,
                        'link': link,
                        'content': content
                    })

                df = pd.DataFrame(search_results, columns=['Content'])
                df.to_csv('../data/scraped_data.csv', index=False)
                    
                logging.info(f"Successfully scraped data from {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while scraping {url}: {e}")

        if search_results:
            return search_results
        else:
            return f"No search results found for {name}"
    else:
        return f"Failed to retrieve search results with status code {response.status_code}"

# Example usage
if __name__ == "__main__":
    url = "https://google.com"
    proxies = {
        "http": "http://your_proxy:port",
        "https": "http://your_proxy:port",
    }  # Optional: Replace with your actual proxy settings
    
    results = scrape_google(url, proxies=proxies)
    for index, result in enumerate(results, start=1):
        print(f"Result {index}:")
        print(f"  Title: {result['title']}")
        print(f"  Link: {result['link']}")
        print(f"  Content: {result['content']}")
        print()