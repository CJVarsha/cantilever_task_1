from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_excel('products.xlsx')

# Clean price and map rating for filtering
df['Price'] = df['Price'].str.replace('£', '').astype(float)
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['RatingNum'] = df['Rating'].map(rating_map)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = df
    query = ''
    min_price = ''
    max_price = ''
    min_rating = ''
    
    if request.method == 'POST':
        query = request.form.get('query', '').lower()
        min_price = request.form.get('min_price', '')
        max_price = request.form.get('max_price', '')
        min_rating = request.form.get('min_rating', '')
        
        results = df
        
        if query:
            results = results[results['Title'].str.lower().str.contains(query)]
        
        if min_price:
            try:
                min_price_val = float(min_price)
                results = results[results['Price'] >= min_price_val]
            except ValueError:
                pass
        
        if max_price:
            try:
                max_price_val = float(max_price)
                results = results[results['Price'] <= max_price_val]
            except ValueError:
                pass
        
        if min_rating:
            try:
                min_rating_val = int(min_rating)
                results = results[results['RatingNum'] >= min_rating_val]
            except ValueError:
                pass
    
    return render_template('index.html', products=results.to_dict(orient='records'),
                           query=query, min_price=min_price, max_price=max_price, min_rating=min_rating)

if __name__ == '__main__':
    app.run(debug=True)
