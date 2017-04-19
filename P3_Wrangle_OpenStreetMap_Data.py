
# coding: utf-8

# 
# 
# ### Introduction ###
# The aim of the priject is to select the map from the region of world, get the data, audit the data and fix the problems encountered in data. Then import the cleaned data into databse and perform several queries against it.  
# 
# ### OSM Data ###
# 
# * I am using OpenStreetMap data of Mountain View city, California downloaded from [mapzen](https://mapzen.com/data/metro-extracts/). The date of downloading the dataset is March 27, 2017 at 10:21 AM.
# * The format of datafile is in XML format, and we can find the description og Open Street XML format [here](http://wiki.openstreetmap.org/wiki/OSM_XML).
# 
# ### Database###
# 
# * MongoDB
# 
# ### Problem encoutered  in Mountain View OSM map ###
# 
# * There are some inconsistencies in the names of streets, some are incorrect and overabbreviated("S California Ave", "Wolfe Rd").
# * Few inconsistent zip codes.
# * There ae inconsistency in phone numbers stored by users("650-322-2554", "+16508570333","(650) 327-1688").
# 
# * This been noticed the OSM data extracted from mapzen extracts tool cotains data about others cities besides the chosen one. So other cities data is also exhibited durig queries.
# 
# 
# ### Overview of Mountain View OSM data ###
# 
# The dataset description is given as
# 
# 
# #### Size of data file ####
# * MountainView.osm(The original downloaded OpenStreetMap in xml format): 209MB
# * MountainView.osm.json(The processed OpenStreetMap in json format): 346MB
# 
# #### Summary of descriptive statistics of dataset ####
# 
# * Number of documents: 5754659
# * Number of unique users: 880
# * Number of nodes: 5136303
# * Number of ways: 618301
# 
# ### References ###
# 
# 1. [Udacity Sample Data Wrangling Project](https://docs.google.com/document/d/1F0Vs14oNEs2idFJR3C_OPxwS6L0HPliOii-QpbmrMo4/pub)
# 
# 2.  <https://zelite.github.io/Wrangle-OpenStreetMap-Data/>
# 
# 3. <https://english.stackexchange.com/questions/29009/standard-format-for-phone-numbers>
# 
# ### Code and Results ###
# There are several queries generated for looking deep insight of data which is follwed by conclusion .
# 
# 
# 
# 
# 
# <b>Import Libraries</b>

# In[102]:

# load libraries
import os
import xml.etree.cElementTree as cET
from collections import defaultdict
import pprint
import re
import codecs
import json
import string
from pymongo import MongoClient
from cleaning import *
from audit import *
from process_map import *


# In[103]:

# set up map file path
filename = "MountainView.osm" # osm filename
# filename = "sample200.osm" # Sample osm filename
path = "/Users/seemamishra/Desktop/Udacity/Data_Wrangling/P3_Data" # directory contain the osm file
MountainViewosm = os.path.join(path, filename)

# MountainViewosm = "MountainView.osm" # osm filename
# path = "d:\GithubRepos\Udacity\P3" # directory contain the osm file
lower = re.compile(r'^([a-z]|_)*$') 
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# initial version of expected street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane",
            "Road", "Trail", "Parkway", "Commons", "highway"]
MountainViewosm


# #### Count the number of Tags ###

# In[104]:


if __name__ == "__main__":
    print count_tags(MountainViewosm)


# ####  Tags types ###

# In[105]:


if __name__ == "__main__":
    print process_map(MountainViewosm)


# #### Audit the street names ###

# In[72]:


if __name__ == '__main__':
    st_types = audit_street(MountainViewosm)
    # print out unexpected street names
#     pprint.pprint(dict(st_types))




# #### Update the street name ###

# In[99]:

