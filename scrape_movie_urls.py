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


# In[ ]:


urls=[]
for year in range(1900,2024,1):
    url=f'https://www.imdb.com/search/title/?title_type=feature&release_date={year}-01-01,{year}-12-31&user_rating=1,10&num_votes=100,'
    urls.append(url)


# In[ ]:


max_year=0
for file in os.listdir(path):
    if 'all_movie_urls_' in file:
        year=int(file.split('all_movie_urls_')[-1].split('.pickle')[0])
        if year>max_year:
            max_year=year
print(max_year)


# In[ ]:


all_movie_urls=[]

for url in urls:
    year=str(url).split('release_date=')[-1].split('-')[0]
    if int(year)<=max_year:
        continue

    driver.get(url)
    time.sleep(3)

    while True:   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            load_more_button=WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,'button[class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-base ipc-btn--theme-base ipc-btn--on-accent2 ipc-text-button ipc-see-more__button"]')))
            driver.execute_script('arguments[0].scrollIntoView();',load_more_button)
            driver.execute_script('arguments[0].click();',load_more_button)
            time.sleep(3)
        except:
            break

    url_elements=driver.find_elements(By.CSS_SELECTOR,'div[class="ipc-page-grid__item ipc-page-grid__item--span-2"] li a[class="ipc-title-link-wrapper"]')
    
    for url_element in url_elements:
        all_movie_urls.append(url_element.get_attribute('href'))
    pickle.dump(all_movie_urls,open(os.path.join(path,f'all_movie_urls_{year}.pickle'),'wb'))
    all_movie_urls=[]
    

    print(url,end='\r')


# In[ ]:


all_movie_urls=[]
for file in os.listdir(path):
    if 'all_movie_urls' in file:
        data=pickle.load(open(os.path.join(path,file),'rb'))
        all_movie_urls=all_movie_urls+data
        print(file,end='\r')

all_movie_urls=list(set(all_movie_urls))
all_movie_urls=sorted(all_movie_urls)
pickle.dump(all_movie_urls,open(os.path.join(path,'all_movie_urls.pickle'),'wb'))


# In[ ]:


all_movie_urls=pickle.load(open(os.path.join(path,'all_movie_urls.pickle'),'rb'))
len(all_movie_urls)

