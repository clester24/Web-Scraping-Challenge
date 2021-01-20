from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser


def init_browser():
     executable_path = {'executable_path': '/Users/chase/Downloads/chromedriver.exe'}
     browser = Browser('chrome', **executable_path, headless=False)
     return browser

mars_data= {}
def mars_news_scrape():
     browser = init_browser()
     Nasa_url = 'https://mars.nasa.gov/news/'
     browser.visit(Nasa_url)
     html = browser.html
     soup = bs(html, 'html.parser')

     # get title
     article = soup.find('div',class_='list_text')
     news_title = article.find('div', class_='content_title').text
     print(f"title {news_title}")
     mars_data['news_title'] = news_title
     # Paragraph text
     news_paragraph = article.find('div',class_='article_teaser_body').text
     mars_data['news_paragraph'] = news_paragraph
     print(f"paragraph {news_paragraph}")

     return mars_data
     
def img_scrape():
     browser = init_browser()
     url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
     browser.visit(url)
     cards = browser.find_by_css('div[class="SearchResultCard"]')
     cards[0].click()

     return mars_data

def mars_facts():
     browser = init_browser()
     mars_facts = 'https://space-facts.com/mars/'
     browser.visit(mars_facts)
     tables_df = ((pd.read_html(mars_facts))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
     tables_df.to_html('table.html')
     browser.quit()
     return mars_data


def mars_hemispheres():
     browser = init_browser()
     hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
     short_url = "https://astrogeology.usgs.gov"

     browser.visit(hemisphere_url)
     html = browser.html
     soup = bs(html, 'html.parser')
     main_url = soup.find_all('div', class_='item')
     
     hemisphere_img_urls=[]      
     for x in main_url:
          title = x.find('h3').text
          url = x.find('a')['href']
          hem_img_url= short_url + url
          browser.visit(hem_img_url)
          html = browser.html
          soup = bs(html, 'html.parser')
          hemisphere_img = soup.find('div',class_='downloads')
          hemisphere_img_url = hemisphere_img.find('a')['href']
          
          print(hemisphere_img_url)
          img_data=dict({'title':title, 'img_url':hemisphere_img_url})
          hemisphere_img_urls.append(img_data)
     mars_data['hemisphere_img_urls']=hemisphere_img_urls
     return mars_data