import pandas as pd
import pymongo
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #Mars News

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')
    slide_elem = soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    browser.quit()

    print("---------------Mars News Scraping Complete---------------")

    ## JPL Mark Space Images
    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url= 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(2)
    current_html = browser.html
    #beautifulsoup
    image_soup = bs(current_html, 'html.parser')
    random_img_url = image_soup.find('img', class_='thumbimg')['src']
    featured_img_url = url + random_img_url

    browser.quit()
    
    print("---------------JPL Mark Space Images Scraping Complete---------------")
    
    
    ## Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.columns = ['Comparison', 'Mars', 'Earth']
    mars_df.set_index('Comparison', inplace=True)
    
    print("---------------Mars Facts Scraping Complete---------------")

    ## Mars Hemispheres Image Url

    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)
    mars_hem_url = browser.html

    mars_hemi_soup = bs(mars_hem_url, 'html.parser')
    hem_img_class = mars_hemi_soup.find_all('div', class_='item')
    hem_img_class[0]

    url = 'https://marshemispheres.com/'
    hem_img_urls = []

    for i in hem_img_class:
        img_title = i.find('h3').text
        img_url = i.find('a')['href']
        #visit link
        browser.visit(url+img_url)
        #store html
        img_html = browser.html
        #soup
        img_soup = bs(img_html, 'html.parser')
        #retrieve img url
        ret_img_url = img_soup.find('img', class_='wide-image')['src']
        #img url
        final_img_url = url + ret_img_url
        #append
        hem_img_urls.append({'title':img_title, 'img_url':final_img_url})

    hem_img_urls
    browser.quit()
    
    print("---------------Mars Hemispheres Scraping Complete---------------")
    
    
    
    mars_data_dict = {}
    
    mars_data_dict['news_title'] = news_title
    mars_data_dict['news_p'] = news_p
    mars_data_dict['featured_img_url'] = featured_img_url
    
    mars_facts = mars_df.to_html(header=True, index=True)
    mars_data_dict['mars_facts'] = mars_facts
    
    mars_data_dict['hem_img_urls'] = hem_img_urls
    
    return mars_data_dict
    

