# banggood_analysis_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Banggood Data Analysis", layout="wide")

st.title("Banggood Product Analysis Dashboard")

# -----------------------------
# 1. Load CSV
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("banggood_all_categories.csv")
    # Clean price column
    df['price'] = df['price'].str.replace('£','').str.strip()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Clean rating column
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    
    # Clean reviews column
    df['reviews'] = df['reviews'].str.replace('reviews','').str.replace('review','').str.strip()
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    
    # Drop rows with missing price or title
    df = df.dropna(subset=['price','title'])
    
    # Best value = rating / price
    df['best_value'] = df['rating'] / df['price']
    
    return df

df = load_data()

# -----------------------------
# 2. Sidebar filters
# -----------------------------
categories = df['main_category'].unique().tolist()
selected_category = st.sidebar.selectbox("Select Category", ["All"] + categories)

if selected_category != "All":
    df_filtered = df[df['main_category'] == selected_category]
else:
    df_filtered = df.copy()

# -----------------------------
# 3. Average Rating per Category
# -----------------------------
st.subheader("Average Rating per Category")
avg_rating = df.groupby('main_category')['rating'].mean()
fig1, ax1 = plt.subplots(figsize=(8,4))
avg_rating.plot(kind='bar', color='lightgreen', ax=ax1)
ax1.set_ylabel("Average Rating")
ax1.set_title("Average Rating per Category")
st.pyplot(fig1)

# -----------------------------
# 4. Top 10 Most Reviewed Products
# -----------------------------
st.subheader("Top 10 Most Reviewed Products")
top_reviews = df_filtered.sort_values(by='reviews', ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.barh(top_reviews['title'], top_reviews['reviews'], color='orange')
ax2.set_xlabel("Number of Reviews")
ax2.set_title("Top 10 Most Reviewed Products")
ax2.invert_yaxis()  # Highest on top
st.pyplot(fig2)

# -----------------------------
# 5. Best Value per Category
# -----------------------------
st.subheader("Best Value per Category (Rating / Price)")
best_value_cat = df.groupby('main_category')['best_value'].mean()
fig3, ax3 = plt.subplots(figsize=(8,4))
best_value_cat.plot(kind='bar', color='purple', ax=ax3)
ax3.set_ylabel("Average Rating / Price")
ax3.set_title("Best Value per Category")
st.pyplot(fig3)

# -----------------------------
# 6. Number of Products per Category
# -----------------------------
st.subheader("Number of Products per Category")
product_count = df['main_category'].value_counts()
fig4, ax4 = plt.subplots(figsize=(8,4))
product_count.plot(kind='bar', color='red', ax=ax4)
ax4.set_ylabel("Number of Products")
ax4.set_title("Number of Products per Category")
st.pyplot(fig4)

# -----------------------------
# 7. Show raw data (optional)
# -----------------------------
with st.expander("Show Raw Data"):
    st.dataframe(df_filtered)
