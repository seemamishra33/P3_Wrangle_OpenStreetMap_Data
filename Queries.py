pipeline_beauty = [{"$match":{"amenity":{"$exists":1}, "amenity": "beauty", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]


pipeline_library = [{"$match":{"amenity":{"$exists":1}, "amenity": "library", "name":{"$exists":1}}},
            {"$group":{"_id":"$name"}},
            {"$sort":{"count":-1}}]


pipeline_school = [{"$match":{"amenity":{"$exists":1}, "amenity": "school", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_parking = [{"$match":{"amenity":{"$exists":1}, "amenity": "parking", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 3}]

pipeline_car_wash = [{"$match":{"amenity":{"$exists":1}, "amenity": "car_wash", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$sort":{"count":-1}},
           {"$limit": 3}]

pipeline_place_of_worship = [{"$match":{"amenity":{"$exists":1}, "amenity": "place_of_worship", "name":  {"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]


pipeline_fuel = [{"$match":{"amenity":{"$exists":1}, "amenity": "fuel", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_hospital = [{"$match":{"amenity":{"$exists":1}, "amenity": "hospital", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]

pipeline_post_box = [{"$match":{"amenity":{"$exists":1}, "amenity": "post_box", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]

pipeline_highway =[{"$group":{"_id":"$highway", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit":5}]

pipeline_exit_to =[{"$group":{"_id":"$exit_to", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_building =  [{'$match': {'building': {'$exists': 1}}}, 
    {'$group': { '_id': '$building','count': {'$sum': 1}}},
    {'$sort': {'count': -1}}, {'$limit': 5}]

pipeline_restaurant = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant", "cuisine":{"$exists":1}}}, 
            {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},        
            {"$sort":{"count":-1}}, 

pipeline_fast_food = [{"$match":{"amenity":{"$exists":1}, "amenity": "fast_food", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit": 5}]
            {"$limit":5}]

pipeline_cafe = [{"$match":{"amenity":{"$exists":1}, "amenity": "cafe", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_user =[{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_timestamp =[{"$group":{"_id":"$created.timestamp", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},
           {"$limit": 5}]

pipeline_created_by = [{"$group":{"_id": "$created_by","count": {"$sum": 1}}},
                     {"$sort": {"count": -1}},
                    {"$limit": 5}]


pipeline_university = [{"$match":{"amenity":{"$exists":1}, "amenity": "university", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
