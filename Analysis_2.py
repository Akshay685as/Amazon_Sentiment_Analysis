import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Page settings
st.set_page_config(page_title="Amazon Review Sentiment Dashboard", layout="wide")

# Load sentiment summary
df = pd.read_csv("outputs/sentiment_summary_full.csv")

# Sidebar: Sentiment filter
st.sidebar.title("🔍 Filter Options")
selected_sentiment = st.sidebar.radio("Select Sentiment", ["All", "Positive", "Neutral", "Negative"])

# Filter data
if selected_sentiment != "All":
    filtered_df = df[df['SentimentLabel'] == selected_sentiment]
else:
    filtered_df = df

st.title("📊 Amazon Product Review Sentiment Dashboard")
st.write(f"Total Reviews Displayed: {len(filtered_df):,}")

# Sentiment Distribution Chart
st.subheader("Sentiment Distribution")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='SentimentLabel', palette='Set2', ax=ax)
st.pyplot(fig)

# WordCloud Display (Pre-generated)
st.subheader("WordCloud: Positive & Negative Feedback")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Positive Reviews WordCloud**")
    image1 = Image.open("charts/wordcloud_positive.png")
    st.image(image1, use_column_width=True)

with col2:
    st.markdown("**Negative Reviews WordCloud**")
    image2 = Image.open("charts/wordcloud_negative.png")
    st.image(image2, use_column_width=True)

# Top 5 Most Positive & Negative Products
st.subheader("🏆 Top Products by Sentiment")
col3, col4 = st.columns(2)

with col3:
    top_pos = pd.read_csv("outputs/top_positive_products.csv")
    st.markdown("**Most Loved Products**")
    st.dataframe(top_pos.head())

with col4:
    top_neg = pd.read_csv("outputs/top_negative_products.csv")
    st.markdown("**Most Hated Products**")
    st.dataframe(top_neg.head())

# Sample reviews
st.subheader("📝 Sample Reviews")
st.dataframe(filtered_df[['ProfileName', 'Score', 'SentimentScore', 'SentimentLabel']].sample(10))
