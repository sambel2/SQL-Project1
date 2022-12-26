###########################################################  
#
# Program that grabs from database and presents
# the data as Riders, Stops, Lines, Stations, Stop Details
# as a total, percent, color or location based on user input 
# By: Sergio Ambelis Diaz     CS341     Spring 2022
# Project 1: Analyzing CTA2 L data in Python
#

import sqlite3
import matplotlib.pyplot as figure

###########################################################  
#
#  plotLineColor -> command 9
#
#  Plot the line colors on a picture map for all to see
#  displaying station names on map
# 
def plotLineColor(StationColor, color):
  plot = input("\nPlot? (y/n) ")
  if (plot == "y"):
    x = []
    y = []
    for r in StationColor:
      x.append(r[2]) 
      y.append(r[1]) 
    image = figure.imread("chicago.png")
    # area covered by map
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)
    figure.title(color + " line")
    if (color.lower() == "purple-express"):
      color = "Purple" # color = "800080"
    figure.plot(x, y, "o", c = color)
    # annotate each(x,y) coordinate with its station name
    for row in StationColor:
      figure.annotate(row[0], (row[2],row[1]))
    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])
    figure.show() 
  else:
    return;   

###########################################################  
#
# PlotChart -> command 9
#
# Gets the plot for command to output Station name, latitude 
# and longitude for user. Also plot a dotted map if user wants
# 
def LineColor(dbCursor):
  color = input("\nEnter a line color (e.g. Red or Yellow): ")
  sql = "Select Stations.Station_Name, Stops.Latitude , Stops.Longitude \
  From Stations join Stops On (Stations.Station_ID = Stops.Station_ID)\
  join StopDetails On (Stops.Stop_ID = StopDetails.Stop_ID)\
  join Lines On (StopDetails.Line_ID = Lines.Line_ID)\
  where Color like ? \
  group by Stations.Station_Name \
  order by Stations.Station_Name asc;"
  dbCursor.execute(sql,[color])
  StationColor = dbCursor.fetchall()
  if(len(StationColor) > 0):
    for x in StationColor:
      print (x[0], ": (" + str(x[1]) + ",", str(x[2]) + ')')
    plotLineColor(StationColor, color)
  else:
    print("**No such line...")
  
###########################################################  
#
# PlotChart -> command 8
#
# Gets the plot for commmand 
# 
#
def plotChart(station1Yr, riderDays, station2Yr, riderDays2):
  plot = input("\nPlot? (y/n) ")
  if(plot == "y"):
    figure.close("all")
    # Create four empty vectors
    x =[]
    y =[]
    x1 = []
    y2 = []
    count = 1
    count2 = 1
    # Create data1 and data2 for plot
    for row in riderDays:
      x.append(count) 
      y.append(row[1]) 
      count += 1   
    for i in riderDays2:
      x1.append(count2) 
      y2.append(i[1]) 
      count2 += 1   
    figure.xlabel("day")
    figure.ylabel("number of riders")
    figure.title("riders each day of 2020")
    figure.plot(x, y, label = str
    (station1Yr[0][1]))
    figure.plot(x1, y2, label  = str(station2Yr[0][1]))
    figure.legend()
    figure.show()

