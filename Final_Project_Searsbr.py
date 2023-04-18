#########################################
##### Name: Brian Sears             #####
##### Uniqname: Searsbr             #####
#########################################

import copy
import json
import webbrowser
import requests
import pprint 
from urllib.parse import quote, urlencode, urljoin
pp = pprint.PrettyPrinter()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

cache = {}

filterTree = \
    ("Do you want family friendly movies?",
        ("Do you want Miyazaki films?",
            ('Do you want want movies with ratings greater than 90?', None, None),
            ('Do you want want movies with ratings greater than 90?', None, None)),
        ("Do you want Miyazaki films?",
            ('Do you want want movies with ratings greater than 90?', None, None),
            ('Do you want want movies with ratings greater than 90?', None, None)))

CACHE_FILEPATH = './stu-cache.json'
API_FILEPATH = "https://studio-ghibli-films-api.herokuapp.com/api"

def create_cache_key(url, params=None):
    """Returns a lowercase string key comprising the passed in < url >, and, if < params >
    is not None, the "?" separator, and any URL encoded querystring fields and values.
    Passes to the function < urllib.parse.urljoin > the optional < quote_via=quote >
    argument to override the default behavior and encode spaces with '%20' rather
    than "+".

    Parameters:
        url (str): string representing a Uniform Resource Locator (URL).
        params (dict): one or more key-value pairs representing querystring fields and values.

    Returns:
        str: Lowercase "key" comprising the URL and accompanying querystring fields and values.
    """

    if params:
        return urljoin(url, f"?{urlencode(params, quote_via=quote)}").lower() 
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

def get_api_resource(url, params=None, timeout=10):    
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

def movie_info(data):
    """Returns a new dictionary representation from the passed in data.

    Key order:
        title
        rating
        director
        reviews

    Parameters:
        data (dict): source data.

    Returns:
        dict: new dictionary.
    """
    return {
        'title': data.get('title'),
        # 'genre': data.get('genre'),
        'rating': data.get('rating'),
        'director': data.get('director'),
        # 'runtimeMinutes': data.get('runtimeMinutes'),
        'reviews': data.get('reviews'),
        # 'release': data.get('release'),
        # 'screenwriters': data.get('screenwriters'),
    }

def get_movie_data(movie_data, movie_name): 
    """Attempts to retrieve a web sourced dictionary representation of a
    movie from the movie list using the passed in filter value. The function performs
    a case-insensitive comparison of each nested dictionary's "name" value against the
    passed in < filter > value. If a match is obtained the dictionary is returned to the
    caller; otherwise None is returned.

    Parameters:
        movie_data (list): web data stored in a list of nested dictionaries.
        movie_name (str): name value used to match on a dictionary's "name" value.

    Returns
        dict|None: web-sourced data dictionary if match on the filter is obtained;
                     otherwise returns None.
    """
    for k,v in movie_data.items():
        if k == movie_name.lower():
            return v
    return None

def get_movie_trailer(movie_name):
    """Takes the movie name and performs a google search for the official trailer.
       The page elements are inspected to find the href that contains youtube and
       returns the url attached to the youtube trailer

    Parameters:
        movie_name: string representation of a movie title

    Returns:
        href: The web url of the specific youtube link that contains the trailer
    """ 
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(f"https://www.google.com/search?q={movie_name}+official+trailer")
    links = driver.find_elements(By.TAG_NAME, 'a')
    Trailer = False

    while Trailer == False:
        for link in links:
            href = link.get_attribute('href')
            if href is not None:
                if "youtube" in href:
                    Trailer = True
                    break
    
    driver.quit()
    return href

def yes_no():
    """Tests if a user input is a valid response to a yes or no question.
    Variations of yes or no are acceptable and case insensitive. 
    loops until an appropriate user input is given

    Parameters:
        None

    Returns:
        True: For any yes answers
        False: For any no answers
    """ 

    yesanswers = ("yes", "ya", "yup", "yeah")
    noanswers = ("no", "nah", "nope")
    loop = None
    while loop == None:
        print("Yes or No?")
        answer = input()
        if answer.lower() in yesanswers:
            loop = True
        elif answer.lower() in noanswers:
            loop =  False
        else:
            print("Please answer with the follow options")
            print(f"For Yes responses use {yesanswers}")
            print(f"For No responses use {noanswers}")
    return loop #Returns a True for correct answer and False for incorrect

def pick_trailer(movie_list):
    """Takes a list of movie titles and asks the user to pick a movie selection based on its numerical value
        within the list. Option to exit is presented if the user doesn't wish to make a movie selection.

    Parameters:
        movie_list (list): a list of movie titles

    Returns:
        None
    """

    while True:
        prompt = "Enter the number of the film you wish to watch a trailer for. (type 'exit' to quit): "
        input_continue = input(prompt)
        if input_continue.isnumeric():
            if int(input_continue) < 1 or int(input_continue) > index:
                print("number is not valid. Please enter a number between 1 and " + str(index))
                continue
        
            elif int(input_continue) <= len(movie_list):
                real_index = int(input_continue) - 1
                webbrowser.open(get_movie_trailer(movie_list[real_index]))

        elif input_continue == "exit":
                break 

### The below function was not needed for the project. I built it and like how it works but it didn't serve a purpose with the tree format of the project.
# def filter_options(filter): 
#     movies = get_api_resource(API_FILEPATH)
#     movie_list = []
#     filtered_list = []
#     index = 0  

#     for movie in movies:
#         movie_list.append(movie)

