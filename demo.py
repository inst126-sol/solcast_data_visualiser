import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

api_base = 'https://api.solcast.com.au'
solcast_api_key =  "Zr4AINd9PudrH8TRJTV2AwIKa7giqYQf"
#api_key = "Zr4AINd9PudrH8TRJTV2AwIKa7giqYQf"

statuscode = 0

address = input("Write the address you are looking up (ex. 12345 Oxhammer Rd, New York, NY 67890, USA): ")
#while (address.lower().strip() is not "done") and (requested_data is not "done"):
delimiter = ' '
address_parts = address.split(", ")
street_address = address_parts[0].split()
house_number = str(street_address[0])
street = delimiter.join(street_address[1:]).rstrip(",")
city = address_parts[1]
state_zip = address_parts[2].split()
#state = state_zip[0].upper()
#zip_code = state_zip[1]
country =

print(house_number)
print(street)
print(city)
print(state)
print(zip_code)

#house_number = input("Enter a house or street number: ")
#street = input("Enter a street name: ")
#city =  input("Enter city name: ")
#country = input("Enter the country address: ")


def here_call(house_number,street,city,country):

    #app_id and app_code are paramters form the Here project website
  app_id = 'zI8FECxjf9LGliewQa5u'
  app_code = 'okD8RNAk-DkxBkisBguzpg'

  #API GET REQUESTS
  here_response = requests.get("https://geocoder.api.here.com/6.2/geocode.json", params ={"app_id": app_id,"app_code":app_code, 'housenumber': house_number, 'street':street, "city":city, "zip":zip_code} )

  #NOTE 2 SELF : ADD RESPONSE IF API CALL IS BAD / NOT 200
  status = here_response.status_code
  if status == 200:
    api_content = here_response.json()

    if len(api_content) == 0:
      print("The address you enter was not found. This may be to a incorrect spelling! Try again")

  else:
    locationinfo = api_content["Response"]["View"][0]["Result"][0]
    latitude = locationinfo['Location']['DisplayPosition']['Latitude']
    longitude = locationinfo['Location']['DisplayPosition']['Longitude']

    return [latitude,longitude]

#The Longitude and Laitiude for the address entered if HERE CODER API was successful

latitude1 = here_call(house_number,street,city,country)[0]
longitude1 = here_call(house_number,street,city,country)[1]

# Accessing SolCast API for  World Solar radiation Data at point Content should include estimated actuals

def world_sol_radiation_data_api(longitude,latitude):

  response = requests.get(

                "https://api.solcast.com.au/world_radiation/estimated_actuals.json",
                params = {
                    'api_key':solcast_api_key,
                    'latitude':latitude,
                     'longitude': longitude }
                     ) # Specify Longitude, langitude


  statuscode = response.status_code
  api_content = response.json()
  #print(statuscode)
  #print(response.content)
  return api_content

# Accessing Solcast API for Rooftop Sites at point Content should include estimated actuals

def rooftop_sites():

  response = requests.get(
       "https://api.solcast.com.au/rooftop_sites/{a6b0-f9cc-4e61-89c5}/estimated_actuals.json",
       params = {
           'api_key': solcast_api_key,
           'latitude':latiude1,
           'longitude': longitude1,
           'capacity': 5,
           'tilt': 23,
           'azimuth' : 0,
           'loss_factor' : 0.9
           })
  statuscode = response.status_code
  api_content = response.json()
  #print(statuscode)
  #print(response.content)
  return api_content

def world_pv_power():
  response = requests.get(
       "https://api.solcast.com.au/world_pv_power/estimated_actuals.json",
       params = {
           'api_key': solcast_api_key,
           'latitude': latitude1,
           'longtitude' : longitude1,
           'capacity': 33.895
       }
    )
  statuscode = response.status_code
  print(statuscode)
  api_content = response.json()
  return api_content


# get data from api
raw_world_data = world_sol_radiation_data_api(longitude1,latitude1)['estimated_actuals']
raw_rooftop_data = rooftop_sites()['estimated_actuals']
raw_worldpv_data = world_pv_power()['estimated_actuals']

# convert json data into dictionary readable by panda - bring over to main branch
def convert_data(raw_data):
  data = {}
    # initialize key-value pairs as empty lists
  for variable in raw_data[0]:
      data[variable] = []
    # restructure raw data into dictionary with variable labels as keys and data as values
  for i in range(len(raw_data)):
      for variable in raw_data[i]:
          list = data[variable]
          list.append(raw_data[i][variable])
    # construct dataframe
  df = pd.DataFrame.from_dict(data)
  return df

world_df = convert_data(raw_world_data)
rooftop_df = convert_data(raw_rooftop_data)
worldpvdf = convert_data(raw_worldpv_data)

# create a list of times from 'period_end' - these will be our axis labels
def time_labels(data_frame):
    times = []
    for i in range(len(data_frame)):
        date_time = data_frame['period_end'][i]
          #print(i)
        time = date_time[11:16]
          #print(time)
        times.append(time)
    return times

world_df['period_end_time'] = time_labels(world_df)

# plot world_df as lineplot
plt.plot('period_end','ghi', data=world_df)
plt.title('ghi: estimated actual')
plt.xlabel('Time (GMT+0)')
plt.ylabel('ghi')
plt.xticks(world_df['period_end'], world_df['period_end_time'], rotation = 'vertical')
plt.subplots_adjust(right=3, top = 1)
plt.show()


rooftop_df['period_end_time'] = time_labels(rooftop_df)

# plot rooftop as lineplot
plt.plot('period_end','pv_estimate', data=rooftop_df)
plt.title('pv_estimate: estimated actual')
plt.xlabel('Time (GMT+0)')
plt.ylabel('pv_estimate')
plt.xticks(rooftop_df['period_end'], rooftop_df['period_end_time'], rotation = 'vertical')
plt.subplots_adjust(right=3, top = 1)
plt.show()
