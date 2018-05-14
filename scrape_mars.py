
# coding: utf-8

# ## Mission to Mars

# * Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. 
# Assign the text to variables that you can reference later.


#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import time

# initialize chrome browser
browser = Browser('chrome', headless=False)

def scrape():

    # NASA website to be scrapped
    url = "https://mars.nasa.gov/news"

    # visit the page to be scrapped and wait for it to load
    browser.visit(url)
    time.sleep(2)

    # Create BeautifulSoup object
    html = browser.html
    soup = bs(html, 'html.parser') 

    # find the latest News Headline on the Nasa - mars - news page.
    news_title = soup.find('div',class_="content_title").a.text

    # find the text for the latest news headline.
    news_p = soup.find('div', class_='article_teaser_body').text

    # ### JPL Mars Space Images - Featured Image

    # url for the images website.
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # visit the images page.  note:- do not close the browser opened above. If so u have to initiate the browser again.
    browser.visit(image_url)
    # Create BeautifulSoup object
    img_html = browser.html
    soup = bs(img_html, 'html.parser')

    # find the a tag for the featured image
    href = soup.find('footer').a['data-fancybox-href']

    # append with the base url to get the full URL for the featured image
    featured_image_url = 'https://www.jpl.nasa.gov'+href

    #visit the featured image using the URL above to verify that the featured image is retrieved accurately.
    browser.visit(featured_image_url)


    # ### Mars Weather

    # URL for Mars Weather Twitter page.
    url = 'https://twitter.com/marswxreport?lang=en'

    #visit the Mars Weather Twitter page
    browser.visit(url)
    # Create BeautifulSoup object
    html = browser.html
    soup = bs(html, 'html.parser')

    #find the first tweet on the page and retrieve its text.
    mars_weather = soup.find('p', class_=  'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    # ### Mars Facts

    # import pandas
    import pandas as pd

    #URL for mars facts.
    url = 'https://space-facts.com/mars'

    # use pandas to read the above page and retrieve the firt table on the page with mars facts.
    facts_table = pd.read_html(url)
    # set the column titles for the retrieved table.
    facts_table[0].columns=['Description', 'Value']
    # convert the table retrieved to html format, set index = false, to not display the default index from Pandas
    facts_table_html = facts_table[0].to_html(index=False)  

    # ### Mars Hemispheres

    # astrogeology website URL for mars hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'

    # visit the astrogeology website
    browser.visit(url) 

    # intiates soup.
    html = browser.html
    soup = bs(html, 'html.parser') 

    # scrape the page to retrieve the mars hemispheres list displayed on the website
    links = soup.find_all('div', class_='description')
    # intialize a 'hemisphere_image_urls' list variable to hold the image dictionaries
    hemisphere_image_urls =[] 
    # loop thru the hemispheres list retrieved
    for link in links:
        image_url = {} # initialize dictionary to hold the title and image urls for the hemisphere
        href = base_url+link.a['href'] # link to the hemisphere page
        #browser = Browser('chrome', headless=False) 
        browser.visit(href) # opens the mar hemisphere in browser.
        time.sleep(1) # let the page load
        html=browser.html
        soup = bs(html, 'html.parser') # create a soup object for the page
        title = (soup.title.text).split('|')[0] # title of the mars hemisphere
        image_url['title'] = title # add the title to the dictionary
        divs = soup.find_all('div', class_ = 'downloads') #find downloadable image links for the mars hemisphere
        list_items = divs[0].ul.find_all('li') # find all list items in the div 
        # loop thru the list_items and retrieve the image URL for the Original image.
        for item in list_items:
            if (item.a.text).lower() == 'original':
                print(item.a['href'])
                image_url['image_url'] = item.a['href'] # add the image URL to the image_url dictionary
        hemisphere_image_urls.append(image_url) # append the image_url dictionary to the the hemisphere list.

    mars_info_set = {"latest_news_title": news_title,
    "latest_news_text": news_p,
    "featured_image": featured_image_url,
    "weather" : mars_weather,
    "mars_facts": facts_table_html,
    "hemispheres": hemisphere_image_urls
    }
    return mars_info_set



