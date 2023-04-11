#########################################
##### Name: Brian Sears             #####
##### Uniqname: Searsbr             #####
#########################################

import copy
import csv
import json
import webbrowser
import requests
import pprint 
from urllib.parse import quote, urlencode, urljoin
pp = pprint.PrettyPrinter()
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_binary

cache = {}

CACHE_FILEPATH = './stu-cache.json'
SWAPI_FILEPATH = "https://studio-ghibli-films-api.herokuapp.com/api"

def create_cache_key(url, params=None):
    """Returns a lowercase string key comprising the passed in < url >, and, if < params >
    is not None, the "?" separator, and any URL encoded querystring fields and values.
    Passes to the function < urllib.parse.urljoin > the optional < quote_via=quote >
    argument to override the default behavior and encode spaces with '%20' rather
    than "+".

    Example:
       url = https://swapi.py4e.com/api/people/
       params = {'search': 'Anakin Skywalker'}
       returns 'https://swapi.py4e.com/api/people/?search=anakin%20skywalker'

    Parameters:
        url (str): string representing a Uniform Resource Locator (URL).
        params (dict): one or more key-value pairs representing querystring fields and values.

    Returns:
        str: Lowercase "key" comprising the URL and accompanying querystring fields and values.
    """

    if params:
        return urljoin(url, f"?{urlencode(params, quote_via=quote)}").lower() # space replaced with '%20'
    else:
        return url.lower()

def get_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the entity.

    Parameters:
        url (str): a uniform resource locator that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds.

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file.
        data (dict)/(list): the data to be encoded as JSON and written to the file.
        encoding (str): name of encoding used to encode the file.
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON.

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def get_swapi_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more SWAPI entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the SWAPI entity.

    Parameters:
        url (str): a uniform resource locator that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds.

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    # WARN: deep copying required to guard against mutating cache objects
    key = create_cache_key(url, params)
    if key in cache.keys():
        return copy.deepcopy(cache[key]) # recursive copy of objects
    else:
        resource = get_resource(url, params, timeout)
        cache[key] = copy.deepcopy(resource) # recursive copy of objects
        return resource

def movieinfo(): #Write a function that produces specific elements of movie to display Is this needed?
    pass

def moviefilters(): #Displays list of potential filter topics (genre, rating, director, screenwriter) Is this needed?
    pass

def setfilter(): #recusrive method that the user inputs how to further filter the results
    pass

def directors(): #Produces list of unique directors
    pass

def genres():
    pass

def rating():
    pass








########################################################################################
########################################################################################

movies = get_swapi_resource(SWAPI_FILEPATH)
movie_list = []
index = 0  

for key in movies:
    movie_list.append(key)

for movie in movie_list:
    index = index + 1
    print(str(index) + " " + movie)





#### Youtube TESTING ###
# PATH = "/USERS/briansears/Desktop/chromedriver"
# driver = webdriver.Chrome(PATH)
# driver.get("https://www.youtube.com/results?search_query=princess+monokoke+official+trailer")

# link = driver.find_element_by_link_test("Princess Monokoke - Official Trailer")
# link.click()

#trailerurl = "https://www.youtube.com/results?search_query=princess+monokoke+official+trailer"

# page = urlopen(trailerurl)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# print(html)
#Below works as expected
# select_url = "https://www.youtube.com/results?search_query=princess+monokoke+official+trailer"
# print("Launching")
# print(select_url)
# print("in web browser...")
# print()
# webbrowser.open(select_url)



# title
# genre
# rating
# release
# director
# music
# runtimeMinutes  
# reviews
# screenwriters              

#### Could ask users to create a tree of filters using the 20 question game on how to build a tree. 
# Do you want to filter based on director? If yes present list of directors and select one
# If no it should branch off a no and ask next filter question.
# Do you want to filter by genre? If yes present list and repeat. This will create a tree which then will go thru the list of movies to find those which contain all filters
####



write_json(CACHE_FILEPATH, cache)