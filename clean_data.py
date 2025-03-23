import pandas as pd
import re
from IPython.display import display

try:
    df = pd.read_csv('ebay_tech_deals.csv', dtype=str)
    print("csv file is loaded with all columns as string successfully")
except Exception as e:
        print("Error occurred:", e)

def clean_numeric(series):
      def convert_value(x):
        x = str(x).strip()
        x = re.sub(r'US\s*\$', '', x)
        x = re.sub(r'[\$,]', '', x)
        try:
            return float(x)
        except ValueError:
            return x
      return series.apply(convert_value)

df['price'] = clean_numeric(df['price'])
df['original_price'] = clean_numeric(df['original_price'])

df['original_price'] = df['original_price'].replace(['N/A', '', None], pd.NA)
df['original_price'] = df['original_price'].fillna(df['price'])

df['shipping'] = df['shipping'].fillna('Shipping info unavailable')

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce')

df['discount_percentage'] = (( 1 - df['price'] / df['original_price'] ) * 100).round(2)

df = df.dropna(subset=['tile', 'price', 'original_price'])

df.to_csv('cleaned_ebay_deals.csv', index=False)