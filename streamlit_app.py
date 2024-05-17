import streamlit as st
import pandas as pd
import sqlite3
import datetime
import matplotlib.pyplot as plt
plt.style.use('ggplot')


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
Apart from recommendations, the project involvs exploratory data analysis on movies, visualized by matplotlib graphs\n
Also, you will find information on most searched movies on this site by users, as well as daily user traffic\n 
If you're curious about the code and want to explore it, feel free to visit my Github account! [GitHub](https://github.com/beridzeg45)\n
You will be able to check the scraped dataset on my Kaggle page: [Kaggle](https://www.kaggle.com/datasets/beridzeg45/all-movies-on-imdb)\n
"""
st.sidebar.markdown(intro_text)




#graphs
st.markdown("<br><br>", unsafe_allow_html=True)
st.header('Graphs')
st.image("timeseries.png", use_column_width=True)
col1, col2 = st.columns(2)
col1.image("top_directors.png", use_column_width=True)
col2.image("number_of_movies_by_genre.png", use_column_width=True)





#most searched movies database
conn = sqlite3.connect('user_movie_searches.db')
df = pd.read_sql_query("SELECT * FROM movie_searches", conn)
conn.close()

st.markdown("<br><br>", unsafe_allow_html=True)
st.header('Website Traffic And Search Stats')

col1, col2 = st.columns(2)
df['timestamp']=pd.to_datetime(df['timestamp'])
top_10=df.groupby('movie_searched')['user_id'].count().sort_values(ascending=False).reset_index().rename(columns={'mvoie_searched':'Title','user_id':'Search Count'}).head(10)
with col1:
    st.subheader('10 Most Frequently Searched Movies')
    st.dataframe(top_10)


fig, ax = plt.subplots(figsize=(8,4))
fig_data = df.groupby(df['timestamp'].dt.to_period('D'))['user_id'].count()
fig_data.plot.line(marker='.', xlabel='Date', ylabel='Visitors', title='Visitors By Date', ax=ax)
col2.pyplot(fig)
