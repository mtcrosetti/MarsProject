import requests
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import os
from flask_table import Table, Col

chrome_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe"

fact_dict =[
    {"description": "Equatorial Diameter", "value":"6792 km"},
    {"description": "Polar Diameter", "value":"6752 km"},
    {"description": "Mass", "value":"6.42 x 10^23 kg (10.7% Earth"},
    {"description": "Moons", "value":"2 (Phobos & Deimos"},
    {"description": "Orbit Distance", "value":"227,943,824 km (1.52 AU)"},
    {"description": "Orbit Period", "value":"687 days (1.9 years)"},
    {"description": "Surface Temperature", "value":"-153 to 20C"},
    {"description": "First Record", "value":"2nd millennium BC"},
    {"description": "Recorded By", "value":"Egyptian astronomers"}
]

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': chrome_path}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #browser=init_browser()
    mars = {}
    mars['fact_dict'] = fact_dict
    ### News Title
    url="https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars['news'] = soup.find('div', class_ = 'content_title').text
   
    ### Paragraph Text
    paragraphs = soup.find_all('div', class_='rollover_description_inner')
    paragraph_text = paragraphs[0].text
    mars['paragraph'] = paragraph_text.replace('\n', '')

    ### URLs for featured Mars image
    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url3="https://www.jpl.nasa.gov"

    ###executable paths/browser
    executable_path = {'executable_path': chrome_path}
    browser = Browser('chrome', **executable_path, headless=False)

    ## Featured Mars Image
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    images = soup2.find_all('article', class_ = "carousel_item")
    mars['featured'] = url3 + "/spaceimages/images/wallpaper/PIA00063-1920x1200.jpg"

    ## Mars Weather
    url4 = "https://twitter.com/marswxreport?lang=en"
    response4 = requests.get(url4)
    soup4 = BeautifulSoup(response4.text, 'html.parser')
    mars_weather = soup4.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars['weather'] = mars_weather.replace("pic.twitter.com/0Eqt9nN21o", '')

    ## Mars Hemispheres
    url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    ## Mars Hemispheres
    response5 = requests.get(url5)
    soup5 = BeautifulSoup(response5.text, 'html.parser')
    cerberus = soup5.find('a', target= "_blank")["href"]

    response6 = requests.get(url6)
    soup6 = BeautifulSoup(response6.text, 'html.parser')
    schiaparelli = soup6.find('a', target= "_blank")["href"]

    response7 = requests.get(url7)
    soup7 = BeautifulSoup(response7.text, 'html.parser')
    syrtis_major = soup7.find('a', target= "_blank")["href"]

    response8 = requests.get(url8)
    soup8 = BeautifulSoup(response8.text, 'html.parser')
    valles_marineris = soup8.find('a', target= "_blank")["href"]

    ### Dictionary / List creation
    cerberus_dict = {
        "Cerberus" : cerberus
    }
    schiaparelli_dict = {
        "Schiaparelli" : schiaparelli
    }
    syrtis_major_dict = {
        "Syrtis Major" : syrtis_major
    }
    valles_marineris_dict = {
        "Valles Marineris" : valles_marineris
    }

    mars['hemispheres'] = [cerberus_dict, schiaparelli_dict, syrtis_major_dict, valles_marineris_dict]
    
    return mars
    
if __name__ == "__main__":
    scrape()



