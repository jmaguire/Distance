distanceJSON.py: Calculates distance between cities, prints closest matches to the command line in JSON format. Currently prints 10 matches. Can print any arbitrary amount by updated the input 'numCities' to the function toJson.

runDistanceScript.py: Loads JSON inputs for metric and spending tuple and then calls distanceJSON.py with via command line with arguements.

benchmarkData.json: your benchmark data

./json: folder with city data in json format

./WeightsJSON: folder with new command line inputs in json format. New versions of the older profiles have been added. CSV files with Normalized values (weights needed such that measure on average is 1) have been added.


*****the .json command line inputs are in the json format... but are not escaped (\" instead of "). I have to convert to JSON another time before i can paste them to the command line... ./WeightsJSONEscaped contains escaped versions that can be directly pasted as command line arguements


example:
  
python distanceJSON.py "City Name"     "[[\"Population, 2010  \", \"0.00014\"], [\"Area\", \"0.7\"], [\"Population Density (2010)\", \"0.0014\"], [\"Mean travel time to work (minutes), workers age 16+, 2006-2010  \", \"0.1\"], [\"Manufacturers shipments, 2007\", \"0.00000003\"], [\"Persons under 18 years, percent, 2010  \", \"15\"], [\"Persons below poverty level, percent, 2006-2010  \", \"40\"], [\"Foreign born persons, percent,  2006-2010  \", \"15\"], [\"Bachelor's degree or higher, pct of persons age 25+, 2006-2010  \", \"15\"], [\"Asian persons, percent, 2010 \", \"55\"], [\"Persons 65 years and over, percent,  2010  \", \"35\"], [\"Total number of firms, 2007  \", \"0.0013\"], [\"Homeownership rate, 2006-2010  \", \"8\"], [\"Persons per household, 2006-2010  \", \"1.6\"], [\"Households, 2006-2010  \", \"0.0004\"], [\"Housing units in multi-unit structures, percent, 2006-2010  \", \"15\"], [\"Merchant wholesaler sales, 2007 \", \"2.00E-08\"], [\"Retail sales, 2007 \", \"1.00E-08\"], [\"Black persons, percent, 2010 \", \"230\"], [\"White persons, percent, 2010 \", \"8\"], [\"Retail sales per capita, 2007  \", \"0.00038\"], [\"White persons not Hispanic, percent, 2010  \", \"9\"], [\"Median value of owner-occupied housing units, 2006-2010  \", \"1.50E-05\"], [\"Land area in square miles, 2010  \", \"0.7\"], [\"Per capita money income in past 12 months (2010 dollars) 2006-2010 \", \"0.0002\"], [\"Female persons, percent, 2010  \", \"8\"], [\"High school graduates, percent of persons age 25+, 2006-2010  \", \"7\"], [\"Median household income 2006-2010  \", \"8.00E-05\"], [\"Violent crime per 100k people\", \"0.02\"], [\"Property crime per 100k people\", \"0.003\"]]"          "[[\"Expenditure\", \"Transportation\", \"Public Transit\", 0.005], [\"Expenditure\", \"Public Safety\", \"Fire\", 3e-07], [\"Revenue\", \"Fines and Forfeitures\", \"Other Fines, Forfeitures, and Penalties\", 2e-06]]"


