import pandas as pd
import certifi
import ssl
import time
import geopy.geocoders
from geopy.geocoders import Nominatim

# import csv file
input_file = "Meteorite World Map_Summary.csv"
df = pd.read_csv(input_file)

# create empty columns
df['country'] = ''
df['state'] = ''

# get location using lat and long
def getLocation(i, lat, long):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.reverse(str(lat) + ', ' + str(long), timeout=10)

    if location:
        address = location.raw['address']
        if 'country' in address: df.loc[i, 'country'] = address['country']
        if 'state' in address: df.loc[i, 'state'] = address['state']
    return

# iterate through each row of the data
for i in range(len(df)):
    lat, long = df.loc[i, 'Reclat'], df.loc[i, 'Reclong']
    if pd.isna(lat) or pd.isna(long) or lat == 0 or long == 0:
        continue
    getLocation(i, lat, long)
    time.sleep(0.05)

# export csv file
df.to_csv('new_data.csv')
