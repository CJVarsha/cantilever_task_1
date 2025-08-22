from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://fakestoreapi.com/products"

@app.route('/', methods=['GET', 'POST'])
def home():
    # Fetch all products from API
    response = requests.get(API_URL)
    products = response.json()
    
    query = request.form.get('query', '').lower() if request.method == 'POST' else ''
    min_price = request.form.get('min_price', '') if request.method == 'POST' else ''
    max_price = request.form.get('max_price', '') if request.method == 'POST' else ''
    category = request.form.get('category', '') if request.method == 'POST' else ''
    
    filtered = products
    
    # Filter by search keyword in title or description
    if query:
        filtered = [p for p in filtered if query in p['title'].lower() or query in p['description'].lower()]
    
    # Filter by minimum price
    if min_price:
        try:
            min_price_val = float(min_price)
            filtered = [p for p in filtered if p['price'] >= min_price_val]
        except ValueError:
            pass
    
    # Filter by maximum price
    if max_price:
        try:
            max_price_val = float(max_price)
            filtered = [p for p in filtered if p['price'] <= max_price_val]
        except ValueError:
            pass
    
    # Filter by category
    if category and category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    
    # Get unique categories for filter dropdown
    categories = list(set(p['category'] for p in products))
    categories.sort()
    
    return render_template('index.html',
                           products=filtered,
                           query=query,
                           min_price=min_price,
                           max_price=max_price,
                           category=category,
                           categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
