import streamlit as st
import streamlit as st
import pickle
import pandas as pd
import requests



movies_list = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_list)


def search(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_id = movies[movies['title'] == movie].movie_id[movie_index]
    movie_summary = movies[movies['title'] == movie].overview[movie_index]
    movie_cast = movies[movies['title'] == movie].cast[movie_index]
    release = movies[movies['title'] == movie].release_date[movie_index]
    search_poster = fetch_poster(movie_id)
    return search_poster, movie_summary, movie_cast, release



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=12de424ece3962c5cb5e633341f33fca&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    movie_cast = []
    releaseDate = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        movie_cast.append(movies.iloc[i[0]].cast)
        releaseDate.append(movies.iloc[i[0]].release_date)

    return recommended_movies, recommended_movie_posters, movie_cast, releaseDate

title = 'Movie Recommender System'

st.title(title)

menu = ["Home", "Search", "Recommend"]

choice = st.sidebar.selectbox('Menu',menu)


if choice == 'Home':
    st.subheader("Home")
    cols = st.columns(4)
    poster = []
    home_title = []
    summary= []
    cast = []
    date = []
    for i in movies['movie_id'].iloc[:10]:
        poster.append(fetch_poster(i))

    for i in movies['title'].iloc[:10]:
        home_title.append(i)

    for i in movies['overview'].iloc[:10]:
        summary.append(i)

    for i in movies['cast'].iloc[0:10]:
           cast.append(i)

    for i in movies['release_date'].iloc[0:10]:
           date.append(i)

    col1, col2 = st.columns(2)
    col1.image(poster[0], width=200)
    option1 = col1.expander(home_title[0], False)
    option1.write(summary[0])
    option1.write("Cast :"+ " " + cast[0][0]+ " , " + cast[0][1]+ " , " + cast[0][2] )
    option1.write("Release Date :" + " " + date[0])
    col2.image(poster[1], width=200)
    option2 = col2.expander(home_title[1], False)
    option2.write(summary[1])
    option2.write("Cast :" + " " + cast[1][0] + " , " + cast[1][1] + " , " + cast[1][2])
    option2.write("Release Date :" + " " + date[1])
    col1.image(poster[2], width=200)
    option3 = col1.expander(home_title[2], False)
    option3.write(summary[2])
    option3.write("Cast :" + " " + cast[2][0] + " , " + cast[2][1] + " , " + cast[2][2])
    option3.write("Release Date :" + " " + date[2])
    col2.image(poster[3], width=200)
    option4 = col2.expander(home_title[3], False)
    option4.write(summary[3])
    option4.write("Cast :" + " " + cast[3][0] + " , " + cast[3][1] + " , " + cast[3][2])
    option4.write("Release Date :" + " " + date[3])
    col1.image(poster[4], width=200)
    option5 = col1.expander(home_title[4], False)
    option5.write(summary[4])
    option5.write("Cast :" + " " + cast[4][0] + " , " + cast[4][1] + " , " + cast[4][2])
    option5.write("Release Date :" + " " + date[4])
    col2.image(poster[5], width=200)
    option6 = col2.expander(home_title[5], False)
    option6.write(summary[5])
    option6.write("Cast :" + " " + cast[5][0] + " , " + cast[5][1] + " , " + cast[5][2])
    option6.write("Release Date :" + " " + date[5])
    col1.image(poster[6], width=200)
    option7 = col1.expander(home_title[6], False)
    option7.write(summary[6])
    option7.write("Cast :" + " " + cast[6][0] + " , " + cast[6][1] + " , " + cast[6][2])
    option7.write("Release Date :" + " " + date[6])
    col2.image(poster[7], width=200)
    option8 = col2.expander(home_title[7], False)
    option8.write(summary[7])
    option8.write("Cast :" + " " + cast[7][0] + " , " + cast[7][1] + " , " + cast[7][2])
    option8.write("Release Date :" + " " + date[7])
    col1.image(poster[8], width=200)
    option9 = col1.expander(home_title[8], False)
    option9.write(summary[8])
    option9.write("Cast :" + " " + cast[8][0] + " , " + cast[8][1] + " , " + cast[8][2])
    option9.write("Release Date :" + " " + date[8])
    col2.image(poster[9], width=200)
    option10 = col2.expander(home_title[9], False)
    option10.write(summary[9])
    option10.write("Cast :" + " " + cast[9][0] + " , " + cast[9][1] + " , " + cast[9][2])
    option10.write("Release Date :" + " " + date[9])
    with st.expander('All Movies', False):
        selected = st.selectbox('Search Movie',movies['title'].values)
        if st.button('Search'):
            poster, summary, cast, date = search(selected)
            st.image(poster, width=200)
            st.write(summary)
            st.write("Cast :" + " " + cast[0] + " , " + cast[1] + " , " + cast[2])
            st.write("Release Date :" + " " + date)


elif choice=="Search":
    st.subheader("Search")
    with st.expander("Search Movie By Year"):
        movie_year = st.number_input("",1940,2020)
        df_for_year = movies[movies['date'].dt.year == movie_year]
        df_for_year = df_for_year[['title', 'genres', 'release_date']]
        df_for_year.reset_index(inplace=True, drop=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("Titles")
            for t in df_for_year['title'].to_list():
                st.write(t)

        with col2:
            st.success("Release Date")
            for t in df_for_year['release_date'].to_list():
                st.write(t)

        with col3:
            st.success("Genres")
            for t in df_for_year['genres'].to_list():
                if len(t)>1:
                    st.write(t[0]+","+t[1] )
                else:
                    st.write(t[0])





else:
    st.subheader("Recommend")
    selected_movie_name = st.selectbox('Search For Movie Recommendations', (movies['title'].values))

    if st.button('Recommend'):
        st.write('Recommendations:')
        names, posters, cast, date = recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(posters[0])
            with st.expander(names[0]):
                st.write("Cast :" + " " + cast[0][0] + " , " + cast[0][1] + " , " + cast[0][2])
                st.write("Release Date :" + " " + date[0])
        with col2:
            st.image(posters[1])
            with st.expander(names[1]):
                st.write("Cast :" + " " + cast[1][0] + " , " + cast[1][1] + " , " + cast[1][2])
                st.write("Release Date :" + " " + date[1])
        with col3:
            st.image(posters[2])
            with st.expander(names[2]):
                st.write("Cast :" + " " + cast[2][0] + " , " + cast[2][1] + " , " + cast[2][2])
                st.write("Release Date :" + " " + date[2])
        with col4:
            st.image(posters[3])
            with st.expander(names[3]):
                st.write("Cast :" + " " + cast[3][0] + " , " + cast[3][1] + " , " + cast[3][2])
                st.write("Release Date :" + " " + date[3])
        with col5:
            st.image(posters[4])
            with st.expander(names[4]):
                st.write("Cast :" + " " + cast[4][0] + " , " + cast[4][1])
                st.write("Release Date :" + " " + date[4])
