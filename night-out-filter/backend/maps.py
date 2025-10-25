import googlemaps
import json
import requests
import time
from pprint import pprint

API_KEY = "AIzaSyCZmQFw2CQ7UUddbhIzjiLm_rFAlG2xucU"

gmaps = googlemaps.Client(key=API_KEY)



def Search():
    
    
    places_results = gmaps.places_nearby(location="55.8617,-4.26",radius= 2000,type="cafe")

    
    time.sleep(3)
    
    places_results = gmaps.places_nearby(page_token = places_results["next_page_token"])
    print(places_results)
    

Search()
    
    
    
    