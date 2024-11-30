import pickle
import streamlit as st
import requests

# Function to fetch movie poster and details using TMDB API
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    overview = data.get('overview', 'Description not available.')
    release_date = data.get('release_date', 'N/A')
    rating = data.get('vote_average', 'N/A')
    genres = [genre['name'] for genre in data.get('genres', [])]
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Image"
    return full_path, overview, release_date, rating, genres

def fetch_streaming_platforms(movie_id, region="US"):
    """
    Fetch the streaming platform information for a movie based on its TMDB ID.
    Returns a list of platform names the movie is available on.
    """
    api_key = "8265bd1679663a7ea12ac168da84d2e8"  # Replace with your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    response = requests.get(url, params={"api_key": api_key})
    
    if response.status_code != 200:
        return []  # Return empty list if the API call fails
    
    data = response.json()
    if "results" in data and region in data["results"]:
        platforms = data["results"][region].get("flatrate", [])
        platform_names = [p["provider_name"] for p in platforms]  # Get the platform names
        return platform_names
    return []  # Return empty list if no platforms are found

# Recommendation function
def recommend(movie, platform_filter=None):
    """
    Generate movie recommendations and filter by selected platform.
    """
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_data = []
    
    for i in distances[1:11]:  # Top 10 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        poster, description, release_date, rating, genres = fetch_movie_details(movie_id)
        streaming_platforms = fetch_streaming_platforms(movies.iloc[i[0]].movie_id)
        
        # Filter by platform if a platform filter is set
        if platform_filter:
            # Compare lowercase platform names to avoid case sensitivity issues
            if platform_filter.lower() not in [p.lower() for p in streaming_platforms]:
                continue  # Skip this movie if it's not available on the selected platform
        
        recommended_movie_data.append({
            "title": movies.iloc[i[0]].title,
            "poster": poster,
            "description": description,
            "release_date": release_date,
            "rating": rating,
            "genres": genres,
            "platforms": streaming_platforms if streaming_platforms else ["None"]
        })
    
    return recommended_movie_data

# Streamlit App
st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎬")

# CSS styling for cards and hover effects
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

# Sidebar
st.sidebar.title("About")
st.sidebar.info("Are you tired of endlessly scrolling through streaming platforms trying to decide what to watch? This app is designed to help you find your next favorite film based on your preferences. Simply select a movie you already enjoy, and let the app suggest a list of similar movies you might love.")
st.sidebar.markdown("---")
st.sidebar.title("How to Use")
st.sidebar.markdown("1. Select a movie from the dropdown menu.\n2. Click **Show Recommendations** to see personalized movie suggestions.")

# Load data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

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
    st.markdown("### ✨ Top 10 Recommendations for You:")
    st.markdown("---")
    recommended_movie_data = recommend(selected_movie, platform_filter)

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