# Street name updatation
# creating a dictionary for correcting street names
mapping_street = { "AA" :"Aberdeen Athletic Center",
            "Ct": "Court",
            "Ct.": "Court",
            "St.": "Street",
            "St,": "Street",
            "ST": "Street",
            "street": "Street",
            "STE": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Rd.": "Road",   
            "rd.": "Road",
            "Rd": "Road",    
            "Hwy": "Highway",
            "HIghway": "Highway",
            "BLDG": "Building",
            "APT": "Apartment",
           "West Evelyn Avenue Suite #114":"West Evelyn Avenue Suite",
           "Showers Drive STE 2": "Showers Drive Street",
           "Showers Drive STE 7": "Showers Drive Street",
           "East Charleston Road APT 9": "East Charleston Road Apartment",
           "Leghorn Street #B": "Leghorn Street",
           "Plymouth Street #C": "Plymouth Street",
           "Hamilton Ave #140": "Hamilton Ave",
           "W. El Camino Real": "West El Camino Real",
           "W El Camino Real":"West El Camino Real",
           "E. El Camino Real": "East El Camino Real",
           "E El Camino Real" : "East El Camino Real",
           "West Dana St": "West Dana Street"
           }
           
                
if __name__ == '__main__':
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_street)
#             print name, "=>", better_name


# #### Audit zip codes

# In[107]:


if __name__ == '__main__':
    zipcodes = audit_zipcodes(MountainViewosm)
# for zipcode in zipcodes:
#     print zipcode, zipcodes[zipcode]
# zipcodes


# #### strategy for updating zip code ###
# 
# Since the data also includes the area of Santa Clara, Cupetino, San Jose and Sunnyvale. I have only updated he zipcode of Moutain view which starts from '94' using mapping dictionary.

# In[92]:


mapping_zipcode = { "CA 94085":"94085",
            "CA 94086":"94086"
           }          
                          
          
if __name__ == '__main__':
    for zipcode in zipcodes:
        better_zipcode = update_zipcode(zipcode, mapping_zipcode)
#         print zipcode, "=>", better_zipcode
        


# 
# 
# #### Process OSM XML file to JSON ###
# Only the elements of type “node” and “way” will be imported to the database. The data model we’re going to use follows the format of this example:
# {
# "id": "2406124091",
# "type: "node",
# "visible":"true",
# "created": {
#          "version":"2",
#          "changeset":"17206049",
#          "timestamp":"2013-08-03T16:43:42Z",
#          "user":"linuxUser16",
#          "uid":"1219059"
#        },
# "pos": [41.9757030, -87.6921867],
# "address": {
#          "housenumber": "5157",
#          "postcode": "60625",
#          "street": "North Lincoln Ave"
#        },
# "amenity": "restaurant",
# "cuisine": "mexican",
# "name": "La Cabana De Don Luis",
# "phone": "1 (773)-271-5176"
# }
# 
# 

# #### Insert the JSON data into MongoDB Database ####

# In[100]:

# process the file
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
def shape_element(element):
    node = {}
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
#     node["amenity"] ={}
#     node["cuisine"] = {}
    refs=[]
    
    # I only process the node and way tags
    if element.tag == "node" or element.tag == "way" :
        if "id" in element.attrib:
            node["id"]=element.attrib["id"]
        node["type"]=element.tag

        if "visible" in element.attrib.keys():
            node["visible"]=element.attrib["visible"]
      
        # the key-value pairs with attributes in the CREATED list are added under key "created"
        for elem in CREATED:
            if elem in element.attrib:
                node["created"][elem]=element.attrib[elem]
                
        # attributes for latitude and longitude are added to a "pos" array
        # include latitude value        
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        # include longitude value    
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))

        
        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"]=tag.attrib['v']
                    
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"]=tag.attrib['v']
                    node["address"]["postcode"] = update_name(node["address"]["postcode"], mapping_zipcode)
                # handling the street attribute, update incorrect names using the strategy developed before   
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']
                    node["address"]["street"] = update_zipcode(node["address"]["street"], mapping_street)

                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
                    
        for nd in element.iter("nd"):
             refs.append(nd.attrib["ref"])
                
        if node["address"] =={}:
            node.pop("address", None)

        if refs != []:
           node["node_refs"]=refs
            
        return node
    else:
        return None
if __name__ == '__main__':
    data = process_map(MountainViewosm, True)
# for d in data:
#     print d


# In[74]:

client = MongoClient()
db = client.MountainViewosm
collection = db.MountainViewMAP
collection.insert(data)


# #### Size of original XML file ####

# In[22]:


os.path.getsize(os.path.join(path, "MountainView.osm"))/1024/1024


# #### Size of processed JSON  file ####

# In[14]:


