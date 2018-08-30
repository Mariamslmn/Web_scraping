# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
import time


def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
#browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}

    #collect the latest News Title and Paragraph Text
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    news_text = soup.find('div', class_="content_title").text
    news_p =  soup.find('div', class_="article_teaser_body").text

    #store in a dictionary:
    mars_info["news_text"]= news_text
    mars_info["news_p"]= news_p
                

    #JPL Mars Space Images - Featured Image

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # results are returned as an iterable list
    article = soup.find('article', class_='carousel_item')

    url = article['style']
    featured_image_url = 'https://www.jpl.nasa.gov' + url.replace('background-image: ','').replace('url(', '').replace(')', '').replace("'","").replace(';','') 

        
    # add item
    mars_info['featured_image_url'] = featured_image_url 



    # Mars Weather:

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    #mars weather
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_info['mars_weather'] = mars_weather


    # Mars Facts:
    url4 = 'https://space-facts.com/mars/'
    time.sleep(5)
    tables = pd.read_html(url4)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['description', 'value']
    mars_facts_df.set_index(mars_facts_df.columns[0], inplace = True)

    # convert the data to a HTML table string:
    html_table = mars_facts_df.to_html()
    html_table=html_table.replace('\n', ' ')
    mars_info['html_table'] = html_table
    print(mars_info["html_table"])

    #save table
    mars_facts_df.to_html('mars_facts_df1.html')



    #Mars Hemispheres:

    mars_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']    

    hemisphere_image_urls = []

    for mars_url in mars_urls:
        browser.visit(mars_url)

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        #----------------------------------------------------------------------
        # Return Image URL:
        images = soup.find_all('div', class_='wide-image-wrapper')

        # Iterate through each image
        for image in images:
                # Use Beautiful Soup's find() method to navigate and retrieve attributes
                img = image.find('img', class_="wide-image")
                image_url = img['src']

                #complete url:
                img_url = 'https://astrogeology.usgs.gov'+ image_url


        # Return Image URL:
        img_titles = soup.find_all('section', class_='block metadata')

        # Iterate through each title
        for img_title in img_titles:
                # Use Beautiful Soup's find() method to navigate and retrieve attributes
                title = img_title.find('h2', class_="title").text

                #create a dictionary 
                mars_dict={"title":title,"img_url":img_url}
                hemisphere_image_urls.append(mars_dict)
        #--------------------------------------------------------------------------------        
        
        mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        
        
    #print(mars_info)
    # return one Python dictionary containing all of the scraped data:
    return(mars_info)       

