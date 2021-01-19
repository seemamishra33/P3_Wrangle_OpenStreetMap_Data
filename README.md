# Mountain View, CA Open Street Data Analysis

### Introduction ###
The aim of the priject is to select the map from the region of world, get the data, audit the data and fix the problems encountered in data. Then import the cleaned data into databse and perform several queries against it.  

### OSM Data ###

* I am using OpenStreetMap data of Mountain View city, California downloaded from [mapzen](https://mapzen.com/data/metro-extracts/). The date of downloading the dataset is March 27, 2017 at 10:21 AM.
* The format of datafile is in XML format, and we can find the description of Open Street XML format [here](http://wiki.openstreetmap.org/wiki/OSM_XML).

### Database ###

* MongoDB

### Problem encoutered  in Mountain View OSM map ###

* There are some inconsistencies in the names of streets, some are incorrect and overabbreviated("S California Ave", "Wolfe Rd").
* Few inconsistent zip codes.
* There ae inconsistency in phone numbers stored by users("650-322-2554", "+16508570333","(650) 327-1688").

* This been noticed the OSM data extracted from mapzen extracts tool cotains data about others cities besides the chosen one. So other cities data is also exhibited durig queries.


### Overview of Mountain View OSM data ###

The dataset description is given as


#### Size of data file ####
* MountainView.osm(The original downloaded OpenStreetMap in xml format): 209MB
* MountainView.osm.json(The processed OpenStreetMap in json format): 346MB

#### Summary of descriptive statistics of dataset ####

* Number of documents: 5754659
* Number of unique users: 880
* Number of nodes: 5136303
* Number of ways: 618301

