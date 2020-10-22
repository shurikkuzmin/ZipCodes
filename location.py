import geopy
import numpy as np
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
import json
import folium
from folium.plugins import HeatMap

def GetCoors():

    dataFrame = pandas.read_csv("zips.csv")

    geoLocator = geopy.Nominatim(user_agent = "shurik.kuzmin@gmail.com")
    geoCode = RateLimiter(geoLocator.geocode, min_delay_seconds=3)
    output = {}

    for zipCode in dataFrame.values:
        zipCode = str(zipCode[0]).strip()
        if '-' in zipCode:
            zipCode=zipCode[0:zipCode.index('-')]
        res = geoCode(zipCode+", United States of America")
        if res != None:
            if zipCode in output:
                output[zipCode]["Count"] = output[zipCode]["Count"] + 1
            else:
                output[zipCode] = {}
                output[zipCode]["Count"] = 1
                output[zipCode]["Latitude"] = res.latitude
                output[zipCode]["Longitude"] = res.longitude
            print("Processing %s" % zipCode)
    with open("coors.json", "w") as f:
        json.dump(output, f)
    return output

def LoadCoors():
    with open("coors.json", "r") as f:
        return json.load(f)
def VisualizeData(data):
    allCount = 0
    mainLongitude = 0.0
    mainLatitude = 0.0
    for zipCode in data:
        count = data[zipCode]["Count"]
        allCount = allCount + count
        mainLongitude = mainLongitude + data[zipCode]["Longitude"] * count
        mainLatitude = mainLatitude + data[zipCode]["Latitude"] * count

    mainLongitude = mainLongitude / allCount
    mainLatitude = mainLatitude / allCount
    
    locs = folium.Map(location=[mainLatitude, mainLongitude])

    for zipCode in data:
        longitude = data[zipCode]["Longitude"]
        latitude = data[zipCode]["Latitude"]
        folium.Marker([latitude, longitude],popup=zipCode,icon=folium.Icon(color="gray")).add_to(locs)
    folium.Marker([mainLatitude, mainLongitude],popup="Main Center", icon=folium.Icon(color="red")).add_to(locs)
  
    locs.save("map.html")

def VisualizeHeatMap(data):
    allCount = 0
    mainLongitude = 0.0
    mainLatitude = 0.0
    sumOrders = data["Count"].sum()
    mainLatitude = (data["Latitude"] * data["Count"]).sum() / sumOrders
    mainLongitude = (data["Longitude"] * data["Count"]).sum() / sumOrders

    #for zipCode in data:
    #    dataHeatMap.append([data[zipCode]["Latitude"], data[zipCode]["Longitude"], data[zipCode]["Count"]])
    #    count = data[zipCode]["Count"]
    #    allCount = allCount + count
    #    mainLongitude = mainLongitude + data[zipCode]["Longitude"] * count
    #    mainLatitude = mainLatitude + data[zipCode]["Latitude"] * count

    #mainLongitude = mainLongitude / allCount
    #mainLatitude = mainLatitude / allCount
    
    locs = folium.Map(location=[mainLatitude, mainLongitude])

    locsHeat = HeatMap(data=data.values, overlay=False).add_to(locs)
  
    locs.save("heatMap.html")

def LoadXLS():
    df = pd.read_excel("26Apr2020.xlsx", header=None, names=["Latitude", "Longitude", "Count"])
    
if __name__=="__main__":
    #data = GetCoors()
    #data = LoadCoors()
    data = LoadXLS()
    quit()
    #VisualizeData(data)
    VisualizeHeatMap(data)
    print(data)