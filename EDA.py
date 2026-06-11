# customer_etl.py

import pandas as pd
from sqlalchemy import create_engine

# Load Data
df = pd.read_csv(
    r"customer_shopping_behavior.csv"
)

# ------------------------
# Data Understanding
# ------------------------

print(df.head())
print(df.info())
print(df.describe())

# ------------------------
# Missing Values
# ------------------------

df['Review Rating'] = (
    df.groupby('Category')['Review Rating']
      .transform(lambda x: x.fillna(x.median()))
)

# ------------------------
# Standardize Columns
# ------------------------

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')

df = df.rename(
    columns={
        'purchase_amount_(usd)':
        'purchase_amount'
    }
)

# ------------------------
# Age Groups
# ------------------------

labels = [
    'Young Adult',
    'Adult',
    'Middle Aged',
    'Seniors'
]

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)

# ------------------------
# Purchase Frequency
# ------------------------

frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}

df['purchase_frequency_days'] = (
    df['frequency_of_purchases']
      .map(frequency_mapping)
)

# ------------------------
# Remove Duplicate Column
# ------------------------

if (
    df['discount_applied']
    ==
    df['promo_code_used']
).all():

    df.drop(
        'promo_code_used',
        axis=1,
        inplace=True
    )

# ------------------------
# PostgreSQL Connection
# ------------------------

username = "postgres"
password = "admin"
host = "localhost"
port = "5432"
database = "Customer_Behaviour"

engine = create_engine(
    f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
)

# Load Data

df.to_sql(
    "customer",
    engine,
    if_exists="replace",
    index=False
)

print("Data Loaded Successfully!")