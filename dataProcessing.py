# create dataframes based on the available data
import json
import os

import geopandas as gpd
import pandas as pd
import rasterio
import rasterstats

import get_variable_name


def generate_dataframe(shapefile, raster):
    # Read the shapefile and convert its crs
    districts = gpd.read_file(shapefile)
    districts = districts.to_crs('epsg:4326')

    # convert it into a geoJson file
    districts.to_file("geoDist", driver="GeoJSON")
    with open("geoDist", encoding="Latin-1") as geofile:
        geojson_layer = json.load(geofile)

    # concordance between the df and the geojson file based on an 'id' key
    state_id_map = {}

    for feature in geojson_layer['features']:
        feature['id'] = feature['properties']['GEN']
        state_id_map[feature['properties']['SHN']] = feature['id']

    districts['id'] = districts['SHN'].apply(lambda x: state_id_map[x])

    # import the raster file
    rf = rasterio.open(raster, mode='r')

    # get the stats from the raster and the shapefile
    # Assign raster values to a numpy nd array
    polluant = rf.read(1)
    affine = rf.transform

    # Calculating the zonal statistics
    avg_pl = rasterstats.zonal_stats(districts, polluant, affine=affine, stats=[
                                     'mean', 'min', 'max', 'std'], geojson_out=True)

    # Extracting the average rainfall data from the list
    avg_poll = []
    i = 0

    while i < len(avg_pl):
        avg_poll.append(avg_pl[i]['properties'])
        i = i + 1

    # Transfering the infromation from the list to a pandas DataFrame
    avg_pl_gr = pd.DataFrame(avg_poll)
    districts["mean"] = avg_pl_gr["mean"]
    districts["min"] = avg_pl_gr["min"]
    districts["max"] = avg_pl_gr["max"]
    districts["std"] = avg_pl_gr["std"]

    dataframe = districts

    return dataframe, geojson_layer


path = './data/rawData'
zones = os.listdir(path)

for zone in zones:
    shapedir = os.listdir(('{}/{}/shapefiles').format(path, zone))
    nuts1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path, zone))
    nuts2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path, zone))
    nuts3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path, zone))
    no2 = os.listdir(('{}/{}/pollutionNO2/').format(path, zone))

    for tif in no2:
        part = tif.split("_")
        year = part[1]
        month = part[2]
        month = month.split(".")
        month = month[0]
        for n in [nuts1, nuts2, nuts3]:

            if n == nuts1:
                try:
                    res = [i for i in n if '.shp' in i]
                    dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts1/{}').format(
                        path, zone, res[0]), ('{}/{}/pollutionNO2/{}').format(path, zone, tif))
                    dataframe['year'] = year
                    dataframe['month'] = month
                    dataframe['polluant'] = 'no2'
                    dataframe.to_csv(
                        ('{}_no2_nuts1_{}_{}.csv').format(zone, year, month))
                except:
                    pass
            elif n == nuts2:
                try:
                    res = [i for i in n if '.shp' in i]
                    dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts2/{}').format(
                        path, zone, res[0]), ('{}/{}/pollutionNO2/{}').format(path, zone, tif))
                    dataframe['year'] = year
                    dataframe['month'] = month
                    dataframe['polluant'] = 'no2'
                    dataframe.to_csv(
                        ('{}_no2_nuts2_{}_{}.csv').format(zone, year, month))
                except:
                    pass
            else:
                try:
                    res = [i for i in n if '.shp' in i]
                    dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts3/{}').format(
                        path, zone, res[0]), ('{}/{}/pollutionNO2/{}').format(path, zone, tif))
                    dataframe['year'] = year
                    dataframe['month'] = month
                    dataframe['polluant'] = 'no2'
                    dataframe.to_csv(
                        ('{}_no2_nuts3_{}_{}.csv').format(zone, year, month))
                except:
                    pass

            # except:
            #    pass
