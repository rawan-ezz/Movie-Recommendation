# 🎬 IMDb Top 250 Movie Recommendation System

This project was developed by four university students — *Rawan Ezzaldeen, Fatima Sabra, Sally Fniesh, and Nour Falha* — as part of a *Data Scraping course project*. It combines web scraping with an interactive Streamlit app to build a content-based movie recommendation system.

---

## 📌 Project Overview

The main goals of this project are:
- Scrape metadata for the top 250 movies from IMDb.
- Store and process the data into a structured format (JSON & Pandas DataFrame).
- Build a recommendation engine using TF-IDF and cosine similarity.
- Provide an interactive user interface for filtering and discovering movies.

---

## 🧱 Components

### 1. 🕸 Web Scraping
Using *Scrapy*, we scraped:
- 🎞 Title
- 📅 Release Year
- ⭐ IMDb Rating
- 🎭 Genres
- 🧾 Description
- 🌍 Country of Origin
- 🕒 Runtime
- 📊 Vote Count
- 🖼 Poster Image URL

### 2. 📊 Recommendation Engine
- We used *TF-IDF (Term Frequency–Inverse Document Frequency)* on the movie *description + genres*.
- *Cosine similarity* is calculated to recommend similar movies.
- Users can get personalized recommendations based on these movies too.

### 3. 💡 Streamlit App
- 🎛 Sidebar filters: genre, country, rating, release year, keyword search.
- 📥 Dynamic movie list display (with posters and metadata).
- 🎯 Click on any movie to get similar recommendations.
- ⚡ Efficient performance via caching and precomputed TF-IDF.

