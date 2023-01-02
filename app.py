import pickle
import streamlit as st
import base64
from pathlib import Path

# Loading Required Pickle Files
movies = pickle.load(open('./movie_data.pkl', 'rb'))
similarity = pickle.load(open('./recommendation_engine.pkl', 'rb'))


def fetch_poster(id):
    poster_index = movies[movies['id'] == id]['poster_path'].iloc[0]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_index
    return full_path


def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:21]:
        id = movies.iloc[i[0]].id  # fetch the movie poster
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie_names.append(movies.iloc[i[0]].original_title)
    return recommended_movie_names, recommended_movie_posters


def movie_info(movie_index):
    movie_detail = movies[movies['original_title'] == recommended_movie_names[movie_index]][['genre', 'release_year', 'original_language', 'vote_average', 'overview']]
    st.write(f"Genre : {movie_detail['genre'].iloc[0]}")
    st.write(f"Release Year : {movie_detail['release_year'].iloc[0]}")
    st.write(f"Original Language : {movie_detail['original_language'].iloc[0]}")
    st.write(f"Vote Average : {movie_detail['vote_average'].iloc[0]}")
    st.write(f"Overview : {movie_detail['overview'].iloc[0]}")
    return


# ---- Movie Recommender System Home Page ----
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")


page_title = "Movie Recommendation System"
text_style = f"<h1 style='font-family:Georgia, serif; text-align:center; color:#f0fff0; font-size:35px;'>{page_title}</h1>"
st.markdown(text_style, unsafe_allow_html=True)


# ---- Setting Up Background ----
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
background_image = current_dir / "background" / "background.jpg"
css_style = current_dir / "styles" / "home_page.css"

with open(background_image, "rb") as f:
    data = f.read()
img = base64.b64encode(data).decode()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: center;
background-repeat: round;
background-attachment: repeat-y;
background-size: cover;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


col1, col2, col3 = st.columns([2, 6, 2])
with col2:
    # DropDown menu
    movie_list = movies['original_title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list, index=1)


if st.button('Show Recommendation'):

    # ---- Info About Selected Movie ----
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4 = st.columns([1,4,4,1])

    movie_data = movies[movies['original_title'] == selected_movie] # selected movie data
    with col2: # selected Movie poster
        st.image(fetch_poster(movie_data['id'].iloc[0]), width=325)
    with col3:  # selected Movie Details
        # Movie Name
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:50px;'>**{selected_movie}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)
        # Movie Genre
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:22px;'>**Genre : {movie_data['genre'].iloc[0]}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)
        # Release Year
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:22px;'>**Release Year : {movie_data['release_year'].iloc[0]}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)
        # Release Year
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:22px;'>**Original Language : {movie_data['original_language'].iloc[0]}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)
        # Release Year
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:22px;'>**Vote Average : {movie_data['vote_average'].iloc[0]}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)
        # Release Year
        display_text = f"<p1 style='font-color:#f0ffff; family-font:serif; text-align:center; font-size:22px;'>**Overview : {movie_data['overview'].iloc[0]}**</p1>"
        st.markdown(display_text, unsafe_allow_html=True)

    for i in range(4):
        st.write(' ')

    # ---- Recommending Movies ----
    movie0, movie1, movie2, movie3 = st.columns(4)

    with movie0:
        st.image(recommended_movie_posters[0], width=250)
        # display_text = f"<p1 style='text-align:center; font-size:20px;'>**{recommended_movie_names[0]}**</p1>"
        # st.markdown(display_text, unsafe_allow_html=True)
        with st.expander(recommended_movie_names[0]):
            movie_info(0)
    with movie1:
        st.image(recommended_movie_posters[1], width=250)
        with st.expander(recommended_movie_names[1]):
            movie_info(1)
    with movie2:
        st.image(recommended_movie_posters[2], width=250)
        with st.expander(recommended_movie_names[2]):
            movie_info(2)
    with movie3:
        st.image(recommended_movie_posters[3], width=250)
        with st.expander(recommended_movie_names[3]):
            movie_info(3)

    movie4, movie5, movie6, movie7 = st.columns(4)
    with movie4:
        st.image(recommended_movie_posters[4], width=250)
        with st.expander(recommended_movie_names[4]):
            movie_info(4)
    with movie5:
        st.image(recommended_movie_posters[5], width=250)
        with st.expander(recommended_movie_names[5]):
            movie_info(5)
    with movie6:
        st.image(recommended_movie_posters[6], width=250)
        with st.expander(recommended_movie_names[6]):
            movie_info(6)
    with movie7:
        st.image(recommended_movie_posters[7], width=250)
        with st.expander(recommended_movie_names[7]):
            movie_info(7)

    col8, col9, col10, col11 = st.columns(4)
    with col8:
        st.image(recommended_movie_posters[8], width=250)
        with st.expander(recommended_movie_names[8]):
            movie_info(8)
    with col9:
        st.image(recommended_movie_posters[9], width=250)
        with st.expander(recommended_movie_names[9]):
            movie_info(9)
    with col10:
        st.image(recommended_movie_posters[10], width=250)
        with st.expander(recommended_movie_names[10]):
            movie_info(10)
    with col11:
        st.image(recommended_movie_posters[11], width=250)
        with st.expander(recommended_movie_names[11]):
            movie_info(11)

    col12, col13, col14, col15 = st.columns(4)
    with col12:
        st.image(recommended_movie_posters[12], width=250)
        with st.expander(recommended_movie_names[12]):
            movie_info(12)
    with col13:
        st.image(recommended_movie_posters[13], width=250)
        with st.expander(recommended_movie_names[13]):
            movie_info(13)
    with col14:
        st.image(recommended_movie_posters[14], width=250)
        with st.expander(recommended_movie_names[14]):
            movie_info(14)
    with col15:
        st.image(recommended_movie_posters[15], width=250)
        with st.expander(recommended_movie_names[15]):
            movie_info(15)

    col16, col17, col18, col19 = st.columns(4)
    with col16:
        st.image(recommended_movie_posters[16], width=250)
        with st.expander(recommended_movie_names[16]):
            movie_info(16)
    with col17:
        st.image(recommended_movie_posters[17], width=250)
        with st.expander(recommended_movie_names[17]):
            movie_info(17)
    with col18:
        st.image(recommended_movie_posters[18], width=250)
        with st.expander(recommended_movie_names[18]):
            movie_info(18)
    with col19:
        st.image(recommended_movie_posters[19], width=250)
        with st.expander(recommended_movie_names[19]):
            movie_info(19)

    # Use Local Contact CSS File
    with open(css_style) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

