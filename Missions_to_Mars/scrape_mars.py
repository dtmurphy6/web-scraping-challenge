import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #NASA Mars News
    #create and executable path and browser to scrape
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #link the URL for scraping
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #create an html object
    html = browser.html
    #Create the BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    #show results for title
    results = soup.find('div', class_='content_title')
    news_title = results.text

    #show results for the paragraph body
    results = soup.find('div', class_="article_teaser_body")
    news_p = results.text

    # JPL Mars Space Images--Featured Images

    #link the URL for scraping
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #create an html object
    html = browser.html
    #Create the BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    #show results for the image and grab the url
    results = soup.find('img', class_="headerimage")
    featured_image_url = f"{url}{results['src']}"

    # Mars Facts

    #now we will use Pandas to scrape the table containing facts about Mars

    #add new url
    url = 'https://galaxyfacts-mars.com/'

    #use pandas to create a dataframe
    df = pd.read_html(url)

    #create an indexed table of Mars facts
    mars_table_df = df[1] 
    mars_table_df.columns = ["Description", "Info"]

    #set description as index
    mars_table_df.set_index('Description', inplace=True)
   
    #convert the above table to html string
    mars_html_table = mars_table_df.to_html()

    #wherever there is a line break, replace that with nothing, to get one continuous html string
    mars_html_table = mars_html_table.replace("\n", "")

    # Mars Hemispheres

    #link the URL for scraping
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #create an html object
    html = browser.html
    #Create the BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    #collect headings assiciated with the images before grabbing images, so we know which images we are looking for. 
    mars_headers=[]
    titles = soup.find_all('h3')
    
    #get rid of the header "back" because we don't need it
    titles = titles[:-1]

    #with a loop, get rid of the html tags to leave us with just the header text
    for t in titles:
        mars_headers.append(t.text)

    #create an empty list to put image urls in, 
        #then use splinter to automate locating the images, click into each image, then locate the source link
    mars_images=[]
    count=0
    for i in mars_headers:
        browser.find_by_css('img.thumb')[count].click()
        mars_images.append(browser.find_by_css('img.wide-image')['src'])
        browser.back()
        #increase the counter by one for each image
        count = count+1

    #now put the four titles and images together
    mars_titles_images=[]
    count=0

    for i in mars_images:
        mars_titles_images.append({"title":mars_headers[count], "img_url":mars_images[count]})
        count = count+1

    mars_data = {"newsTitle":news_title, "newsParagraph":news_p, "image_url":featured_image_url, "marsTable":mars_html_table, "hemisphereImages": mars_titles_images}

    browser.quit()

    return mars_data
    


