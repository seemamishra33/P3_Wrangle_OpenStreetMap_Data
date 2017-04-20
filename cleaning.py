# Update street name
def update_name(name, mapping):    
    for key in mapping:
        if key in name:
            name = string.replace(name,key,mapping[key])
    return name


# Update zipcodes
def update_zipcode(zipcode, mapping):    
    for key in mapping:
        zipcode = string.replace(zipcode, key,mapping[key])
    return zipcode