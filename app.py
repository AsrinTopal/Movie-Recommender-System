import pickle
import streamlit as st
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import fetch_movie_details, fetch_movie_cast, fetch_streaming_platforms, fetch_all_movie_data, recommend

# Streamlit App (Main Code)
st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎬")

# CSS styling for cards and hover effects
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .main-header {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: white;
        background: linear-gradient(to right, #FF5733, #FFC300);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 20px;
        text-align: center;
        color: #555;
        margin-bottom: 20px;
    }
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
        padding: 15px;
        background-color: white;
    }
    .movie-card:hover {
        transform: scale(1.03);
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.15);
    }
    .movie-poster {
        border-radius: 10px;
    }
    .footer {
        text-align: center;
        font-size: 16px;
        color: #888;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="main-header">🎥 Movie Recommender System 🎥</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover your next favorite movie with personalized recommendations!</div>', unsafe_allow_html=True)


# Splited path
parts_dir = "model/similarity_parts"

# Load Similarity
def load_similarity():
    files = sorted([os.path.join(parts_dir, f) for f in os.listdir(parts_dir) if f.startswith("similarity_part_")])
    similarity_data = b""
    for file in files:
        with open(file, "rb") as f:
            similarity_data += f.read()
    return pickle.loads(similarity_data)

# Load data
similarity = load_similarity()
movies = pickle.load(open('model/movie_list.pkl', 'rb'))

# Sidebar
st.sidebar.title("About")
st.sidebar.info("Are you tired of endlessly scrolling through streaming platforms trying to decide what to watch? This app is designed to help you find your next favorite film based on your preferences. Simply select a movie you already enjoy, and let the app suggest a list of similar movies you might love.")
st.sidebar.markdown("---")
st.sidebar.title("How to Use")
st.sidebar.markdown("1. Select a movie from the dropdown menu.\n2. Click **Show Recommendations** to see personalized movie suggestions.")

# Create two columns: one for the search and sort dropdowns, and one for the selected movie's poster
col1, col2 = st.columns([4, 1])  # Split the layout into two equal columns

# Movie selection, sorting, and platform filter dropdowns in the left column (col1)
with col1:
    # Dropdown for movie selection
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "🔍 Search or Select a Movie:",
        movie_list,
        help="Select a movie to get recommendations."
    )

    # Sorting dropdown
    sort_option = st.selectbox(
        "Sort Recommendations By:",
        ["Rating (Highest to Lowest)", "Release Date (Newest to Oldest)", "Title (Alphabetical)"],
        help="Choose how you'd like to sort the recommendations."
    )
    
    # Platform filter dropdown
    platform_filter = st.selectbox(
        "Filter by Platform:",
        ["All", "Netflix", "Disney Plus", "Amazon Prime", "Hulu", "HBO Max"],
        help="Select a streaming platform to filter recommendations."
    )
    # If "All" is selected, set platform_filter to None
    if platform_filter == "All":
        platform_filter = None

# Fetch the poster for the selected movie
selected_movie_index = movies[movies['title'] == selected_movie].index[0]
selected_movie_id = movies.iloc[selected_movie_index].movie_id
selected_poster, _, _, _, _ = fetch_movie_details(selected_movie_id)

# Display the movie poster in the right column (col2)
with col2:
    st.image(selected_poster, use_container_width=True, caption="Selected Movie Poster")

# Recommendation button
if st.button('Show Recommendations 🎬'):
    # Display "be patient" message if it takes too long
    with st.spinner("Fetching recommendations... Please be patient. This might take a few seconds."):
        recommended_movie_data = recommend(selected_movie, movies, similarity, platform_filter)
    
    st.markdown("### ✨ Top 10 Recommendations for You:")
    st.markdown("---")
    
    # Sorting logic based on selected option
    if sort_option == "Rating (Highest to Lowest)":
        recommended_movie_data = sorted(recommended_movie_data, key=lambda x: x['rating'], reverse=True)
    elif sort_option == "Release Date (Newest to Oldest)":
        recommended_movie_data = sorted(recommended_movie_data, key=lambda x: x['release_date'], reverse=True)
    elif sort_option == "Title (Alphabetical)":
        recommended_movie_data = sorted(recommended_movie_data, key=lambda x: x['title'].lower())

    # Display recommendations with card layout
    for movie in recommended_movie_data:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(movie["poster"], use_container_width=True, caption=movie["title"])
            with col2:
                st.markdown(f"**🎬 {movie['title']}**")
                st.markdown(f"**⭐ Rating:** {movie['rating']} | **📅 Release Date:** {movie['release_date']}")
                st.markdown(f"**🎭 Genres:** {', '.join(movie['genres'])}")
                
                # Display platform names beside the movie poster
                platforms = ", ".join(movie["platforms"])
                if platforms == "None":
                    platforms = "None"
                st.markdown(f"**📡 Available On:** {platforms}")
                
                # Display cast names
                st.markdown(f"**🎬 Cast:** {', '.join(movie['cast'])}")
                
                st.markdown(f"*{movie['description']}*")
            
                st.markdown("---")

# Footer
st.markdown(
    """
    --- 
    <div class="footer">
        Created By ASRIN TOPAL
    </div>
    """,
    unsafe_allow_html=True,
)
