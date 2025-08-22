import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('products.xlsx')

# Clean price data: remove currency symbol and convert to float
df['Price'] = df['Price'].str.replace('£', '').astype(float)

# Map rating words to numbers
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
df['Rating'] = df['Rating'].map(rating_map)

# Plot price distribution
plt.figure(figsize=(8,6))
sns.histplot(df['Price'], bins=10, kde=True)
plt.title('Product Price Distribution')
plt.xlabel('Price (£)')
plt.ylabel('Number of Products')
plt.show()

# Plot count of ratings
plt.figure(figsize=(8,6))
sns.countplot(x='Rating', data=df)
plt.title('Product Ratings Count')
plt.show()
