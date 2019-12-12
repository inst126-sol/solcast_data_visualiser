import requests
import json
import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

def here_call(house_number,street,city,country):

#app_id and app_code are paramters form the Here project website
    app_id = 'zI8FECxjf9LGliewQa5u'
    app_code = 'okD8RNAk-DkxBkisBguzpg'

    #API GET REQUESTS
    here_response = requests.get("https://geocoder.api.here.com/6.2/geocode.json", params ={"app_id": app_id,"app_code": app_code, "housenumber": house_number, "street":street, "city": city, "country": country})
    #print(here_response)
    status = here_response.status_code
    api_content = here_response.json()
    if status != 200:
        print("The address you enter was not found. This may be to a incorrect spelling! Try again")

    else:
        locationinfo = api_content["Response"]["View"][0]["Result"][0]
        latitude = locationinfo['Location']['DisplayPosition']['Latitude']
        longitude = locationinfo['Location']['DisplayPosition']['Longitude']
        return [latitude,longitude]

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
  #print(statuscode)
  api_content = response.json()
  return api_content

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

def time_labels(data_frame):
    times = []
    for i in range(len(data_frame)):
        date_time = data_frame['period_end'][i]
          #print(i)
        time = date_time[11:16]
          #print(time)
        times.append(time)
    return times

def plot_ghi():
    # plot world_df as lineplot
    plt.plot('period_end','ghi', data=world_df)
    plt.title('fig. 1, ghi: estimated actual')
    plt.xlabel('Time (GMT+0)')
    plt.ylabel('ghi (W/m^2)')
    plt.xticks(world_df['period_end'], world_df['period_end_time'], rotation = 'vertical')
    plt.subplots_adjust(right=3, top = 1)
    plt.show()

def plot_ebh():
    # plot world_df as lineplot
    plt.plot('period_end','ebh', data=world_df)
    plt.title('fig. 1, ebh: estimated actual')
    plt.xlabel('Time (GMT+0)')
    plt.ylabel('ebh (W/m^2)')
    plt.xticks(world_df['period_end'], world_df['period_end_time'], rotation = 'vertical')
    plt.subplots_adjust(right=3, top = 1)
    plt.show()

def plot_dhi():
    # plot world_df as lineplot
    plt.plot('period_end','dhi', data=world_df)
    plt.title('fig. 1, dhi: estimated actual')
    plt.xlabel('Time (GMT+0)')
    plt.ylabel('dhi (W/m^2)')
    plt.xticks(world_df['period_end'], world_df['period_end_time'], rotation = 'vertical')
    plt.subplots_adjust(right=3, top = 1)
    plt.show()

def plot_dni():
    # plot world_df as lineplot
    plt.plot('period_end','dni', data=world_df)
    plt.title('fig. 1, dni: estimated actual')
    plt.xlabel('Time (GMT+0)')
    plt.ylabel('dni (W/m^2)')
    plt.xticks(world_df['period_end'], world_df['period_end_time'], rotation = 'vertical')
    plt.subplots_adjust(right=3, top = 1)
    plt.show()

def plot_pv_estimate():
    # plot rooftop as lineplot
    plt.plot('period_end','pv_estimate', data=worldpv_df)
    plt.title('fig. 2, pv estimate: estimated actual')
    plt.xlabel('Time (GMT+0)')
    plt.ylabel('pv estimate')
    plt.xticks(worldpv_df['period_end'], worldpv_df['period_end_time'], rotation = 'vertical')
    plt.subplots_adjust(right=3, top = 1)
    plt.show()



# global variable definitions

api_base = 'https://api.solcast.com.au'
solcast_api_key =  "Zr4AINd9PudrH8TRJTV2AwIKa7giqYQf"
#api_key = "Zr4AINd9PudrH8TRJTV2AwIKa7giqYQf"

statuscode = 0

i = 0
address = input("Write the address you are looking up (ex. 12345 Oxhammer, New York, NY 67890, USA): ")

# main code
while (address.lower().strip() is not "done") and (i < 5):
    delimiter = ' '

    address_parts = address.split(", ")
    street_address = address_parts[0].split()
    house_number = int(street_address[0])
    street = delimiter.join(street_address[1:]).rstrip(",").lower()
    city = address_parts[1].lower()
    #state_zip = address_parts[2].split()
    #state = state_zip[0].upper()
    #zip_code = state_zip[1]
    country = address_parts[3].lower()

    #print(house_number)
    #print(street)
    #print(city)
    #print(country)

    #The Longitude and Laitiude for the address entered if HERE CODER API was successful

    latitude1 = here_call(house_number,street,city,country)[0]
    longitude1 = here_call(house_number,street,city,country)[1]

    varnames = ['ghi', 'dhi','ebh','dni']

    variable_request = input("Which radiation variable would you like to plot? (ghi/dhi/ebh/dni): ")
    if variable_request == "done":
      break
    elif variable_request not in varnames:
      print('Not a valid data set. %d attempts left.\n' % (5-i))
    else:
        # get data from api
        raw_world_data = world_sol_radiation_data_api(longitude1,latitude1)['estimated_actuals']
        raw_worldpv_data = world_pv_power()['estimated_actuals']

        world_df = convert_data(raw_world_data)
        worldpv_df = convert_data(raw_worldpv_data)

        # create a list of times from 'period_end' - these will be our axis labels

        world_df['period_end_time'] = time_labels(world_df)
        worldpv_df['period_end_time'] = time_labels(worldpv_df)
        if variable_request == "ghi":
            plot_ghi()
            print('Figure 1: Global Horizontal Irradiance (GHI, W/m2): The total irradiance received on a horizontal surface. It is the sum of the horizontal components of direct (beam) and diffuse irradiance. GHI = DNI*cosθ + DHI.')
        elif variable_request == "ebh":
            plot_ebh()
            print('Figure 1: Direct (Beam) Horizontal Irradiance (EBH, W/m2): The horizontal component of Direct Normal Irradiance.'
        elif variable_request == "dhi":
            plot_dhi()
            print('Diffuse Horizontal Irradiance (DIF, DHI, W/m2): The horizontal component of diffuse irradiance (irradiance that is scattered by the atmosphere). When passing through the atmosphere, the solar radiation is scattered, reflected, and absorbed by air molecules, aerosol particles, water droplets and ice crystals in clouds. This produces diffuse solar radiation.')
        elif variable_request == "dni":
            plot_dni()
            print('Figure 1: Direct Normal Irradiance (DNI, W/m2): Solar irradiance arriving in a direct line from the sun as measured on a surface held perpendicular to the sun. As the sun moves down, the Direct Normal Irradiance (DNI) beam strikes the Earth’s surface obliquely, and spreads out, reducing the amount of energy per unit area as a cosine function.')
        elif variable_request == "done":
          break
        plot_pv_estimate()
        print('%d attempts left.' % (5-i))
    i += 1
