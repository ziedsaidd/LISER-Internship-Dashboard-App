#create dataframes based on the available data
import os
import geopandas as gpd
import json
import rasterio
import rasterstats
import pandas as pd


def generate_dataframe (shapefile, raster):
    # Read the shapefile and convert its crs 
    districts = gpd.read_file (shapefile)
    districts = districts.to_crs('epsg:4326')
    # convert it into a geoJson file
    districts.to_file("geoDist", driver = "GeoJSON")
    with open("geoDist") as geofile:
        geojson_layer = json.load(geofile)
    #concordance between the df and the geojson file based on an 'id' key
    state_id_map = {}

    for feature in geojson_layer['features']:
        feature['id'] = feature['properties']['GEN']
        state_id_map[feature['properties']['SHN']] = feature['id']
        
    districts['id']=districts['SHN'].apply(lambda x: state_id_map[x])
    # import the raster file
    rf = rasterio.open(raster, mode = 'r')
    # get the stats from the raster and the shapefile
    # Assign raster values to a numpy nd array
    polluant = rf.read(1)
    affine = rf.transform

    # Calculating the zonal statistics 
    avg_pl  = rasterstats.zonal_stats(districts, polluant, affine = affine,stats = ['mean', 'min', 'max', 'std'],geojson_out = True)

    # Extracting the average rainfall data from the list
    avg_poll = []
    i = 0

    while i < len(avg_pl):
        avg_poll.append(avg_pl[i]['properties'])
        i = i + 1 

    # Transfering the infromation from the list to a pandas DataFrame

    avg_pl_gr = pd.DataFrame(avg_poll)
    districts["mean"]=avg_pl_gr["mean"]
    districts["min"]=avg_pl_gr["min"]
    districts["max"]=avg_pl_gr["max"]
    districts["std"]=avg_pl_gr["std"]

    dataframe = districts

    return dataframe, geojson_layer

def rem_dir (saving_path, p, n):
    names = os.listdir(p)
    names= pd.DataFrame(names)
    names.to_excel("{}/{}.xlsx".format(saving_path, n), index = False)
    return

def create_csvs (path):
    zones = os.listdir(path)
    rem_dir(path, path, "ancienCountries")
    for zone in zones:
        if ".xlsx" not in zone:   
            nuts1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path,zone))
            nuts2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path,zone))
            nuts3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path,zone))
            poll = os.listdir(('{}/{}/polluant').format(path,zone))
            #
            rem_dir(('{}/{}/shapefiles/nuts1').format(path,zone),('{}/{}/shapefiles/nuts1').format(path,zone), "{}_nuts1".format(zone))
            rem_dir(('{}/{}/shapefiles/nuts2').format(path,zone),('{}/{}/shapefiles/nuts2').format(path,zone), "{}_nuts2".format(zone))
            rem_dir(('{}/{}/shapefiles/nuts3').format(path,zone),('{}/{}/shapefiles/nuts3').format(path,zone), "{}_nuts3".format(zone))
            rem_dir(('{}/{}/polluant').format(path,zone),('{}/{}/polluant').format(path,zone), "{}_polluants".format(zone))
            #
            for p in poll:
                if ".xlsx" not in p:
                    ppath = os.path.join(('{}/{}/polluant/').format(path,zone), p)
                    pelement = os.listdir(ppath)
                    rem_dir(('{}/{}/polluant/{}').format(path, zone, p),('{}/{}/polluant/{}').format(path,zone, p), "{}_polluants_{}".format(zone, p))
                    for tif in pelement:
                        if ".xlsx" not in tif:
                            part = tif.split("_")
                            year = part[1]
                            month = part [2]
                            month = month.split(".")
                            month = month[0]
                            month = str(int(month))
                            for n in [nuts1, nuts2, nuts3]:
                                
                                if n == nuts1:
                                    try:
                                        res = [i for i in n if '.shp' in i]
                                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts1/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                                        dataframe['year'] = year
                                        dataframe['month'] = month
                                        dataframe['polluant'] = p
                                        dataframe.to_excel(('./data/processedData/{}_{}_nuts1_{}_{}.xlsx').format(zone, p, year, month))
                                    except:
                                        pass
                                elif n == nuts2 :
                                    try:
                                        res = [i for i in n if '.shp' in i]
                                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts2/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                                        dataframe['year'] = year
                                        dataframe['month'] = month
                                        dataframe['polluant'] = p
                                        dataframe.to_excel(('./data/processedData/{}_{}_nuts2_{}_{}.xlsx').format(zone, p, year, month))
                                    except:
                                        pass
                                else:
                                    try:
                                        res = [i for i in n if '.shp' in i]
                                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts3/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                                        dataframe['year'] = year
                                        dataframe['month'] = month
                                        dataframe['polluant'] = p
                                        dataframe.to_excel(('./data/processedData/{}_{}_nuts3_{}_{}.xlsx').format(zone, p, year, month))
                                    except:
                                        pass
    return

