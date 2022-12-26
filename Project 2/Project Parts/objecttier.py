#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, movieId, title, year):
    self._Movie_ID = movieId
    self._Title = title
    self._Release_Year = year

  @property
  def Movie_ID(self):
    return self._Movie_ID
  
  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, movieId, title, year, numReviews, avgRating):
    self._Movie_ID = movieId
    self._Title = title
    self._Release_Year = year
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating

  @property
  def Movie_ID(self):
    return self._Movie_ID
  
  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, movieId, title, dates, runtime, lang, budget, revenue, numReviews, avgRating ,tag):
    self._Movie_ID = movieId
    self._Title = title
    self._Release_Date = dates
    self._Runtime = runtime 
    self._Original_Language = lang
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = numReviews
    self._Avg_Rating = avgRating
    self._Tagline = tag
    self._Genres = []
    self._Production_Companies = []

  @property
  def Movie_ID(self):
    return self._Movie_ID
  
  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating    

  @property
  def Tagline(self):
    return self._Tagline  
 
  @property
  def Genres(self):
    return self._Genres  

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  sql = "Select count(*) from Movies;"

  row = datatier.select_one_row(dbConn, sql)   
  if row is None:
    return -1
  else:    
    return row[0]


  


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  sql = "Select count(*) from Ratings;"
 

  row = datatier.select_one_row(dbConn, sql)      
  if row is None:
    return -1
  else:    
    return row[0]



##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """Select Movie_Id, Title, strftime('%Y', Release_Date) 
    From Movies 
    Where Title like ?
    Order by Title asc;"""

  result = datatier.select_n_rows(dbConn, sql, [pattern])  
  array1 = []
    # print("**Internal error: retrieve_stations")
  if result is None:
    return []
  else:
    for x in result:
      
      s = Movie (x[0], x[1], x[2]);
      array1.append(s)
  return array1




##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  qmovies = """Select Movies.Movie_Id, Movies.Title, date(Release_Date), Movies.Runtime, 
Original_Language, Budget, Revenue
from Movies
Where Movies.Movie_Id = ?;"""

  qratings = """Select count(Rating)
from Ratings left join Movies on (Movies.Movie_Id = Ratings.Movie_Id)
Where Movies.Movie_Id = ?;"""

  qratings2 = """Select avg(Rating)
from Ratings left join Movies on (Movies.Movie_Id = Ratings.Movie_Id)
Where Movies.Movie_Id = ?;"""

  qgenre = """Select Genre_Name
from Genres left join  Movie_Genres  on (Genres.Genre_ID = Movie_Genres.Genre_ID)
left join Movies on (Movies.Movie_ID = Movie_Genres.Movie_ID)
Where Movies.Movie_Id = ?
order by Genre_Name asc;"""

  qcompany = """Select Company_Name
from Companies left join Movie_Production_Companies on 
(Companies.Company_ID = Movie_Production_Companies.Company_ID)
left join Movies on (Movie_Production_Companies.Movie_ID = Movies.Movie_ID)
Where Movies.Movie_Id = ?
order by Companies.Company_Name asc;"""

  qtag = """Select Tagline
from Movie_Taglines left join Movies
on (Movies.Movie_ID = Movie_Taglines.Movie_ID)
Where Movies.Movie_Id = ?;"""


  movie = datatier.select_one_row(dbConn, qmovies, [movie_id])
  if movie is None or movie == ():
    return None
  
  rating = datatier.select_one_row(dbConn, qratings, [movie_id]) 
  avgrate = datatier.select_one_row(dbConn, qratings2, [movie_id]) 
  if rating is None or rating == () or rating[0] == 0 :
    numRating = 0
    numRating2 = 0
  else:
    numRating = rating[0]
    numRating2 = avgrate[0]
  
  tag = datatier.select_one_row(dbConn, qtag, [movie_id])     
  if tag is None or tag == ():
    tagline = ""
  else:
    tagline = tag[0]


  # for x in movie:
  s = MovieDetails(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], numRating, numRating2, tagline)  
    # array1.append(s)

    
  genre = datatier.select_n_rows(dbConn, qgenre, [movie_id]) 
  if genre is None or len(genre) == 0:
    pass
    # array1.append(s)
  else:
    for i in genre:
      s.Genres.append(i[0])
      # array1.append(s)

  
  company = datatier.select_n_rows(dbConn, qcompany, [movie_id])  
  if company is None or len(company) == 0:
    pass
    # array1.append(s)
  else:
    for x in company:
      s.Production_Companies.append(x[0])
      # array1.append(s)

  return s



         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  if N < 1:
    return []

  sql = """Select Movies.Movie_Id, Movies.Title, strftime('%Y', Release_Date), AVG(Rating), count(Rating)
from Movies join Ratings on (Movies.Movie_Id = Ratings.Movie_Id)
group by Movies.Movie_Id
having count(Rating) >= ?
order by AVG(Rating) desc
limit ?;"""

  rate = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  #  movieId, title, year, numReviews, avgRating):

  if rate is None:
    return []
  array1 = []
  for x in rate:
      s = MovieRating (x[0], x[1], x[2], x[4], x[3])
      array1.append(s)
  return array1


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  sql = """INSERT INTO Ratings (Movie_Id, Rating)
  VALUES (?, ?);
  """

  sqlId = """Select Movie_Id
  from Movies
  where Movie_Id = ?"""

  id = datatier.select_one_row(dbConn, sqlId, [movie_id])



  if id is None or id == ():
    return 0
  if rating > 10 or rating < 0:
    return 0
  s = datatier.perform_action(dbConn, sql, [ movie_id, rating])
  return s

##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  sqlM = """Select Movie_Id
  from Movies
  Where Movie_Id = ?"""

  movieCheck = datatier.select_one_row(dbConn, sqlM, [movie_id])
  if movieCheck is None or movieCheck == ():  # Check if movie exists
    return 0
    
  tag = """Select Tagline
  from Movie_Taglines
  Where Movie_Id = ?"""

  newTag = """INSERT INTO Movie_Taglines (Movie_Id, Tagline)
  VALUES (?, ?);"""

  update = "UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_Id = ?;"
  
  tagCheck = datatier.select_one_row(dbConn, tag, [movie_id]) 
 
  # print(tagCheck)
  
  if tagCheck is None or tagCheck == (): # Check if tag is empty
    s = datatier.perform_action(dbConn, newTag, [movie_id, tagline])
  else: # Update my tag if it does exist
    s = datatier.perform_action(dbConn, update, [tagline, movie_id])
  return s
      

  

  # Check if movie exists
  # Check if there is no tagline
  # Check if there already is a tagline then update it
   