#     for movie in movie_list:    
#         info = (movie_info(get_movie_data(movies, movie)))
#         split = info[filter].split('/')
#         for items in split:
#             if items in filtered_list:
#                 continue
#             else:
#                 filtered_list.append(items)

#     for filter in filtered_list:
#         index = index + 1
#         print(str(index) + " " + filter)

#     while True:
#         prompt = "Enter the number you want to select"
#         input_continue = input(prompt)
#         if input_continue.isnumeric():
#             if int(input_continue) < 1 or int(input_continue) > index:
#                 print("number is not valid. Please enter a number between 1 and " + str(index))
#                 continue
        
#             elif int(input_continue) <= len(filtered_list):
#                 real_index = int(input_continue) - 1
#         return filtered_list[real_index]

def isanswer(tree):  
    """Determines if the parameter is a internal node or leaf of a tree. 

    Parameters: 
        tree: the working node of the tree

    Returns:
        True: If the parameter is a leaf
    """

    if not tree[1] and not tree[2]:
        return True

def giveanswer(prompt):
    """Provides the user with a question in which a yes or no response is required.
    the question asked is dependent on if the current tree node is internal or a leaf.
    The function isanswer is used to determine the node. 
    The function yes_no is used to determine user input.

    Parameters:
        prompt: Tuple element that provides the user a question to answer

    Returns:
        yes_no():
            True: For any yes answers
            False: For any no answers
    """

    if isanswer(prompt) == True:
        print(f"\nIt is {prompt[0]}\n")
    else:
        print(f"\n{prompt[0]}\n")
    return yes_no()

def simplePlay(tree):
    """Takes a prebuilt tree and allows the user to filter movie elements

    Parameters:
        tree: A preconstructed tree saved within the program

    Returns:
        None
    """

    if isanswer(tree) == True:
        if giveanswer(tree) == True:
            filterlist.append(True)
            return tree
        else:
            filterlist.append(False)
            return tree
    else:
        if giveanswer(tree) == True:
            returned_tree = simplePlay(tree[1])
            filterlist.append(True)
            return (tree[0], returned_tree, tree[2])
        else:
            returned_tree = simplePlay(tree[2])
            filterlist.append(False)
            return (tree[0], tree[1], returned_tree)

def movie_filters(movie_list, filterlist):
    """Takes a movie list and filters the titles based on the filterlist elements. 
       The initial new_list is appended with all titles meeting the criteria and
       then movies are removed if they do not meet criteria. Returns a new list of
       movies that meet the user selected filters. 

    Parameters:
        movie_list (list): List of movie titles
        filterlist (list): List containing True or False elements

    Returns:
        new_list (list): new list of movies 
    """
    new_list = []
    for movie in movie_list:
        for i in range(len(filterlist)):
            info = (movie_info(get_movie_data(movies, movie)))

            if i == 0 and filterlist[i] == True:
                if info['rating'] == "G" or info['rating'] == "PG":
                    new_list.append(movie)
                    continue

            elif i == 0 and filterlist[i] == False:
                if info['rating'] != "G" and info['rating'] != "PG":
                    new_list.append(movie)
                    continue

            elif i == 1 and filterlist[i] == True:
                if info['director'] != "Hayao Miyazaki":
                    try:
                        new_list.remove(movie)
                        continue
                    except:
                        continue
            elif i == 1 and filterlist[i] == False:
                if info['director'] == "Hayao Miyazaki":
                    try:
                        new_list.remove(movie)
                        continue
                    except:
                        continue

            elif i == 2 and filterlist[i] == True:
                split = info['reviews']['rottenTomatoes'].split('%')
                try:
                    split = int(split[0])
                    if split < 90:
                        new_list.remove(movie)
                        continue
                except:
                    continue
                
            elif i == 2 and filterlist[i] == False:
                split = info['reviews']['rottenTomatoes'].split('%')
                try:
                    split = int(split[0])
                    if split >= 90:
                        new_list.remove(movie)
                        continue
                except:
                    continue
    return new_list

def main():
    """This program will provide the user a list of Studio Ghibli movies
    From this the user can filter the movie options to fit their viewing preferences
    The filtered options will display the title, rating, director, and review rating.
    Lastly the user has the option to watch the official trailer launched straight from the program.
    """

print("\nHello and welcome to the Studio Ghibli Collection Database!")
print("This program will help you learn more about these wonderful movies and find films best suited for you")
print("Below is the full list of movies that Studio Ghibli has created\n")

replay = True

while replay == True:

    movies = get_api_resource(API_FILEPATH)
    movie_list = []
    filterlist = []
    filtered_movies = []
    index = 0  
   
    for movie in movies:
        movie_list.append(movie)

    for movie in movie_list:
        index = index + 1
        print(str(index) + " " + movie)

    print("Do you want to filter your selection options?\n")

    response = yes_no()
    if response == False:
        pick_trailer(movie_list)

    else:   
        
        simplePlay(filterTree)
        filtered_movies = movie_filters(movie_list, list(reversed(filterlist)))
        index = 0
        print("")
   
        for flick in filtered_movies:
            info = (movie_info(get_movie_data(movies, flick)))
            index = index + 1
            print(str(index) + " " + flick + " - " + "Rated: " + info["rating"] + ", Director: " + info['director'] + ", Review Rating: " + info['reviews']['rottenTomatoes'])
        print("")
        pick_trailer(filtered_movies)

    print("\nDo you want to start over?\n")
    repeat = yes_no()
    if repeat == True:
        continue
    else:
        repeat = False
        print("Bye")
        break


write_json(CACHE_FILEPATH, cache)

if __name__ == '__main__':
    main()