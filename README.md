# Movie Recommender System 🎥
This project is a movie recommendation system that suggests movies based on user preferences. It consists of two main components:

# MOVIE RECOMMENDER SYSTEM GIVE IT A TRY
## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [App Screenshot](#app-screenshot)
- [License](#license)

## Overview
The Movie Recommender System is a user-friendly application designed to help movie enthusiasts discover new films tailored to their tastes. The system analyzes metadata such as genres, cast, crew, and keywords to provide personalized movie recommendations.

The app uses a content-based filtering approach, ensuring high-quality suggestions based on the user's selected movie. The train.py script processes the movie metadata and generates the necessary files (movie_list.pkl and similarity.pkl), which are then used by the app for recommendations. Users must run the training script first to prepare the data before using the application.

The accompanying Streamlit web interface offers an intuitive experience, allowing users to explore recommendations, view movie posters, and sort results by rating, release date, or title. With seamless integration of the TMDB API, the app fetches detailed movie information, including posters, ratings, and descriptions, enhancing the user experience.

Whether you're looking for your next favorite movie or exploring new genres, the Movie Recommender System is here to help!


## Key Features
* Suggests movies based on metadata like genres, keywords, cast, and crew.
* Sort recommendations by rating, release date, or title.
* Displays movie details, including posters, ratings, genres, and overviews, using the TMDB API.

## Project Structure
* **train.py:** Prepares and trains the model. You do not need to run this as the pre-trained files are already provided.
* **app.py:** The main Streamlit app for user interaction.

#### Data Files (Optional for re-training):
* **tmdb_5000_movies.csv:** Dataset containing movie metadata.
* **tmdb_5000_credits.csv:** Dataset containing movie credits information.

## How It Works
#### Movie Selection:
* Choose a movie from the dropdown menu.
* The app fetches metadata and poster using the TMDB API.
#### Recommendations:
* Displays the top 10 recommendations based on the trained model.
*Includes sorting options: rating, release date, or title.
#### Visual Layout:
* Recommendations are shown in a card-style layout with posters, ratings, genres, and descriptions.\

## Installation
### Prerequisites
* Pandas: For data manipulation and analysis.
* NumPy: For numerical operations.
* Scikit-learn: For machine learning and vectorization.
* Streamlit: For building and running the web app.
* Requests: For fetching data from the TMDB API.
* Ast: For safely parsing strings into Python objects.

### Step 1: Clone the Repository

```
git clone https://github.com/AsrinTopal/movie-recommender-system.git
cd movie-recommender-system
```

### Step 2: Install Dependencies
```
pip install -r requirements.txt
```

### Step 3: Train the data
```
python train.py
```

### Step 4: Run the Streamlit App
```
steamlit run app.py
```
The app will launch in your browser. If it doesn't open automatically, navigate to http://localhost:8501 in your browser.

## App Screenshot

## Example Output
### Web App
* Selected Movie: Displays the poster and details of the chosen movie.
* Recommended Movies: Suggestions are shown with relevant details like poster, brief description, genres, ratings, and release dates.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Future Enhancements
* Include collaborative filtering for personalized recommendations.
* Integrate availability checks on streaming platforms.
* Add support for multi-language movie metadata.

### Author
Created by ASRIN TOPAL. Contributions and suggestions are welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)