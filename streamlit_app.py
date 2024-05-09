import streamlit as st
import pandas as pd

df = pd.read_csv('movies.csv')

#define function
def return_similar_movies(selected_value):
    selected_value = selected_value.lower()
    filtered_df = df[df['Title'].str.lower().fillna('').str.contains(selected_value)].sort_values('Rating Count', ascending=False)
    if len(filtered_df)==0:
        st.warning("No movies found matching the input title.")
        return [], [], []
    
    filtered_movie = filtered_df.iloc[0]
    director = filtered_movie['Directors']
    genre = filtered_movie['Genres']
    
    similar_movies_df = df[
        (df['Directors'].str.contains(director, na=False,case=False)) &
        (df['Genres'].str.contains(genre, na=False,case=False)) &
        (df['Title'].notna())
    ].sort_values(['Rating Count', 'IMDB Rating'], ascending=[False, False])
    
    similar_movies_titles = similar_movies_df['Title'].tolist()
    similar_movies_posters = similar_movies_df['Poster'].tolist()
    similar_movies_urls = similar_movies_df['Movie URL'].tolist()
    
    return similar_movies_titles, similar_movies_posters, similar_movies_urls




#st app
st.set_page_config(layout="wide")

st.header('Movie Recommendation Project')
input_value = st.text_input('Type movie title to get recommendations', '')

if st.button('Show Recommended Movies') and input_value:
    titles, posters, urls = return_similar_movies(input_value)
    cols = st.columns(len(titles))

    for i, (title, poster, url) in enumerate(zip(titles, posters, urls)):
        with cols[i]:
            st.markdown(f"<span style='font-size: 14px;'><a href='{url}'>{title}</a></span>", unsafe_allow_html=True)
            st.image(poster)


# Add intro text to upper left corner
intro_text="""
\n\n\n
Hi! I'm Giorgi, and this is my latest python project. This website recommends movies based on the director's work.\n
I gathered movie data from IMDB.com using Python's Selenium and BeautifulSoup web scraping libraries.\n
If you're curious about the code and want to explore it, feel free to visit my Github account! (https://github.com/beridzeg45)\n
"""
st.write("<div style='text-align: left;'>" + intro_text + "</div>", unsafe_allow_html=True)
