import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('article', class_='product_pod')

data = []

for product in products:
    title = product.h3.a['title']
    price = product.find('p', class_='price_color').text
    rating = product.p['class'][1]  # rating in class name
    product_url = "http://books.toscrape.com/catalogue/" + product.h3.a['href']

    product_page = requests.get(product_url)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    description_tag = product_soup.find('meta', attrs={'name':'description'})
    description = description_tag['content'].strip() if description_tag else "No description"

    data.append({
        'Title': title,
        'Price': price,
        'Rating': rating,
        'Description': description
    })

df = pd.DataFrame(data)
df.to_excel('products.xlsx', index=False)

print("Scraping complete. Data saved to products.xlsx")
