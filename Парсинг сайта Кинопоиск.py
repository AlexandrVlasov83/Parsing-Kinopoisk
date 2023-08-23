#!/usr/bin/env python
# coding: utf-8

# ### Парсинг сайта Кинопоиск

# In[42]:


import pandas as pd
import requests


# In[163]:


from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from tqdm import tqdm, trange, tqdm_notebook
from tqdm.notebook import tqdm


# In[645]:


import re


# In[ ]:


import datetime
from datetime import timedelta


# In[1037]:


driver = webdriver.Chrome()
driver.maximize_window()
driver2 = webdriver.Chrome()
driver2.maximize_window()


# In[1038]:


with open('movies_top500.csv','w',encoding='utf-8') as mi:       # Открываем файл на запись
    mi.write('name | country | year | link | ganre | description | time | rating | research_date | page | number\n')
    url_page = 1
    count_page = 10                    # !!! Обязательно указать количество страниц
    while url_page <= count_page:
        for u in tqdm(range(1),desc=f'page number {url_page}',mininterval=0.01,position=0):
            k = 1
            time_now = datetime.datetime.now()
            time_str = datetime.datetime.strftime(time_now, '%Y,%m,%d')
            research_date = datetime.datetime.strptime(time_str,'%Y,%m,%d')
            url_online = f'https://www.kinopoisk.ru/lists/movies/top500/?page={url_page}'  # !!! Необходимо взять актуальную ссылку для корректной работы
            try:
                driver.get(url_online)
                sleep(2)
                blocks = driver.find_element(By.TAG_NAME, 'main')
                posts = blocks.find_elements(By.CLASS_NAME, 'styles_upper__j8BIs')
            except:
                mi.close()
                break
            
            for post in posts:
                link = post.find_element(By.CLASS_NAME, 'styles_main__Y8zDm').find_element(By.TAG_NAME, 'a').get_attribute('href')
                try:
                    driver2.get(link)
                    sleep(1)
                except:
                    pass
                try:
                    blocks_inner = driver2.find_element(By.TAG_NAME, 'main')
                    posts_inner = blocks_inner.find_element(By.CLASS_NAME, 'styles_paragraph__wEGPz').text
                except:
                    posts_inner = 'None'
                name = post.find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'span').text
                try:
                    t = post.find_element(By.CLASS_NAME, 'styles_main__Y8zDm').find_element(By.CLASS_NAME, 'desktop-list-main-info_truncatedText__IMQRP').text
                except:
                    pass
                try:
                    country = re.search(r'(^.*)(\s)(•)(\s)(.*)(\s)(\s)(Режиссёр)',t).groups()[0]
                except:
                    try:
                        country = re.search(r'(^.*)(\s)(•)(\s)(.*)',t).groups()[0]
                    except:
                        try:
                            country = re.search(r'([А-Я]\w*)(\s+)( Режиссёр)',t).groups()[0]
                        except:
                            country = 'None'
                try:
                    ganre = re.search(r'(^.*)(\s)(•)(\s)(.*)(\s)(\s)(Режиссёр)',t).groups()[4]
                except:
                    try:
                        ganre = re.search(r'(^.*)(\s)(•)(\s)(.*)',t).groups()[4]
                    except:
                        try:
                            ganre = re.search(r'([а-я]\w*)(\s+)( Режиссёр)',inform4).groups()[0]
                        except:
                            ganre = 'None'
                try:
                    rating = post.find_element(By.CLASS_NAME, 'styles_kinopoiskValuePositive__vOb2E').text
                except:
                    try:
                        rating = post.find_element(By.CLASS_NAME, 'styles_kinopoiskValueNeutral__sW9QT').text
                    except:
                        try:
                            rating = post.find_element(By.CLASS_NAME, 'styles_kinopoiskValueNegative__Y75Rz').text
                        except:
                            rating = 'None'
                try:
                    j = post.find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryTitleSlot__mc0mI').find_element(By.CLASS_NAME, 'desktop-list-main-info_secondaryText__M_aus').text
                except:
                    pass
                try:
                    year = re.search(r'(\d{4})(\s*,\s*)(\d*)',j).groups()[0]
                except:
                    try:
                        year = re.search(r'(\d{4})',j).groups()[0]
                    except:
                        year = 'None'
                try:
                    time = re.search(r'(\d{4})(\s*,\s*)(\d*)',j).groups()[2]
                except:
                    time = 'None'
                mi.write(f'{name}|{country}|{year}|{link}|{ganre}|{posts_inner}|{time}|{rating}|{research_date}|{url_page}|{k}\n')
                k += 1
        url_page += 1
    mi.close()
    print('Парсинг сайта окончен. Все данные сохранены в файле "movies_top500.csv"')


# In[1047]:


movies_top500 = pd.read_csv('movies_top500.csv',sep='|', encoding='utf-8')
movies_top500.head(5)


# In[1050]:


movies_top500.columns


# In[1056]:


movies_top500.columns = ['name', 'country', 'year', 'link', 'ganre', 'description','time', 'rating', 'research_date', 'page', 'number']


# In[1061]:


movies_top500.name.unique()


# In[1016]:


movies_top500.time.unique()


# In[1170]:


import matplotlib.pyplot as plt


# In[1174]:


movies_top500['ganre'].hist(backend='plotly')


# In[1176]:


movies_top500['country'].hist(backend='plotly')


# In[1185]:


movies_top500['rating'].hist(backend='plotly')


# In[1186]:


movies_top500['year'].hist(backend='plotly')


# In[1175]:


for x in movies_top500.ganre.unique():
    print(x)
    plt.figure()
    plt.show()
    plt.hist(movies_top500[movies_top500.ganre == x].rating,50)
    plt.show()


# In[1131]:


import seaborn as sns


# In[1194]:


sns.pairplot(movies_top500[['rating','year']], y_vars='rating',hue='rating', palette='Set1',height=5)


# In[1147]:


def ganre_identification(data):
    for i, j in enumerate(movies_top500.ganre.unique()):
        if data == j:
            return i


# In[1149]:


movies_top500['ganre_identification'] = movies_top500.ganre.apply(ganre_identification)


# In[1158]:


movies_top500.tail(10)


# In[1197]:


sns.pairplot(movies_top500[['rating','ganre_identification']], hue='rating', height=5, palette='Set1')


# In[1169]:


movies_top500.groupby('ganre').mean().reset_index().sort_values('ganre_identification')[['ganre','ganre_identification']]


# In[1130]:


movies_top500.to_excel('movies_top500.xlsx')

