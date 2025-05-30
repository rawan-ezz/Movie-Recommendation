import streamlit as st
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- Load JSON ----------
@st.cache_data
def load_data():
    with open("final_merged_results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['genres'] = df['genres'].apply(lambda x: list(set(x)))  # Remove duplicates
    return df

df = load_data()

# ---------- Precompute TF-IDF Matrix and Vectorizer ----------
@st.cache_data
def compute_tfidf_matrix(df):
    df_copy = df.copy()
    df_copy["description"] = df_copy["description"].fillna("")
    df_copy["genres_str"] = df_copy["genres"].apply(lambda x: " ".join(x))
    df_copy["combined_text"] = df_copy["description"] + " " + df_copy["genres_str"]
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df_copy["combined_text"])
    return tfidf_matrix, tfidf

tfidf_matrix, tfidf_vectorizer = compute_tfidf_matrix(df)

# ---------- Helper Function ----------
def display_poster(url, width=150):
    if not url or not url.startswith("http"):
        url = "https://via.placeholder.com/150x220.png?text=No+Image"
    try:
        st.image(url, width=width)
    except:
        st.image("https://via.placeholder.com/150x220.png?text=Error", width=width)

def recommend_similar_movies(movie_title, df, tfidf_matrix, top_n=5):
    df_copy = df.copy()

    try:
        idx = df_copy[df_copy["title"] == movie_title].index[0]
    except IndexError:
        return pd.DataFrame()  # Movie not found

    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    similar_indices = cosine_sim.argsort()[-(top_n+1):][::-1]
    similar_indices = [i for i in similar_indices if i != idx]

    return df_copy.iloc[similar_indices]

# ---------- Sidebar Filters ----------
st.sidebar.title("🎛️ Filters")

all_genres = sorted({genre for sublist in df['genres'] for genre in sublist})
selected_genres = st.sidebar.multiselect("🎭 Genre", options=all_genres)

countries = sorted(df['country'].dropna().unique())
selected_country = st.sidebar.selectbox("🌍 Country", ["All"] + countries)

search_query = st.sidebar.text_input("🔍 Search by title or description")

min_rating, max_rating = st.sidebar.slider("⭐ Rating Range", 5.0, 10.0, (5.0, 10.0))

min_year, max_year = st.sidebar.slider(
    "📅 Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (int(df["release_year"].min()), int(df["release_year"].max()))
)


sort_by = st.sidebar.selectbox("Sort By", ["Rating", "Vote Count", "Year", "Rank"])
sort_order = st.sidebar.radio("Order", ["Descending", "Ascending"])

# ---------- Filtering ----------
filtered_df = df[
    df["rating"].between(min_rating, max_rating) &
    df["release_year"].between(min_year, max_year)
]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_genres:
    filtered_df = filtered_df[filtered_df["genres"].apply(lambda genres: any(g in genres for g in selected_genres))]

if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False) |
        filtered_df["description"].str.contains(search_query, case=False, na=False)
    ]

ascending = True if sort_order == "Ascending" else False
sort_column = {
    "Rating": "rating",
    "Vote Count": "vote_count",
    "Year": "release_year",
    "Rank": "rank"
}[sort_by]

filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

# ---------- Main Title ----------
st.title("🎬 Movie Recommender App..")
st.markdown("Explore movies based on your favorite genres, country, and ratings!")

# ---------- Display Filtered Movies ----------
if filtered_df.empty:
    st.warning("⚠️ No movies match your filters. Try adjusting them.")
else:
    st.markdown("## 📽️ Results")

    cols = st.columns(4)
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        with cols[i % 4]:
            display_poster(row["poster_url"], width=140)
            st.markdown(f"**{row['title']}**")
            st.markdown(f"⭐ {row['rating']} | {row['release_year']}")
            st.markdown(f"*{', '.join(row['genres'])}*")
            st.markdown(f"🕒 {row['runtime']}")
            st.caption(row["country"])

        if (i + 1) % 4 == 0 and i != len(filtered_df) - 1:
            cols = st.columns(4)

# ---------- Movie Similarity Section ----------
movie_titles = filtered_df["title"].sort_values().tolist()
default_index = 0 if movie_titles else -1

selected_movie = st.selectbox(
    "Choose a movie you like",
    movie_titles,
    index=default_index
)

if selected_movie:
    show_details = st.checkbox("Show movie details")

    st.markdown(f"### Similar to **{selected_movie}**...")

    similar_movies = recommend_similar_movies(selected_movie, df, tfidf_matrix)

    movie_info = df[df["title"] == selected_movie].iloc[0]

    if show_details:
        st.markdown(f"**Description:** {movie_info['description']}")
        st.markdown(f"**Country:** {movie_info['country']}")
        st.markdown(f"**Runtime:** {movie_info['runtime']} minutes")
        st.markdown(f"**Genres:** {', '.join(movie_info['genres'])}")
        st.markdown(f"**Rating:** {movie_info['rating']}")
        st.markdown(f"**Release Year:** {movie_info['release_year']}")

    if not similar_movies.empty:
        st.markdown("## 🎯 Similar Movies")
        cols = st.columns(4)
        for i, (_, row) in enumerate(similar_movies.iterrows()):
            with cols[i % 4]:
                display_poster(row["poster_url"], width=140)
                st.markdown(f"**{row['title']}**")
                st.markdown(f"⭐ {row['rating']} | {row['release_year']}")
                st.markdown(f"*{', '.join(row['genres'])}*")
                st.markdown(f"🕒 {row['runtime']}")
                st.caption(row["country"])
          
            if (i + 1) % 4 == 0 and i != len(similar_movies) - 1:
                cols = st.columns(4)
    else:
        st.warning("No similar movies found.")