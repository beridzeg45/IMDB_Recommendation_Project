#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
import requests
import time
import datetime as dt 
import pandas as pd

import pickle
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# In[2]:


path=r'D:\python data\movie_recommendation_project'


# In[3]:


driver=webdriver.Edge()
driver.maximize_window()


# urls=[]
# for year in range(1900,2024,1):
#     url=f'https://www.imdb.com/search/title/?title_type=feature&release_date={year}-01-01,{year}-12-31&user_rating=1,10&num_votes=100,'
#     urls.append(url)

# max_year=0
# for file in os.listdir(path):
#     if 'all_movie_urls_' in file:
#         year=int(file.split('all_movie_urls_')[-1].split('.pickle')[0])
#         if year>max_year:
#             max_year=year
# print(max_year)

# all_movie_urls=[]
# 
# for url in urls:
#     year=str(url).split('release_date=')[-1].split('-')[0]
#     if int(year)<=max_year:
#         continue
# 
#     driver.get(url)
#     time.sleep(3)
# 
#     while True:   
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 
#         try:
#             load_more_button=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button[class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--on-accent2 ipc-text-button ipc-see-more__button"]')))
#             driver.execute_script('arguments[0].scrollIntoView();',load_more_button)
#             driver.execute_script('arguments[0].click();',load_more_button)
#             time.sleep(3)
#         except:
#             break
# 
#     url_elements=driver.find_elements(By.CSS_SELECTOR,'div[class="ipc-page-grid__item ipc-page-grid__item--span-2"] li a[class="ipc-title-link-wrapper"]')
#     
#     for url_element in url_elements:
#         all_movie_urls.append(url_element.get_attribute('href'))
#     pickle.dump(all_movie_urls,open(os.path.join(path,f'all_movie_urls_{year}.pickle'),'wb'))
#     all_movie_urls=[]
#     
# 
#     print(url,end='\r')
# 

# all_movie_urls=[]
# for file in os.listdir(path):
#     if 'all_movie_urls' in file:
#         data=pickle.load(open(os.path.join(path,file),'rb'))
#         all_movie_urls=all_movie_urls+data
#         print(file,end='\r')
# 
# all_movie_urls=list(set(all_movie_urls))
# all_movie_urls=sorted(all_movie_urls)
# pickle.dump(all_movie_urls,open(os.path.join(path,'all_movie_urls.pickle'),'wb'))

# In[ ]:


all_movie_urls=pickle.load(open(os.path.join(path,'all_movie_urls.pickle'),'rb'))
len(all_movie_urls)


# In[5]:


def return_movie_info(movie_url):  

    try:
        driver.get(movie_url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        pass
    
    try:
        poster=driver.find_element(By.CSS_SELECTOR,'div[class="ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2"] img').get_attribute('src')
    except:
        poster=None

    try:
        movie_title=driver.find_element(By.CSS_SELECTOR,'div[class="sc-b7c53eda-0 dUpRPQ"] h1[data-testid="hero__pageTitle"]').text.replace('\n','')
    except:
        movie_title=None

    try:
        year=driver.find_element(By.CSS_SELECTOR,'ul[class="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"]').text
    except:
        year=None

    try:
        rating=driver.find_element(By.CSS_SELECTOR,'div[class="sc-bde20123-0 dLwiNw"]').text
    except:
        rating=None

    try:
        summary=driver.find_element(By.CSS_SELECTOR,'div[data-testid="storyline-plot-summary"]').text.replace('\n','')
    except:
        summary=None

    try:
        plot=driver.find_element(By.CSS_SELECTOR,'p[data-testid="plot"]').text.replace('\n','')
    except:
        plot=None

    try:
        director=driver.find_element(By.CSS_SELECTOR,'div[class="sc-b7c53eda-3 vXcqY"]').text
    except:
        director=None

    try:
        genres=driver.find_element(By.CSS_SELECTOR,'div[data-testid="genres"]').text
    except:
        genres=None
    
    info_dict={'Movie URL':movie_url,'Title':movie_title,'Poster':poster,'Year':year,'Rating':rating,'Summary':summary,'Plot':plot,'Director':director,'Genres':genres}
    return info_dict


# In[7]:


all_data=[]

for i,movie_url in enumerate(all_movie_urls,start=1):
    info_dict=return_movie_info(movie_url)
    all_data.append(info_dict)

    if i%1000==0 or i==len(all_data):
        pickle.dump(all_data,open(os.path.join(path,f'all_data_{i}'),'wb'))
        all_data=[]

    print(i,end='\r')



# In[ ]:




