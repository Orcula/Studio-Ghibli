# Studio-Ghibli
## What is this program?
This program is designed to allow users to explore movies created by Studio Ghibli.  
The users can interact with the minimal yet complete film franchise by filtering out personal preferences to supply a list of movies tailored to their liking.  
If the user desires they can access the official trailer from youtube launched straight from the program.  
Enjoy and I hope you discover some new movies in the process!

## How does it work?
The program starts by collecting all the data from an API website that is open to all. This data is in JSON format already and easy to work with.  
When the program is ran this data collection occurs and a list of movies is presented to the user. From here the user has two options. To immediately pick a movie to view its trailer or filter the movies.  
When filtering the movies a tree structure is utilized to navigate the options for a total of 8 different outcomes. Each yes or no answer will take the user down a different branch of the tree. The questions remain the same but the filter options stored will impact the filtered options.  
While traversing the tree the responses are saved in a list with True or False values. These values are used when filtering the complete movie list to remove elements that do no meet the user requested preferences. This will output a new list of movie titles for the user to select from.  
printed output that contains the title, rating, director, and rottentomatoes rating on each line shows the user how their preferences matched their responses. Lastly the user can opt to view the official trailer from this filtered list or exit.  
Upon exiting the user is asked if they wish to start over or exit.  