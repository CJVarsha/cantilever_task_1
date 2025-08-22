import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

products = soup.select("div.thumbnail")

data = []

image_folder = 'static/images'
os.makedirs(image_folder, exist_ok=True)

for idx, product in enumerate(products):
    title = product.select_one("a.title").text.strip()
    price = product.select_one("h4.price").text.strip().replace('$', '')
    description = product.select_one("p.description").text.strip()
    rating = len(product.select("div.ratings span.glyphicon-star"))
    image_url = "https://webscraper.io" + product.select_one("img")['src']

    # Download image and save locally
    img_data = requests.get(image_url).content
    img_filename = f"product_{idx}.jpg"
    img_path = os.path.join(image_folder, img_filename)
    with open(img_path, "wb") as f:
        f.write(img_data)

    data.append({
        "Title": title,
        "Price": price,
        "Description": description,
        "Rating": rating,
        "Image": img_filename  # Just filename, path relative to static folder
    })

df = pd.DataFrame(data)
df.to_excel("webscraper_products.xlsx", index=False)

print("Scraping complete and images saved locally.")
