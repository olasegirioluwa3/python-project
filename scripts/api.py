# api.py

from flask import Flask, jsonify, request
from scraper import scrape_google  # Import the scraper function

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # Extract the 'name' query parameter from the URL
    name = request.args.get('name')
    
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    try:
        
        search_url = f"https://www.google.com/search?q={name.replace(' ', '+')}"
        # Pass the name parameter to the scraping function
        scraped_data = scrape_google(search_url)
        return jsonify({"data": scraped_data})
    except Exception as e:
        print (e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