###########################################################  
#
# ExtendStationsByYear -> command 8
#
# Goes through the query and finds if station is multiple or no 
# station found
#
def ExtendStationsByYear(dbCursor, sql1, sql2, year):
   # Fetch station 1  
  station1 = input("\nEnter station 1 (wildcards _ and %): ")
  dbCursor.execute(sql1, [year, station1])
  station1Yr = dbCursor.fetchall()
  dbCursor.execute(sql2, [year, station1])
  riderDays = dbCursor.fetchall()  
  if(len(station1Yr) > 1 ):
    print("**Multiple stations found...")
    return; 
  if(len(station1Yr) == 0):
      print("**No station found...")
      return;      
   # Fetch station 2
  station2 = input("\nEnter station 2 (wildcards _ and %): ")    
  dbCursor.execute(sql1, [year, station2])
  station2Yr = dbCursor.fetchall()
  dbCursor.execute(sql2, [year, station2])
  riderDays2 = dbCursor.fetchall() 
  if(len(station2Yr) > 1 ):
    print("**Multiple stations found...")
    return; 
  if(len(station2Yr) == 0):
      print("**No station found...")
      return;
  # Station 1 loop for all dates and  riders
  for x in station1Yr:
    print("Station 1:",x[0], x[1])  
  for x in riderDays[0:5]:
    print(x[0], x[1])
  for x in riderDays[-5:]:
    print(x[0], x[1])
  # Station 2 loop for all dates and  riders
  for i in station2Yr:
    print("Station 2:",i[0], i[1])
  for i in riderDays2[0:5]:
    print(i[0], i[1])
  for i in riderDays2 [-5:]:
    print(i[0], i[1])
  plotChart(station1Yr, riderDays, station2Yr, riderDays2)  

###########################################################  
#
# StationsByYear -> command 8
#
# Outputs station Id and station name for two diff stations
# Give each number of riders based on first and last 5 days of year
#
def StationsByYear(dbCursor):
  year = input("\nYear to compare against? ")
  # Get Year and Station
  sql1 = "Select Ridership.Station_ID, Stations.Station_name \
  From Stations join Ridership On (Stations.Station_ID = Ridership.Station_ID) \
  where strftime('%Y', Ride_Date) like ? and Station_name like ? \
  group by Stations.Station_name \
  order by strftime('%m', Ride_Date) asc;"
  # Get First and last 5 days and daily ridership for year
  sql2 = "Select strftime('%Y-%m-%d',Ridership.Ride_Date), Ridership.Num_Riders \
  From Stations join Ridership On (Stations.Station_ID = Ridership.Station_ID) \
  where strftime('%Y', Ride_Date) like ? and Station_name like ? \
  group by Ride_Date \
  order by Ride_Date asc;" 
  ExtendStationsByYear(dbCursor, sql1, sql2, year)

###########################################################  
#
# RiderByMonth
#
# Outputs the total sum of Riders per Year and allows 
# for user to output a plot chart if they choose.
#
def RidersByYear(dbCursor):
  print("** ridership by year **")
  sql = "Select strftime('%Y', Ride_Date), sum(Num_Riders) \
  from Ridership \
  group by strftime('%Y', Ride_Date) \
  order by strftime('%Y', Ride_Date) asc;"
  dbCursor.execute(sql)
  Years = dbCursor.fetchall()  
  for x in Years:
    print(x[0], ":", f"{x[1]:,}")
  plot = input("\nPlot? (y/n) ")
  if(plot == "y"):
    figure.close("all")
    # Create two empty vectors
    x =[]
    y =[]
    for row in Years:
      # For x.append I used slice row[elem][2nd str:4th str]
      x.append(row[0][2:4]) 
      y.append(row[1])
    figure.xlabel("year")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("yearly ridership")
    figure.plot(x,y)
    figure.show()  

###########################################################  
#
# RiderByMonth
#
# Outputs the total sum of Riders per month and allows 
# for user to output a plot chart if they choose.
#
def RidersByMonth(dbCursor):
  print("** ridership by month **")
  sql = "Select strftime('%m', Ride_Date), sum(Num_Riders) \
  from Ridership \
  group by strftime('%m', Ride_Date) \
  order by strftime('%m', Ride_Date) asc;"
  dbCursor.execute(sql)
  Months = dbCursor.fetchall()  
  for x in Months:
    print(x[0], ":", f"{x[1]:,}")
  plot = input("\nPlot? (y/n) ")
  if(plot == "y"):
    figure.close("all")
    # Create two empty vectors
    x =[]
    y =[]
    for row in Months:
      x.append(row[0])
      y.append(row[1])
    figure.xlabel("month")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("monthly ridership")
    figure.plot(x,y)
    figure.show()