def generate_from_countries (path, zone):
    '''
    This function allows the generation of csvs based on a given path and specific region
    '''
    nuts1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path,zone))
    nuts2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path,zone))
    nuts3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path,zone))
    poll = os.listdir(('{}/{}/polluant').format(path,zone))
    #
    rem_dir(('{}/{}/shapefiles/nuts1').format(path,zone),('{}/{}/shapefiles/nuts1').format(path,zone), "{}_nuts1".format(zone))
    rem_dir(('{}/{}/shapefiles/nuts2').format(path,zone),('{}/{}/shapefiles/nuts2').format(path,zone), "{}_nuts2".format(zone))
    rem_dir(('{}/{}/shapefiles/nuts3').format(path,zone),('{}/{}/shapefiles/nuts3').format(path,zone), "{}_nuts3".format(zone))
    rem_dir(('{}/{}/polluant').format(path,zone),('{}/{}/polluant').format(path,zone), "{}_polluants".format(zone))
    #
    for p in poll:
        ppath = os.path.join(('{}/{}/polluant/').format(path,zone), p)
        pelement = os.listdir(ppath)
        rem_dir(('{}/{}/polluant/{}').format(path, zone, p),('{}/{}/polluant/{}').format(path,zone, p), "{}_polluants_{}".format(zone, p))
        for tif in pelement:
            if ".xlsx" not in tif:
                part = tif.split("_")
                year = part[1]
                month = part [2]
                month = month.split(".")
                month = month[0]
                month = str(int(month))
                for n in [nuts1, nuts2, nuts3]:           
                    if n == nuts1:
                        try:
                            res = [i for i in n if '.shp' in i]
                            dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts1/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                            dataframe['year'] = year
                            dataframe['month'] = month
                            dataframe['polluant'] = p
                            dataframe.to_excel(('./data/processedData/{}_{}_nuts1_{}_{}.xlsx').format(zone, p, year, month))
                        except:
                            pass
                    elif n == nuts2 :
                        try:
                            res = [i for i in n if '.shp' in i]
                            dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts2/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                            dataframe['year'] = year
                            dataframe['month'] = month
                            dataframe['polluant'] = p
                            dataframe.to_excel(('./data/processedData/{}_{}_nuts2_{}_{}.xlsx').format(zone, p, year, month))
                        except:
                            pass
                    else:
                        try:
                            res = [i for i in n if '.shp' in i]
                            dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts3/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                            dataframe['year'] = year
                            dataframe['month'] = month
                            dataframe['polluant'] = p
                            dataframe.to_excel(('./data/processedData/{}_{}_nuts3_{}_{}.xlsx').format(zone, p, year, month))
                        except:
                            pass
    return

def generate_from_polluant (path, zone, polluant):
    pelement = os.listdir(('{}/{}/polluant/{}').format(path, zone, polluant))
    nuts1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path,zone))
    nuts2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path,zone))
    nuts3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path,zone))
    for tif in pelement:
        if ".xlsx" not in tif:
            part = tif.split("_")
            year = part[1]
            month = part [2]
            month = month.split(".")
            month = month[0]
            month = str(int(month))           
            for n in [nuts1, nuts2, nuts3]:           
                if n == nuts1:
                    try:
                        res = [i for i in n if '.shp' in i]
                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts1/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, polluant, tif))
                        dataframe['year'] = year
                        dataframe['month'] = month
                        dataframe['polluant'] = polluant
                        dataframe.to_excel(('./data/processedData/{}_{}_nuts1_{}_{}.xlsx').format(zone, polluant, year, month))
                    except:
                        pass
                elif n == nuts2 :
                    try:
                        res = [i for i in n if '.shp' in i]
                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts2/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, polluant, tif))
                        dataframe['year'] = year
                        dataframe['month'] = month
                        dataframe['polluant'] = polluant
                        dataframe.to_excel(('./data/processedData/{}_{}_nuts2_{}_{}.xlsx').format(zone, polluant, year, month))
                    except:
                        pass
                else:
                    try:
                        res = [i for i in n if '.shp' in i]
                        dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts3/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, polluant, tif))
                        dataframe['year'] = year
                        dataframe['month'] = month
                        dataframe['polluant'] = polluant
                        dataframe.to_excel(('./data/processedData/{}_{}_nuts3_{}_{}.xlsx').format(zone, polluant, year, month))
                    except:
                        pass
    return

