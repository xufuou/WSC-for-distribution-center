# WSC-for-distribution-center
A python application to determine the best location for a distribution center using Weighting the Selection Criteria.

# Description of files

* Input: CSV file with information of possible sites(coords)
* Output: CSV file with the best location(FactSelec)
* tabulate.py - a python script to display arrays into tables
* projeto.py - the core script of the application
* pymaps.py - the Google Maps script for map visualization
* mymap.html - the html file to output the map

#Main features

A text based menu with the following options:

1. Read the information from the CSV file
2. Determine the best location based on WSC method
3. Generate a visualization map with Google Maps api of all possible locations and the best location
4. Save the best location to CSV file
5. Delete a factor of decision for WSC method
6. Add a factor of decision for WSC method

