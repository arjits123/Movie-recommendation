import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')
movies_dict = pickle.load(open('movies_todict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarities = pickle.load(open('similarities.pkl', 'rb'))

selected_movie_name = st.selectbox('Please enter the movie name you want to watch:', movies['title'].values )


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1e81603975601c3b788394aa6b44415f'.format(movie_id))
    data = response.json()  
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    # sort by second number in decreasing order (2977, 0.1305582419667734), use lambda functions 
    distances = sorted(list(enumerate(similarities[index])),reverse=True,key = lambda x: x[1]) # enumerate holds the index position 
    recommended_movies = []
    recommended_movies_poster = []
    for i in distances[1:10]:
        #i[0] is the movie id
        movie_id = movies.iloc[i[0]].movie_id

        # fetch the movie names
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch the poster
        recommended_movies_poster.append(fetch_poster(movie_id))  
    return recommended_movies, recommended_movies_poster

if st.button('recommend'):
        # recommendations = recommend(selected_movie_name)
        # for i in recommendations:
        #     st.write(i)

        names, posters  = recommend(selected_movie_name)
        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
             st.text(names[0])
             st.image(posters[0])
        with col2:
             st.text(names[1])
             st.image(posters[1])
        with col3:
             st.text(names[2])
             st.image(posters[2])
        with col4:
             st.text(names[3])
             st.image(posters[3])
        with col5:
             st.text(names[4])
             st.image(posters[4])