def generate_from_nuts (n, path, zone, nutfile):
    poll = os.listdir(('{}/{}/polluant').format(path,zone))  
    for p in poll:
        ppath = os.path.join(('{}/{}/polluant/').format(path,zone), p)
        pelement = os.listdir(ppath)
        for tif in pelement:
            if ".xlsx" not in tif:
                part = tif.split("_")
                year = part[1]
                month = part [2]
                month = month.split(".")
                month = month[0]
                month = str(int(month))
                try:
                    dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/{}/{}').format(path, zone, n,  nutfile), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                    dataframe['year'] = year
                    dataframe['month'] = month
                    dataframe['polluant'] = p
                    dataframe.to_excel(('./data/processedData/{}_{}_{}_{}_{}.xlsx').format(zone, p, n, year, month))
                except:
                    pass

    return

def generate_from_tif (path, zone , p,  tif):
    nuts1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path,zone))
    nuts2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path,zone))
    nuts3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path,zone))
    part = tif.split("_")
    year = part[1]
    month = part [2]
    month = month.split(".")
    month = month[0]
    month = str(int(month))
    for n in [nuts1, nuts2, nuts3]:           
        if n == nuts1:
            try:
                res = [i for i in n if '.shp' in i]
                dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts1/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                dataframe['year'] = year
                dataframe['month'] = month
                dataframe['polluant'] = p
                dataframe.to_excel(('./data/processedData/{}_{}_nuts1_{}_{}.xlsx').format(zone, p, year, month))
            except:
                pass
        elif n == nuts2 :
            try:
                res = [i for i in n if '.shp' in i]
                dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts2/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                dataframe['year'] = year
                dataframe['month'] = month
                dataframe['polluant'] = p
                dataframe.to_excel(('./data/processedData/{}_{}_nuts2_{}_{}.xlsx').format(zone, p, year, month))
            except:
                pass
        else:
            try:
                res = [i for i in n if '.shp' in i]
                dataframe, jsonfile = generate_dataframe(('{}/{}/shapefiles/nuts3/{}').format(path, zone, res[0]), ('{}/{}/polluant/{}/{}').format(path, zone, p, tif))
                dataframe['year'] = year
                dataframe['month'] = month
                dataframe['polluant'] = p
                dataframe.to_excel(('./data/processedData/{}_{}_nuts3_{}_{}.xlsx').format(zone, p, year, month))
            except:
                pass

    return 

def check_new_countries (path):
    '''
    This function allow us to check the countries directory and generate csvs from newly added regions
    '''
    zones = os.listdir(path)
    ancien = pd.read_excel("./data/rawData/ancienCountries.xlsx")
    lis = ancien[0].tolist()
    new = []
    for zone in zones:
        if ".xlsx" not in zone:
            if zone not in lis:
                new.append(zone)

    if len(new) != 0:
        number_new_docs = len(new)
        print ("there is {} new regions added".format(number_new_docs))
        for i in new:
            if ".xlsx" not in i:
                try:
                    generate_from_countries(path,i)
                except:
                    pass
                lis = lis + new
                liste=pd.DataFrame(lis)
                liste.to_excel("{}/ancienCountries.xlsx".format(path), index = False)
    return

def check_new_polluants(path):
    '''
    This fuction allows us to check polluants directory of each area 
    and generates csvs from a newly added ones
    '''
    zones = os.listdir(path)
    for zone in zones:
        if ".xlsx" not in zone:
            poll = os.listdir(('{}/{}/polluant').format(path,zone))
            ancien = pd.read_excel("./data/rawData/{}/polluant/{}_polluants.xlsx".format(zone, zone))
            lis = ancien[0].tolist()
            new = []
            for p in poll:
                if p not in lis:
                    if ".xlsx" not in p:
                        new.append(p)

            if len(new) != 0:
                print(new)
                number_new_poll = len(new)
                print ("there is {} new polluant added for the zone {}".format(number_new_poll, zone))
                for i in new:
                    if ".xlsx" not in i:
                        try:
                            generate_from_polluant(path, zone, i)
                        except:
                            pass
                        lis = lis + new
                        liste=pd.DataFrame(lis)
                        liste.to_excel("{}/{}/polluant/{}_polluants.xlsx".format(path, zone, zone), index = False)
    return
    

