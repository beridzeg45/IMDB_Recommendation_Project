from bs4 import BeautifulSoup
import requests
import time
import datetime as dt 
import pandas as pd

import pickle
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}




path=r'D:\python data\movie_recommendation_project'



all_movie_urls=pickle.load(open(os.path.join(path,'all_movie_urls.pickle'),'rb'))
len(all_movie_urls)



def return_movie_info(movie_url):  

    try:
        html=requests.get(movie_url,headers=headers).content
        soup=BeautifulSoup(html,'html.parser')
    except:
        pass
    
    try:
        poster=soup.select_one('div[class="ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2"] img')['src']
    except:
        poster=None

    try:
        movie_title=soup.select_one('div[class="sc-b7c53eda-0 dUpRPQ"] h1[data-testid="hero__pageTitle"]').text.replace('\n','')
    except:
        movie_title=None

    try:
        year=soup.select_one('ul[class="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"]').get_text(separator='|')
    except:
        year=None

    try:
        rating=soup.select_one('div[class="sc-bde20123-0 dLwiNw"]').get_text(separator='|')
    except:
        rating=None

    try:
        summary=soup.select_one('div[data-testid="storyline-plot-summary"]').text.replace('\n','')
    except:
        summary=None

    try:
        plot=soup.select_one('p[data-testid="plot"]').text.replace('\n','')
    except:
        plot=None

    try:
        director=soup.select_one('div[class="sc-b7c53eda-3 vXcqY"]').get_text(separator='|')
    except:
        director=None

    try:
        genres=soup.select_one('div[data-testid="genres"]').get_text(separator='|')
    except:
        genres=None
    
    info_dict={'Movie URL':movie_url,'Title':movie_title,'Poster':poster,'Year':year,'Rating':rating,'Summary':summary,'Plot':plot,'Director':director,'Genres':genres}
    return info_dict


max_index=0 
for file in os.listdir(path): 
    if 'all_data_' in file: 
        index=int(file.split('all_data_')[-1].split('.pickle')[0]) 
        if index>max_index: 
            max_year=index

all_data=[]

for i,movie_url in enumerate(all_movie_urls,start=1):
    if i<=max_index:
        continue
    info_dict=return_movie_info(movie_url)
    all_data.append(info_dict)

    if i%1000==0 or i==len(all_data):
        pickle.dump(all_data,open(os.path.join(path,f'all_data_{i}'),'wb'))
        all_data=[]

    print(i,end='\r')




