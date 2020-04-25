from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def scrape():
    mars_data = {}
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    news_title = results[0].find('div', class_="content_title").text.strip()
    news_p = results[0].find('div', class_="rollover_description_inner").text.strip()
    mars_data["news_title"] = news_title
    mars_data["news_text"] = news_p

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_text('jpg')
    mars_data["featured_image_url"] = browser.url

    weather_url = 'https://twitter.com/marswxreport'
    browser.visit(weather_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_data["mars_weather"] = results[0].text

    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    html_table = df.to_html()
    mars_data["mars_table"] = html_table.replace('\n', '')

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    links = []

    for item in items:
        link = item.find('h3').text
        links.append(link)

    hemisphere_image_urls = []

    for link in links:
        browser.click_link_by_partial_text(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title":link[:-9], "img_url":img_url})
        browser.visit(hemisphere_url)
        
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return(mars_data)