os.path.getsize(os.path.join(path, "MountainView.osm.json"))/1024/1024


# #### Number of documents ####

# In[15]:

collection.find().count()


# #### Number of unique users ####

# In[19]:

# Number of unique users
len(collection.group(["created.uid"], {}, {"count":0}, "function(o, p){p.count++}"))


# #### Number of nodes ####

# In[20]:

# Number of nodes
collection.find({"type":"node"}).count()


# #### Number of ways ####

# In[21]:

collection.find({"type":"way"}).count()


# #### Top 5 methods used to create data entry ####

# In[65]:


pipeline = [{"$group":{"_id": "$created_by","count": {"$sum": 1}}},
                     {"$sort": {"count": -1}},
                    {"$limit": 5}]
           
result = collection.aggregate(pipeline)
for r in result:
    print r
# assert len(result['result'])

# print(len(result['result']))
# print result[result]


# #### Top 5 users contributions ####

# In[42]:

import csv
# top three users with most contributions
pipeline = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
            ]
result = collection.aggregate(pipeline)
for r in result:
    print r





# ### Additional Data exploration

# #### Most popular fast food resturant ####

# In[45]:

# Most popular cuisines
pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant", "cuisine":{"$exists":1}}}, 
            {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},        
            {"$sort":{"count":-1}}, 
            {"$limit":5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Name of Universities ####

# In[25]:

# University
pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "university", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# ####  Places for worship ####

# In[83]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "place_of_worship", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# #### Gas stations ####

# In[82]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "fuel", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# #### Most popular Fast food cuisines ####

# In[48]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "fast_food", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Number of hospitals ####

# In[27]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "hospital", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Beauty Salon ####

# In[81]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "beauty", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# #### Libraries ####

# In[54]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "library", "name":{"$exists":1}}},
            {"$group":{"_id":"$name"}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# ####  most poular schools ####

# In[55]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "school", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Most popular Parkings ####

# In[80]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "parking", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 3}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# ####  Popular Car wash ####

# In[79]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "car_wash", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$sort":{"count":-1}},
           {"$limit": 3}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# #### Post office ####

# In[78]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "post_box", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
# for r in result:
#     print r


# #### most populr Coffe shops ####

# In[58]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "cafe", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# 
# 
# #### Top 5 unique contributor of data ####

# In[59]:

pipeline =[{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Top 5 timestamps when the data is  contributed  ####

# In[68]:

pipeline =[{"$group":{"_id":"$created.timestamp", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Highway ways in mountain view  ####

# In[67]:

pipeline =[{"$group":{"_id":"$highway", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit":5}
           ]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Types and number of ways in mountain view  ####

# In[66]:

pipeline =[{"$group":{"_id":"$exit_to", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}
           ]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Most common building types

# In[77]:

pipeline =  [{'$match': {'building': {'$exists': 1}}}, 
    {'$group': { '_id': '$building','count': {'$sum': 1}}},
    {'$sort': {'count': -1}}, {'$limit': 5}
]
result = collection.aggregate(pipeline)
for r in result:
    print r


# ### Other Ideas about data set 
# 1. Since the data consist of inconsistent phone numbers like "650-322-2554", "+16508570333" etc. During the collection of the data from user, it should follow the rule format of phone number of given country or area which is generraly in ITU E.123 standard:
#   - "+"
#   - 1.2 the national code (1 for the USA)
#   - space
#   - the area/regional code
#   - space
#   - the local exchange
#   - space
#   - the local number<br />
# 
# 2. There are some fields of node is missing like County, the data collection should follow the structured format. But it trivial because Nosql database can pretty much handle the non structured data.<br />
# 
# 3. To ensure the data collections lead to rich infomation about the nodes, the interface of website may follow some protocols while entering data using some altert like user can only enter data within this range depends on the region for which data is being entered.<br />
# 
# 4. To encourange contribution in data collection there might be some kind of gamification for the people.

# ### Conclusion
# After reviewing the data of mountain view, much of the information has been extracted about the city. The data has been well cleaned for the purpose of enough information extraction. Thinking about the compnies and startups established in Mountain view, i couldn't find any information regarding that. If the data is stored as in the name of comapnies and startups buildings, it would be really helpful to gain insight of number of the comapanies establishd in given city.
