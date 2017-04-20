from collections import defaultdict


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