def check_new_nuts (path):
    zones = os.listdir(path)
    for zone in zones:
        if ".xlsx" not in zone:
            n1 = os.listdir(('{}/{}/shapefiles/nuts1').format(path,zone))
            an1 = pd.read_excel("{}/{}/shapefiles/nuts1/{}_nuts1.xlsx".format(path,zone,zone))
            if an1.empty == False:
                lis1 = an1[0].tolist()
                new1 = []
            n2 = os.listdir(('{}/{}/shapefiles/nuts2').format(path,zone))
            an2 = pd.read_excel("{}/{}/shapefiles/nuts2/{}_nuts2.xlsx".format(path,zone,zone))
            if an2.empty == False:
                lis2 = an2[0].tolist()
                new2 = []
            n3 = os.listdir(('{}/{}/shapefiles/nuts3').format(path,zone))
            an3 = pd.read_excel("{}/{}/shapefiles/nuts3/{}_nuts3.xlsx".format(path,zone,zone))
            if an3.empty == False:
                lis3 = an3[0].tolist()
                new3 = []
            try:    
                for n in n1:
                    if n not in lis1:
                        new1.append(n)
                for n in n2:
                    if n not in lis2:
                        new2.append(n)
                for n in n3:
                    if n not in lis3:
                        new3.append(n)

                number_new_nuts1 = len(new1)
                number_new_nuts2 = len(new2)
                number_new_nuts3 = len(new3)
                print ("there is {} new nuts1 file added for the zone {}".format(number_new_nuts1, zone))
                print ("there is {} new nuts2 file added for the zone {}".format(number_new_nuts2, zone))
                print ("there is {} new nuts3 file added for the zone {}".format(number_new_nuts3, zone))

                if len(new1) != 0:
                    for i in new1:
                        if ".shp" in i:
                            try:
                                generate_from_nuts("nuts1", path, zone, i)
                            except:
                                pass
                            lis1 = lis1 + new1
                            liste1=pd.DataFrame(lis1)
                            liste1.to_excel("{}/{}/shapefiles/nuts1/{}_nuts1.xlsx".format(path, zone, zone), index = False)

                if len(new2) != 0:
                    for i in new2:
                        if ".shp" in i:
                            try:
                                generate_from_nuts("nuts2", path, zone, i)
                            except:
                                pass
                            lis2 = lis2 + new2
                            liste2 = pd.DataFrame(lis2)
                            liste2.to_excel("{}/{}/shapefiles/nuts2/{}_nuts2.xlsx".format(path, zone, zone), index = False)

                if len(new3) != 0:
                    for i in new3:
                        if ".shp" in i:
                            try:
                                generate_from_nuts("nuts3", path, zone, i)
                            except:
                                pass
                            lis3 = lis3 + new3
                            liste3 = pd.DataFrame(lis3)
                            liste3.to_excel("{}/{}/shapefiles/nuts3/{}_nuts3.xlsx".format(path, zone, zone), index = False)
            except:
                pass

    return

def check_new_tif (path):
    #try:
    zones = os.listdir(path)
    for zone in zones:
        if ".xlsx" not in zone:
            poll = os.listdir(('{}/{}/polluant').format(path,zone))
            for p in poll:
                if ".xlsx" not in p:
                    ppath = os.path.join(('{}/{}/polluant/').format(path,zone), p)
                    pelement = os.listdir(ppath)
                    ancienpelement = pd.read_excel("{}/{}/polluant/{}/{}_polluants_{}.xlsx".format(path, zone, p, zone, p))
                    if ancienpelement.empty == False:
                        lis = ancienpelement[0].tolist()
                        new = []
                    try:
                        for n in pelement:
                            if n not in lis:
                                new.append(n)   
                        new_tif = len(new)
                        print ("there is {} new tif file added for the zone {} and the polluant {}".format(new_tif, zone, p))
                        if len(new) != 0:
                            for i in new:       
                                if ".xlsx" not in i:
                                    try:
                                        generate_from_tif(path, zone, p, i)
                                    except:
                                        pass
                                    lis = lis + new
                                    liste = pd.DataFrame(lis)
                                    liste.to_excel("{}/{}/polluant/{}/{}_polluants_{}.xlsx".format(path, zone, p, zone, p), index = False)
                    
                    except:
                        pass
                    new = []
    #except:
    #    pass
    return 

path = './data/rawData'
processedFilesDir = "./data/processedData"
procD = os.listdir(processedFilesDir)
if len(procD) == 0 :
    create_csvs(path)
    print("I am creating files for the first time)")   
else:
    check_new_countries(path)
    print("I checked new countries")
    check_new_nuts(path)
    print("I checked new nuts")
    check_new_polluants(path)
    print("I checked new polluants")
    check_new_tif(path)
    print("I checked new tifs")