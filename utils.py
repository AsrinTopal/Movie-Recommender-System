import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch movie poster, details, and cast using TMDB API
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

# Function to fetch movie cast
def fetch_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    cast = data.get('cast', [])
    cast_names = [member['name'] for member in cast[:5]]  # Get top 5 cast members
    return cast_names

# Function to fetch streaming platform information
def fetch_streaming_platforms(movie_id, region="US"):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    response = requests.get(url, params={"api_key": api_key})
    
    if response.status_code != 200:
        return []  # Return empty list if the API call fails
    
    data = response.json()
    if "results" in data and region in data["results"]:
        platforms = data["results"][region].get("flatrate", [])
        platform_names = [p["provider_name"] for p in platforms]
        return platform_names
    return []

# Function to fetch all data concurrently
def fetch_all_movie_data(movie_id):
    poster, description, release_date, rating, genres = fetch_movie_details(movie_id)
    cast = fetch_movie_cast(movie_id)
    platforms = fetch_streaming_platforms(movie_id)
    return poster, description, release_date, rating, genres, cast, platforms

# Function to recommend movies based on the selected movie
def recommend(movie, movies, similarity, platform_filter=None):
    # Get the index of the selected movie
    index = movies[movies['title'] == movie].index[0]
    
    # Compute distances and get the top 10 most similar movies
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:11]
    
    recommended_movies = []

    with ThreadPoolExecutor() as executor:
        futures = {}
        # Submit tasks with their corresponding index
        for i in distances:
            movie_id = movies.iloc[i[0]].movie_id
            futures[executor.submit(fetch_all_movie_data, movie_id)] = i[0]

        for future in as_completed(futures):
            original_index = futures[future]  # Get the index corresponding to the movie
            poster, description, release_date, rating, genres, cast, platforms = future.result()
            
            # Filter platforms if a platform filter is applied
            platforms = [p for p in platforms if platform_filter is None or p.lower() == platform_filter.lower()]
            
            # Append movie details only if platforms match or no filter is applied
            if platforms or platform_filter is None:
                recommended_movies.append({
                    "title": movies.iloc[original_index].title,
                    "rating": rating,
                    "release_date": release_date,
                    "genres": genres,
                    "cast": cast,
                    "poster": poster,
                    "description": description,
                    "platforms": platforms,
                })

    return recommended_movies