###########################################################  
#
# colorStation
#
# Input station color and output all stop names of that color line
#
def colorStation(dbCursor):
  color = input("\nEnter a line color (e.g. Red or Yellow): ")
  sql = "Select Stops.Stop_Name, Stops.Direction, Stops.ADA  \
  From Stations join Stops On (Stations.Station_ID = Stops.Station_ID)\
  join StopDetails On (Stops.Stop_ID = StopDetails.Stop_ID)\
  join Lines On (StopDetails.Line_ID = Lines.Line_ID)\
  where Color like ?\
  order by Stops.Stop_Name asc;"
  dbCursor.execute(sql,[color])
  StationColor = dbCursor.fetchall()
  if(StationColor):
    for x in StationColor:
      if(x[2] == True ):
        print (x[0], ": direction =", x[1], "(accessible? yes)")
      else:
        print (x[0], ": direction =", x[1], "(accessible? no)")
  else:
    print("**No such line...")

###########################################################  
#
# min10Stations
#
# Get the least 10 busiest Stations 
#
def min10Stations(dbCursor, totalRiders):
  print("** least-10 stations **")
  sql = "Select Station_Name, sum(Num_Riders)\
  From Stations join Ridership on\
  (Stations.station_id = Ridership.station_id)\
  group by Stations.Station_Name \
  order by sum(Ridership.Num_Riders) asc \
  limit 10;"  
  dbCursor.execute(sql)
  min10 = dbCursor.fetchall()
  for x in min10:
    print(x[0], ":", f"{x[1]:,}", f"({x[1]/totalRiders[0]:.2%})")

###########################################################  
#
# command3
#
# Get the top 10 busiest Stations 
#
def top10Stations(dbCursor, totalRiders):
  print("** top-10 stations **")
  sql = "Select Station_Name, sum(Num_Riders) \
  From Stations join Ridership on\
  (Stations.station_id = Ridership.station_id)\
  group by Stations.Station_Name \
  order by sum(Ridership.Num_Riders) desc \
  limit 10;"
  dbCursor.execute(sql)
  top10 = dbCursor.fetchall()
  for x in top10:
    print(x[0], ":", f"{x[1]:,}", f"({x[1]/totalRiders[0]:.2%})")

###########################################################  
#
# command2
#
# User get total Station names and sum of riders for station
# as well as percent.
#
def totalStations(dbCursor, totalRiders):
  print("** ridership all stations **")
  sql = "Select Station_Name, sum(Num_Riders)\
  From Stations join Ridership on\
  (Stations.station_id = Ridership.station_id)\
  group by Stations.Station_Name \
  order by Stations.Station_Name asc;"
  dbCursor.execute(sql)
  RiderPerStation = dbCursor.fetchall()
  for x in RiderPerStation:
    print(x[0], ":", f"{x[1]:,}", f"({x[1]/totalRiders[0]:.2%})")

###########################################################  
#
# command1
#
# User enters partial station name and outputs it to screen
#
def command1(dbCursor):
  cmd = input(f"\nEnter partial station name (wildcards _ and %): ")
  sql = "Select Station_ID, Station_Name \
  From Stations \
  Where Station_name like ? \
  Order by Station_Name asc;"
  dbCursor.execute(sql, [cmd])
  result = dbCursor.fetchall()
  if (result):
    for x in result:
      print (x[0], ":", x[1])
  else:
    print("**No stations found...")

