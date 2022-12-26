##################################################################  
# 
#  By: Sergio Ambelis Diaz      CS 421    Spring 2022
#  Description: Program which searches for movie in a database and 
#  outputs options to user such as total movies in list, total reviews.
#  Also updates tags and reviews in movie details
#

import sqlite3
import objecttier

##################################################################  
# 
#  Input/update a movie tag if there is a movie else 
#  print an error and exit
#
def inputTag(dbConn):
  tagline = input("\ntagline? ")
  movieId = input("movie id? ")
  movie_id = int(movieId)
  
  # Call from objectier a set tagline method
  tag = objecttier.set_tagline(dbConn, movie_id, tagline)

  if tag == 0: # Check if movie in list exists
    print("\nNo such movie...")
    menu(dbConn)
  else:  #  Check successful, new tag inserted
    print("\nTagline successfully set")
    menu(dbConn)

#################################################################  
# 
# Input a rating to database if movie exists regardless 
# of previous rating inputted or not, else print error. 
#
def inputRating(dbConn):
  newRates = input("\nEnter rating (0..10): ")
  newRate = int(newRates)

  if newRate < 0 or newRate > 10 : #  Check if n is less 0 or less
    print("Invalid rating...")
    menu(dbConn)

  newId = input("Enter movie id: ") 
  movie_id = int(newId)
  rate = objecttier.add_review(dbConn, movie_id, newRate)

  if rate == 0: # Check if movie in list exists
    print("\nNo such movie...")
    menu(dbConn)
  else:   #  Check successful, new rating inserted
    print("\nReview successfully inserted")
    menu(dbConn)

#################################################################  
# 
# Top N Movies: Gets a list of top N amount of movies based on rating
#
def top_N_Movies(dbConn):
  N = input("\nN? ")
  n = int(N)
  if n < 1: #  Check if n is less 0 or less
    print("Please enter a positive value for N...")
    menu(dbConn)
  min = input("min number of reviews? ")
  min_reviews = int(min)  #convert to int
  if min_reviews < 1:
    print("Please enter a positive value for min number of reviews...")
    menu(dbConn)    
  top = objecttier.get_top_N_movies(dbConn, n, min_reviews)

  if top == []:
    menu(dbConn)
  else:
    print()
    for x in top:
      print (x.Movie_ID, ":", x.Title, "("+ x.Release_Year +"),", "avg rating =", f"{x.Avg_Rating:.2f}" , f"({x.Num_Reviews:}", "reviews)"   )
    menu(dbConn)

##################################################################  
# 
# retrieves movie details based on Movie Id inputted 
#
def num_details(dbConn):
  movieId = input("\nEnter movie id: ")
  d = objecttier.get_movie_details(dbConn, movieId)

  if d is None:  # Check is movie exists if None is returned
    print("\nNo such movie...")
    menu(dbConn)
  else:  # Print all data below
    print()
    print(d.Movie_ID, ":", d.Title)
    print("  Release date:", d.Release_Date)
    print("  Runtime:", d.Runtime, "(mins)\n", " Orig language:", d.Original_Language)
    print("  Budget:", f"${d.Budget:,}", "(USD)")
    print("  Revenue:", f"${d.Revenue:,}", "(USD)")
    print("  Num reviews:", d.Num_Reviews)
    print("  Avg rating:", f"{d.Avg_Rating:.2f} (0..10)")
    print("  Genres: ", end = "")
    for x in d.Genres:
      print(x + ", ", end = "" )
    print("\n  Production companies: ", end = "")
    for x in d.Production_Companies:
      print(x + ", ", end = "" )      
    print("\n  Tagline:", d.Tagline)
    menu(dbConn)      

##################################################################  
# 
# retrieve number of movies based on name inputted
#
def num_movies(dbConn):
  name = input("\nEnter movie name (wildcards _ and % supported):")
  getMovies = objecttier.get_movies(dbConn, name)
  print("\n# of movies found:", len(getMovies))
  
  if getMovies == []:  # None
    menu(dbConn)
  else:
    if (len(getMovies) > 100): # If user inputs greater than 100 movies to display, tell to trim
      print("\nThere are too many movies to display, please narrow your search and try again...")
      menu(dbConn)
    else:
      print()
      for x in getMovies:
        print(x.Movie_ID, ":", x.Title, "(" + x.Release_Year + ")")
      menu(dbConn)


##################################################################  
# 
#  Creates a stats window to show total movies 
#  and total number of reviews
#
def stats(dbConn):
  numMovies = objecttier.num_movies(dbConn)
  print("\nGeneral stats:\n  # of movies:",  f"{numMovies:,}")
  numReviews = objecttier.num_reviews(dbConn)
  print("  # of reviews:",  f"{numReviews:,}")


##################################################################  
# 
#  Creates a menu for the user to interact with
#
def menu(dbConn):
  print()
  cmd = input("Please enter a command (1-5, x to exit): ")
  
  while cmd != "x":
    if cmd == "1":
        num_movies(dbConn)
    elif cmd == "2":
        num_details(dbConn)
    elif cmd == "3":
        top_N_Movies(dbConn)       
    elif cmd == "4":
        inputRating(dbConn)     
    elif cmd == "5":
        inputTag(dbConn)          
    else:
        print("**Error, unknown command, try again...")
        print()
        cmd = input("Please enter a command (1-5, x to exit): ")
  exit(0)
  
##################################################################  
#
# main
#
print("** Welcome to the MovieLens app **")

dbConn = sqlite3.connect('MovieLens.db')
stats(dbConn)
menu(dbConn)



  

# done





