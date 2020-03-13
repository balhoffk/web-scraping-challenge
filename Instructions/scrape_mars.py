#!/usr/bin/env python
# coding: utf-8

# In[80]:


# Import dependencies - Splinter and BeautifulSoup and twitter stuff

from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import tweepy
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests


# In[81]:
#create scrape dictionary
scrape = {}
def mars_scrape():

#MARS NASA NEWS SITE


# In[82]:


# Add URL of site/retrieve
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)


# In[83]:


#create BeautifulSoup object
    soup = bs(response.text, 'html.parser')


# In[84]:


#prettify
    print(soup.prettify())


# In[85]:


# find the first article, save it as news_title, find paragraph text
    results = soup.find_all('div', class_ = "content_title")
    headlines = []
    for result in results:
        headlines.append(result.a.text.strip())
    
    news_title = headlines[0]

    print(news_title)


# In[86]:


#Find article text, save as news_p
    paragraph_results = soup.find_all('div', class_="rollover_description_inner")
    paragraph = []
    for paragraph_result in paragraph_results:
        paragraph.append(paragraph_result.text.strip())
       
    news_p = paragraph[0]

    print(news_p)
    scrape['news_title'] = news_title
    scrape['news_text'] = news_p


# In[112]:


#JPL Space Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[95]:


# Visit URL of img
    urlimg = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(urlimg)


# In[96]:


# Find the image
    html = browser.html
    soup = bs(html, 'html.parser')
    buttons = soup.find_all('a', class_='button fancybox')


# In[97]:


#click image to go to webpage
    browser.click_link_by_id('full_image')


# In[98]:


#new page/navigate to more info
    html = browser.html
    soup = bs(html, 'html.parser')
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()


# In[99]:


# Parse
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')


# In[100]:


# relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    img_url_rel


# In[102]:


# final url
    featured_image_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    featured_image_url
    scrape['img url'] = featured_image_url

# In[119]:


#Mars Weather


# In[144]:


#repasting in chromedriver cause this stuff keeps not working

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[145]:


    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)


# In[146]:


    html = browser.html
    weather = bs(html, 'html.parser')


# In[155]:


    print(weather.prettify())


# In[158]:


# Find `Mars Weather` tweet
    mars_weather_tweet = weather.find_all('span')


# In[161]:


#Save as Mars Weather
    mars_weather_soup = mars_weather_tweet.find('span', attrs={"class": "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})
    mars_weather = mars_weather_tweet.find_all('tweet','').get_text()
    mars_weather
    scrape['weather'] = mars_weather


# In[ ]:


#mars facts


# In[128]:


    url_facts = 'https://space-facts.com/mars/'
    facts = pd.read_html(url_facts)
    facts


# In[129]:


#create pandas df
    df_facts = facts[0]
    df_facts.columns = ['Planet Facts', 'Mars']
    df_facts.head()


# In[131]:


#transfer to html
    html_facts = df_facts.to_html()
#html_facts
    html_facts.replace('\n','')


# In[132]:


    df_facts.to_html('spacefactsmars.html')
    scrape['mars_facts'] = html_facts


# In[127]:


#hemispheres


# In[177]:


#repasting in chromedriver cause this stuff keeps not working

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[178]:


    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)


# In[179]:


    hemisphere_image_urls = []


# In[181]:


    for i in range (4):
        hemis = browser.find_by_tag('h3')
        hemis[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2',class_='title').text
        img = soup.find('img', class_='wide-image')['src']
        img_url = f'https://astrogeology.usgs.gov{img}'
    #APPEND
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
        
        browser.back()
    
    print(hemisphere_image_urls)
    scrape['hemis'] = hemisphere_image_urls

