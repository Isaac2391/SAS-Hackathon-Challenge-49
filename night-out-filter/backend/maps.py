import googlemaps
import json
import requests
import time
from pprint import pprint

API_KEY = "AIzaSyCZmQFw2CQ7UUddbhIzjiLm_rFAlG2xucU"

gmaps = googlemaps.Client(key=API_KEY)



def Search(search_category):
    with open("allowedtypes.txt", "r") as f:
            validated_types_list = []
            words = f.read().split("\n")
            search_type = search_category.lower().strip().split("and")
            try:
                for word in search_type:
                    newword = word.strip(" ").replace(" ","_")
                    
                    if newword in words:
                        validated_types_list.append(newword)       
            except Exception as e:
                print(e)
    if validated_types_list == []:
        print(f"error wrong input")
        return
    
          
    pagelist = []
    places_results = gmaps.places_nearby(location="55.8617,-4.26",radius= 9656,type=validated_types_list)
    pagelist.extend(places_results["results"])
    
    if "next_page_token" in places_results:
        time.sleep(3)
        
        places_results = gmaps.places_nearby(page_token = places_results["next_page_token"])
        pagelist.extend(places_results["results"])
    

Search()
    
    
    
    