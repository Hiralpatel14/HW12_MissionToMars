# import dependencies
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import requests
import time
import re
import os
#from selenium import webdriver

#define scrap function
def scrape():
    #create a library to hold all Mars Data
    mars_lib = {}
    
    #url for page scrap
    nasa_url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(nasa_url)
    
    #Create BeautifulSoup object; parse with 'lxml'
    #soup1 = BeautifulSoup(response.text, 'html.parser')
    soup1 = BeautifulSoup(response.text, 'lxml')
    type(soup1)

    #scrapping latest news 
    #news_titles = soup.find('div', class_='content_title').text
    news_title1 = soup1.find_all('div', class_='content_title')[0].find('a').text.strip()
    news_p = soup1.find_all('div', class_ = 'rollover_description_inner')[0].text.strip()
    
    mars_lib["news_title1"]= news_title1
    mars_lib["news_p"] = news_p

    ## JPL Mars images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(jpl_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup2 = BeautifulSoup(response.text, 'lxml')
    type(soup2)
    
    images = soup2.find_all('div', class_='carousel_items')
    for img in images:
        image = img.find('article')
        background_image = image.get('style')
        print(background_image)
    # extract url
    re_background_image = re.search("'(.+)'",background_image)
    search_background_image= re_background_image.group(1)
    featured_image_url = f'https://www.jpl.nas/gov{search_background_image}'
    print(featured_image_url)

    ##or extra jpl image
    part_address = soup2.find_all('a',class_='fancybox')[0].get('data-fancybox-href').strip()
    Featured_img_url = "https://www.jpl.nas/gov"+part_address
    print(Featured_img_url)

    #put info into library
    mars_lib["featured_image_url"] = featured_image_url

    ##3 Mars Weather
    # from url parse file with beautifulSoup
    Twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(Twitter_url)
    Twit_soup = BeautifulSoup(response.text, 'lxml')
    type(Twit_soup)
    #scrap Mars  weather Tweet    
    mars_weather = Twit_soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    
    # put info into library
    mars_lib['mars_weather'] = mars_weather


    ### Mars Facts
    # URL of Page to scraped
    Fact_url = 'https://space-facts.com/mars/'
    # To get the url table
    tables = pd.read_html(Fact_url)
    # convert list of table into pandas Dataframe
    Fact_df = tables[0]
    # update columns name
    Fact_df.columns = ['Description', 'Mars_Value', 'Earth_Value']
    Fact_df.set_index('Description', inplace=True)
    mars_facts = Fact_df.to_html(justify='left')
    # put info into library
    mars_lib['mars_facts'] = mars_facts


    ### Mars Hemisperes
    #url for page scrap
    Hemp_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(Hemp_url)
    # Create BeautifulSoup object; parse with 'lxml'
    Hemp_soup = BeautifulSoup(response.text, 'html5lib')

    #assigned list to store:
    hemisphere_image_urls =[]
    #create empty dictionary
    dict = {}

    # get all Titles
    results = Hemp_soup.find_all('h3')
    # loop through each result
    for r in results:
        #get text info from result
        itema = r.text
        time.sleep(1)
      
        #assign html content
        htmla =response.text
        
        # create a BeautifulSoup
        soupa = BeautifulSoup(htmla,'lxml')
        time.sleep(1)
        #grab the image link
        linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
         #pass title to dict
        time.sleep(1)
        dict["title"]=itema
        dict["img_url"] = linka
        #append dict to the list
        hemisphere_image_urls.append(dict) 
         # clean up dict         
        dict = {}                       
        time.sleep(1)

    # put info into library
    mars_lib["hemisphere_image_urls"] = hemisphere_image_urls   


    # return library
    return mars_lib