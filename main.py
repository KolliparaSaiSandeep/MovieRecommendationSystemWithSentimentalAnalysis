import streamlit as st
import pickle
import pandas as pd
import requests
import json
from w import *

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]#lambda for saying sort on basis of first index that is similarity values
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:4]
    recommended_movies=[]
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movie_posters

movies_dict=pickle.load(open(r'C:\Users\ksai1\Untitled Folder 3\Untitled Folder\movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open(r'C:\Users\ksai1\Untitled Folder 3\Untitled Folder\similarity.pkl','rb'))
st.title('Movie Recommender System')

selected_movie_name=st.selectbox('Enter movie for which u need recommendations?',movies['title'].values)

def callapi(nam):
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q": nam}
    headers = {#"710ee70cc5mshf05a9aeff4196dbp10deecjsn663f1501a0fa"
        "X-RapidAPI-Key":"710ee70cc5mshf05a9aeff4196dbp10deecjsn663f1501a0fa",# "50dcfabfddmshdc87ba3b713711cp1d0371jsn75dc5e70173e",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    a= json.loads(response.text)
    return a

def hi(nam):
    import requests
    import json
    import webbrowser
    url = "https://online-movie-database.p.rapidapi.com/title/find"

    querystring = {"q": nam}

    headers = {
        "X-RapidAPI-Key":"710ee70cc5mshf05a9aeff4196dbp10deecjsn663f1501a0fa",# "50dcfabfddmshdc87ba3b713711cp1d0371jsn75dc5e70173e",
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    a = response.text
    a = json.loads(a)
    print(a)
    b = (a["results"][0])['id']
    c = 'https://www.imdb.com'
    st.write(c + b)
    return b

load=st.button("Recommend")

if "load_state" not in st.session_state:
    st.session_state.load_state=False

if load or st.session_state.load_state:
    st.session_state.load_state=True
    names,posters=recommend(selected_movie_name)
    col1, col2, col3 = st.columns(3)
    with col1:
            st.text(names[0])
            st.image(posters[0])
            a = callapi(names[0])
            st.write("Actors-", ((a['d'])[0])['s'])
            st.write("Release Year-", ((a['d'])[0])['y'])
            b=hi(names[0])
            print("hello")
            if st.button('REVIEW',key='1'):#key is used to avoid error when multiple buttons use same name
                ji('text(names[0])',b)

    with col2:
        st.text(names[1])
        st.image(posters[1])
        a = callapi(names[1])
        st.write("Actors-", ((a['d'])[0])['s'])
        st.write("Release Year-", ((a['d'])[0])['y'])
        b=hi(names[1])
        if st.button('REVIEW',key='2'):
            ji('text(names[1])',b)

    with col3:
        st.text(names[2])
        st.image(posters[2])
        a = callapi(names[2])
        st.write("Actors-", ((a['d'])[0])['s'])
        st.write("Release Year-", ((a['d'])[0])['y'])
        b=hi(names[2])
        if st.button('REVIEW',key="3"):
            ji('text(names[2])',b)


