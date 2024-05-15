import streamlit as st
import pandas as pd
import datetime
import sqlite3


#preprocess
df = pd.read_csv('movies.csv')
df['Release Year']=df['Release Year'].apply(lambda x:str(x).split('.')[0] if x!='nan' else None)
df['Title']=df['Title'].astype(str)+' ('+df['Release Year'].astype(str)+')'
list_of_movies=df['Title'].unique().tolist()




#define function
def return_similar_movies(selected_value):

    filtered_df = df[df['Title']==selected_value].sort_values('Rating Count', ascending=False)
    if len(filtered_df)==0:
        st.warning("No movies found matching the input title.")
        return [], [], []
    
    filtered_movie = filtered_df.iloc[0]
    director = filtered_movie['Directors']
    genre = filtered_movie['Genres']
    
    similar_movies_df = df[(df['Directors']==director)].sort_values(['Rating Count', 'IMDB Rating'], ascending=[False, False])
    
    similar_movies_titles = similar_movies_df['Title'].tolist()
    similar_movies_posters = similar_movies_df['Poster'].tolist()
    similar_movies_urls = similar_movies_df['Movie URL'].tolist()
    
    return similar_movies_titles, similar_movies_posters, similar_movies_urls




#append to database
def append_to_database(selected_value, current_time):
    conn = sqlite3.connect('user_movie_searches.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movie_searches (movie_searched, timestamp) VALUES (?, ?)", (selected_value, current_time))
    conn.commit()
    conn.close()





#st app
st.set_page_config(layout="wide")

st.header('Movie Recommendation Project')
input_value = st.selectbox('Type movie title to get recommendations', [''] + list_of_movies)

if st.button('Show Recommended Movies') and input_value:
    titles, posters, urls = return_similar_movies(input_value)
    cols = st.columns(len(titles))

    #append data to db
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    append_to_database(input_value,current_time)


    for i, (title, poster, url) in enumerate(zip(titles, posters, urls)):
        with cols[i]:
            st.markdown(f"<span style='font-size: 14px;'><a href='{url}'>{title}</a></span>", unsafe_allow_html=True)
            st.image(poster)




# Add intro text to upper left corner
st.sidebar.markdown("# About me:")

intro_text = """
Hi!👋 \n
I'm Giorgi, and this is my latest python project. This website recommends movies based on the director's work.\n
I gathered movie data from IMDB.com using Python's Selenium and BeautifulSoup web scraping libraries.\n
If you're curious about the code and want to explore it, feel free to visit my Github account! [GitHub](https://github.com/beridzeg45)\n
You will be able to check the scraped dataset on my Kaggle page: [Kaggle](https://www.kaggle.com/datasets/beridzeg45/all-movies-on-imdb)\n
"""
st.sidebar.markdown(intro_text)




#graphs
st.header('Graphs')
st.image("timeseries.svg", use_column_width=True)
col1, col2 = st.columns(2)
col1.image("top_directors.svg", use_column_width=True)
col2.image("number_of_movies_by_genre.svg", use_column_width=True)





#most searched movies database
conn = sqlite3.connect('user_movie_searches.db')
df = pd.read_sql_query("SELECT * FROM movie_searches", conn)
conn.close()
st.dataframe(df)
