import requests
import json
import pandas as pd

api_base = 'https://api.solcast.com.au'

solcast_api_key =  "U7mG4zUHGW3gczhlcZslxE2QiWDOTGJl"
#api_key = "U7mG4zUHGW3gczhlcZslxE2QiWDOTGJl"

statuscode = 0

# Accessing SolCast API for  World Solar radiation Data at point Content should include estimated actuals

def world_sol_radiation_data_api():

  response = requests.get(

                "https://api.solcast.com.au/world_radiation/estimated_actuals.json",
                params = {
                    'api_key':solcast_api_key,
                    'latitude':33.895,
                     'longitude': -118.308}
                     ) # Specify Longitude, langitude


  statuscode = response.status_code
  api_content = response.json()
  #print(statuscode)
  #print(response.content)
  print(api_content)

# Accessing Solcast API for Rooftop Sites at point Content should include estimated actuals

def rooftop_sites():

  response = requests.get(
       "https://api.solcast.com.au/rooftop_sites/{a6b0-f9cc-4e61-89c5}/estimated_actuals.json",
       params = {
           'api_key': solcast_api_key,
           'latitude':33.895,
           'longitude': -118.308,
           'capacity': 5,
           'tilt': 23,
           'azimuth' : 0,
           'loss_factor' : 0.9
           })
  statuscode = response.status_code
  api_content = response.json()
  #print(statuscode)
  #print(response.content)
  print(api_content)

def world_pv_power:

   response = requests.get(

   )

world_data = json.loads(world_sol_radiation_data_api())
print(world_data)

rooftop_data = json.loads(rooftop_sites())
print(rooftop_data)