###########################################################  
#
# prompt
#
# Menu prompt which user will be able to interactive and 
# select choice of preference.
#
def prompt(dbCursor, totalRiders):
  cmd = input("\nPlease enter a command (1-9, x to exit): ")
  while( cmd != "x"):
    # User enters partial station name and outputs it to screen
    if(cmd == "1"): 
      command1(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    # User get total Station names and sum of riders for station  
    elif(cmd == "2"):
      totalStations(dbCursor, totalRiders)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    # Get the top 10 busiest Stations   
    elif(cmd == "3"):
      top10Stations(dbCursor, totalRiders)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    # Get the least 10 busiest Stations   
    elif(cmd == "4"):
      min10Stations(dbCursor, totalRiders)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    # Input station color and output all stop names of that color line  
    elif(cmd == "5"):
      colorStation(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    # Output total ridership by month and option to plot data  
    elif(cmd == "6"):
      RidersByMonth(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    elif(cmd == "7"):
      RidersByYear(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    elif(cmd == "8"):
      StationsByYear(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    elif(cmd == "9"):
      LineColor(dbCursor)
      cmd = input("\nPlease enter a command (1-9, x to exit): ")
    else:
      print("**Error, unknown command, try again...")
      cmd = input("\nPlease enter a command (1-9, x to exit): ")

###########################################################  
#
# total_Ridership
#
# Prints the total of riders based on weekday,
# weekend or holiday.
#
def total_Ridership(dbCursor, totalRiders):
    # Output weekday riders and percent
    print("  Total ridership:", f"{totalRiders[0]:,}")  
    dbCursor.execute("Select sum(Num_Riders) \
    From Ridership \
    Where Type_of_Day = 'W';")
    WeekdayRiders = dbCursor.fetchone()
    print("  Weekday ridership:", f"{WeekdayRiders[0]:,}", 
    "("+f"{WeekdayRiders[0]/totalRiders[0]:.2%}"+")") 
    # Output Saturday riders total and percent
    dbCursor.execute("Select sum(Num_Riders), Type_of_Day \
    From Ridership \
    Where Type_of_Day = 'A';")
    SatRiders = dbCursor.fetchone()
    print("  Saturday ridership:", f"{SatRiders[0]:,}",
    "("+f"{SatRiders[0]/totalRiders[0]:.2%}"+")")
    # Output Sunday/Holiday ridership and total 
    dbCursor.execute("Select sum(Num_Riders), Type_of_Day \
    From Ridership \
    Where Type_of_Day = 'U';")
    SundayRiders = dbCursor.fetchone()
    print("  Sunday/holiday ridership:", f"{SundayRiders[0]:,}",
    "("+f"{SundayRiders[0]/totalRiders[0]:.2%}"+")")

###########################################################  
#
# dateRange
#
# Prints the first and last date in the table 
#
def dateRange(dbCursor, totalRiders):    
    # Executing FIRST date range entry from Ridership  
    dbCursor.execute("Select strftime('%Y-%m-%d',Ride_Date)\
    From Ridership \
    Order by Ride_date asc;")
    # Executing LAST date range entry from Ridership  
    firstRow = dbCursor.fetchone()
    dbCursor.execute("Select strftime('%Y-%m-%d',Ride_Date)\
    From Ridership \
    Order by Ride_date desc;")
    lastRow = dbCursor.fetchone()
    print("  date range:", firstRow[0], "-", lastRow[0])
    # Calling method/function of total riders based on weekday or 
    # weekend or holiday
    total_Ridership(dbCursor, totalRiders)
        
###########################################################  
#
# print_count
#
# Prints a count of stations, stops, rides
# SQL queries to retrieve and output basic stats.
#
def calcStat(dbCursor, totalRiders):
    # Executing count of stations entries from Stations
    dbCursor.execute("Select count(*) From Stations;")
    totalStations = dbCursor.fetchone()
    print("  # of stations:", f"{totalStations[0]:,}")
    # Executing count of stops entries from Stops
    dbCursor.execute("Select count(*) From Stops;")
    totalStops = dbCursor.fetchone()
    print("  # of stops:", f"{totalStops[0]:,}")   
    # Executing count of ride entries from Ridership
    dbCursor.execute("Select count(*) From Ridership;")
    totalRides = dbCursor.fetchone()
    print("  # of ride entries:", f"{totalRides[0]:,}") 
    # Grab date range
    dateRange(dbCursor, totalRiders)

###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General stats:")
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    totalRiders = dbCursor.fetchone()
    calcStat(dbCursor, totalRiders)
    prompt(dbCursor, totalRiders)
    
###########################################################  
#
# main
#
print('** Welcome to CTA L analysis app **\n')
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
print_stats(dbConn)
dbConn.close()
quit()
#
# done
#
