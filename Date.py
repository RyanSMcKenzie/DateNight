# Web Scraping Yelp
# Import requests, BeautifulSoup, and random library
import requests
from bs4 import BeautifulSoup
from random import randint,choice

# Scrape Yelp function
def ScrapeYelp(loc):
    base_url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc='
    page = 0 
    #print(yelp_r.status_code)
    #yelp_html = yelp_r.text
    #print(yelp_html)
    #print(yelp_soup.prettify())

    # Randomly select a page to read from, request url
    restaurants = []
    page = randint(0,4) * 30
    url = base_url + loc + '&start=' + str(page)
    yelp_r = requests.get(url)
    # Parse html, find restaurant tabs, business name and address within each tab
    yelp_soup = BeautifulSoup(yelp_r.text, 'html.parser')
    businessinfo = yelp_soup.findAll('div',{'class':'largerScrollablePhotos__373c0__3FEIJ'})
    for i in range(len(businessinfo)):
        busname = businessinfo[i].findAll('div',{'class':"businessName__373c0__1fTgn"})
        address = businessinfo[i].findAll('address',{'class':'lemon--address__373c0__2sPac'})
        # For results with a leading number, remove number (it was annoying)
        try:
            busname = busname[0].text.split('.')
            busname.remove(busname[0])
            busname = ''.join(busname)
            restaurants.append((busname,address[0].text))
        except:
            restaurants.append((busname,'no address'))
    restaurants = list(set(restaurants))

    return restaurants

# Define Scrape AMC function
def ScrapeAMC():
    # Get url for movie section, parse, and find movie grids
    url = 'https://www.amctheatres.com/movies'
    AMC_r = requests.get(url)
    AMC_soup = BeautifulSoup(AMC_r.text, 'html.parser')
    movies = AMC_soup.findAll('div',{'class':'MoviePostersGrid-text'})
    movie_list = []
    # Find name of each movie from within each grid
    for movie in movies:
        Name = movie.findAll('h3')
        movie_list.append(Name[0].text)
    return movie_list

# Define main function
def Main():
    # Input location for yelp search
    loc = input('Where are you going on your date?: ')
    loc = loc.replace(' ','+')
    print('Your dinner and movie are being generated...')
    restaurants = ScrapeYelp(loc)
    movies = ScrapeAMC()
    # Randomly select dinner and movie
    food = choice(restaurants)
    movie = choice(movies)
    print('Dinner:', food[0], 'at', food[1])
    print('Movie: ',movie)

Main()
