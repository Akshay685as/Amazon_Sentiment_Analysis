import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import os
from wordcloud import WordCloud

df = pd.read_csv("C:/Users/Akshay Soni/Python Data Analysis/Amazon_Sentimmental_analysis/Reviews.csv")
#df = df.sample(5000, random_state=42).copy()

df['ReadableTime'] = pd.to_datetime(df['Time'], unit='s')

# Drop missing or blank reviews
df = df.dropna(subset=['Text'])
df = df[df['Text'].str.strip() != ""]

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Apply sentiment scoring (vectorized with list comprehension for speed)
tqdm.pandas()
df['SentimentScore'] = df['Text'].progress_apply(lambda x: analyzer.polarity_scores(str(x))['compound'])

# Label sentiment
def label_sentiment(score):
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

df['SentimentLabel'] = df['SentimentScore'].apply(label_sentiment)
# Calculate average sentiment per product
product_sentiment = df.groupby('ProductId')['SentimentScore'].mean().reset_index()

# Top 10 most loved products
top_positive_products = product_sentiment.sort_values(by='SentimentScore', ascending=False).head(10)

# Top 10 most hated products
top_negative_products = product_sentiment.sort_values(by='SentimentScore', ascending=True).head(10)

# Save to CSV
os.makedirs("outputs", exist_ok=True)
top_positive_products.to_csv("outputs/top_positive_products.csv", index=False)
top_negative_products.to_csv("outputs/top_negative_products.csv", index=False)

# Save results
df[['ProductId', 'ProfileName', 'Score', 'SentimentScore', 'SentimentLabel']].to_csv("outputs/sentiment_summary_full.csv", index=False)

# Plot sentiment distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='SentimentLabel', palette='Set2')
plt.title("Sentiment Distribution of Amazon Product Reviews")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()

# Create charts folder before saving
os.makedirs("charts", exist_ok=True)
plt.savefig("charts/sentiment_distribution_full.png")
plt.show()


# Filter text for wordclouds
positive_text = ' '.join(df[df['SentimentLabel'] == 'Positive']['Text'].dropna().astype(str))
negative_text = ' '.join(df[df['SentimentLabel'] == 'Negative']['Text'].dropna().astype(str))

# Generate Positive WordCloud
wordcloud_pos = WordCloud(width=800, height=400, background_color='white').generate(positive_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_pos, interpolation='bilinear')
plt.axis('off')
plt.title("WordCloud – Positive Reviews")
plt.tight_layout()

os.makedirs("charts", exist_ok=True)
plt.savefig("charts/wordcloud_positive.png")
plt.show()

# Generate Negative WordCloud
wordcloud_neg = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(negative_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_neg, interpolation='bilinear')
plt.axis('off')
plt.title("WordCloud – Negative Reviews")
plt.tight_layout()
plt.savefig("charts/wordcloud_negative.png")
plt.show()

