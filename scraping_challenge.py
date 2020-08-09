# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

# Import Pandas
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)
    img_url_1, img_url_2, img_url_3, img_url_4, title_1, title_2, title_3, title_4 = hemis(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "img_url_1": img_url_1,
        "img_url_2": img_url_2,
        "img_url_3": img_url_3,
        "img_url_4": img_url_4,
        "title_1": title_1,
        "title_2": title_2,
        "title_3": title_3,
        "title_4": title_4
    }

    browser.quit()
    return data

def hemis(browser):
    try:
        img_url_1 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
        browser.visit(img_url_1)
    
        # Scrape page into Soup
        html = browser.html
        soup_1 = soup(html, "html.parser")

        img_url_1 = soup_1.find_all('img')[7]["src"]
        title_1 = soup_1.find('h2', class_='title').get_text()


        img_url_2 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
        browser.visit(img_url_2)
        html = browser.html
        soup_2 = soup(html, "html.parser")

        img_url_2 = soup_2.find_all('img')[7]['src']
        title_2 = soup_2.find('h2', class_='title').get_text()


        img_url_3 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
        browser.visit(img_url_3)
        html = browser.html
        soup_3 = soup(html, "html.parser")

        img_url_3 = soup_3.find_all('img')[7]['src']
        title_3 = soup_3.find('h2', class_='title').get_text()


        img_url_4 = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
        browser.visit(img_url_4)
        html = browser.html
        soup_4 = soup(html, "html.parser")

        img_url_4 = soup_4.find_all('img')[7]['src']
        title_4 = soup_4.find('h2', class_='title').get_text()
    except BaseException:
        return None

    return img_url_1, img_url_2, img_url_3, img_url_4, title_1, title_2, title_3, title_4

def mars_news(browser):

    # Visit the Mars NASA news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# Featured Images

def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
       
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

def mars_facts():

    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())