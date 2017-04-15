
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
# ### Issues in Mountiav View OSM data ###
# 
# * There are some inconsistencies in the names of streets, some are incorrect and abbreviated.
# * Few inconsistent zip codes.
# * There ae inconsistency in phone numbers stored by users.
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
# There several queries generated for look deeep insight of data which is follwed by conclusion .
# 
# 
# 
# 
# 
# <b>Import Libraries</b>

# In[2]:

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


# In[3]:

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

# In[4]:

# Iterative parsing
def count_tags(filename):
    
    # make empty defaultdict
#     from collections import defaultdict
    tags_dict = defaultdict(int)
    
    # use the iterparse method to find all the tags
    for event, element in cET.iterparse(filename, events=("start", "end")):
#         print event
        tags_dict[element.tag] += 1
        
    # return your results 
    return tags_dict

if __name__ == "__main__":
    print count_tags(MountainViewosm)


# ####  Tags types ###

# In[5]:

# Tag types
def key_type(element, keys):
    if element.tag == "tag":
    
        k = element.attrib['k']
#         print k
        # serach k to see if it matches each regular expression
        if lower.search(k):
            keys['lower'] += 1
        elif lower_colon.search(k):
            keys['lower_colon'] += 1
        elif problemchars.search(k):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
           
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in cET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == "__main__":
    print process_map(MountainViewosm)


# #### Audit the street names ###

# In[6]:

def audit_street_type(street_types, street_name):
    # add unexpected street name to a list
    m = street_type_re.search(street_name)
#     print m
    if m:
        street_type = m.group()
#         street_type
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def is_street_name(elem):
    # determine whether a element is a street name
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    # iter through all street name tag under node or way and audit the street name value
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in cET.iterparse(osm_file, events=("start","end")):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types
if __name__ == '__main__':
    st_types = audit_street(MountainViewosm)
    # print out unexpected street names
    pprint.pprint(dict(st_types))




# #### Update the street name ###

# In[7]:

# Street name updatation
# creating a dictionary for correcting street names
mapping = { "AA" :"Aberdeen Athletic Center",
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
           
                     
# function that corrects incorrect street names
def update_name(name, mapping):    
    for key in mapping:
        if key in name:
            name = string.replace(name,key,mapping[key])
    return name
if __name__ == '__main__':
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


# In[8]:

# zip code
def audit_zipcodes(osmfile):
    # iter through all zip codes, collect all the zip codes that does not start with 94
    osm_file = open(osmfile, "r")
    zip_codes = {}
    for event, elem in cET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode" and not tag.attrib['v'].startswith('94'):
                    if tag.attrib['v'] not in zip_codes:
                        zip_codes[tag.attrib['v']] = 1
                    else:
                        zip_codes[tag.attrib['v']] += 1
    return zip_codes

zipcodes = audit_zipcodes(MountainViewosm)
for zipcode in zipcodes:
    print zipcode, zipcodes[zipcode]
# zipcodes


# #### strategy for updating zip code ###
# 
# Since the data also includes the area of Santa Clara, Cupetino, San Jose and Sunnyvale. I have only updated he zipcode of Moutain view which stats from '94' using mapping dictionary.

# In[70]:



mapping = { "CA 94085":"94085",
            "CA 94086":"94086"
           }
           
                     
# function that corrects incorrect street names
def update_zipcode(zipcode, mapping):    
    for key in mapping:
        if key in zipcode:
            zipcode = string.replace(zipcode, key,mapping[key])
        return zipcode
       
          
if __name__ == '__main__':
    for zipcode in zipcodes:
        better_zipcode = update_zipcode(zipcode, mapping)
        print zipcode, "=>", better_zipcode
        


# In[ ]:

# Audit phone number


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

# In[11]:


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
                
                # handling the street attribute, update incorrect names using the strategy developed before   
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']
                    node["address"]["street"] = update_name(node["address"]["street"], mapping)

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



def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in cET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


# In[21]:

# process the file
data = process_map(MountainViewosm, True)
# for d in data:
#     print d


# #### Insert the JSON data into MongoDB Database ####

# In[22]:

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


# #### Top 10 methods used to create data entry ####

# In[38]:


pipeline = [{"$group":{"_id": "$created_by",
                       "count": {"$sum": 1}}},
                     {"$sort": {"count": -1}},
                    {"$limit": 10}]
           
result = collection.aggregate(pipeline)
for r in result:
    print r
# assert len(result['result'])

# print(len(result['result']))
# print result[result]


# #### Top 5 users contributions ####

# In[23]:

# top three users with most contributions
pipeline = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# ### Top 10 amenity

# In[18]:

pipeline = [{'$match': {'amenity': {'$exists': 1}}}, 
                                {'$group': {'_id': '$amenity', 
                                            'count': {'$sum': 1}}}, 
                                {'$sort': {'count': -1}}, 
                                {'$limit': 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Most popular fast food resturant ####

# In[24]:

# Most popular cuisines
pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant", "cuisine":{"$exists":1}}}, 
            {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},        
            {"$sort":{"count":-1}}, 
            {"$limit":10}]
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


# #### 10 Places for worship ####

# In[23]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "place_of_worship", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Gas stations ####

# In[27]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "fuel", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### 10 Most popular Fast food cuisines ####

# In[24]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "fast_food", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit": 10}]
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

# In[30]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "beauty", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Libraries ####

# In[31]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "public_bookcase", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### 10 most poular schools ####

# In[26]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "school", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### 10 Most popular Parkings ####

# In[27]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "parking", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# ####  10 Most popular Car wash ####

# In[34]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "car_wash", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Post office ####

# In[35]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "post_box", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### 10 most populr Coffe shops ####

# In[29]:

pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "cafe", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# 
# 
# #### Top 10 unique contributor of data ####

# In[31]:

pipeline =[{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Top 10 version of contribution of data ####

# In[39]:

pipeline =[{"$group":{"_id":"$created.version", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Top 10 timestamps when the data is  contributed  ####

# In[25]:

pipeline =[{"$group":{"_id":"$created.timestamp", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Highway ways in mountain view  ####

# In[24]:

pipeline =[{"$group":{"_id":"$highway", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}
           ]
result = collection.aggregate(pipeline)
for r in result:
    print r


# #### Types and number of ways in mountain view  ####

# In[26]:

pipeline =[{"$group":{"_id":"$exit_to", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 10}
           ]
result = collection.aggregate(pipeline)
for r in result:
    print r


# ### Other Ideas about data set 
# Since the data consist of inconsistent phone numbers like "650-322-2554", "+16508570333" etc. During the collection of the data from user, it should follow the rule format of phone number of given country or area which is generraly in ITU E.123 standard:
# * "+"
# * the national code (1 for the USA)
# * space
# * the area/regional code
# * space
# * the local exchange
# * space
# * the local number
# 
# There are some fields of node is missing like County, the data collection should follow the structured format. But it trivial because Nosql database can pretty much handle the non structured data.

# ### Conclusion
# After reviewing the data of mountain view, much of the information has been extracted about the city. The data has been well cleaned for the purpose of enough information extraction. Thinking about the compnies and startups established in Mountain view, i couldn't find any information regarding that. If the data is stored as in the name of comapnies and startups buildings, it would be really helpful to gain insight of number of the comapanies establishd in given city.
