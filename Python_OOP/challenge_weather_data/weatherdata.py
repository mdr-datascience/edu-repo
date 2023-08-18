# This file retrieves and analyses weather data from the NOAA
# Application based on Michele Vallisneri's Python Data Analysis Course

# Import relevant modules
import os
import urllib.request
import numpy as np
import functools
import pandas as pd

# Import relevant data
if not os.path.isfile('stations.txt'):
    urllib.request.urlretrieve('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt',
                               'stations.txt')
    
# parse the stations.txt file as described in video 05_02
allstations = np.genfromtxt('stations.txt', delimiter=[11,9,10,7,3,31,4,4,6],
                                            usecols=[0,1,2,3,4,5,6,7,8],
                                            names=['id','latitude','longitude','elevation','state','name','gsn','hcn','wmo'],
                                            dtype=['U11','d','d','d','U3','U31','U4','U4','U6'],
                                            autostrip=True)

def getfile(station_name):  
    
    # name of the local file
    station_file = f'{station_name}.dly'
    
    # if we don't have the file locally...
    if not os.path.isfile(station_file):
        # figure out the station id from the stations.txt file
        
        # start with all the station with names that begin as requested
        stations = allstations[np.char.find(allstations['name'], station_name) == 0]

        if len(stations) == 0:
            raise IOError("Station not available.")
        
        # we prefer GSN stations if available, then HCN, then we default to the first match
        if np.any(stations['gsn'] != ''):
            station = stations[stations['gsn'] != ''][0]
        elif np.any(stations['hcn'] != ''):
            station = stations[stations['hcn'] != ''][0]
        else:
            station = stations[0]
        
        print(f"Using {station}.")
        
        # compose the URL at which we expect to find the data
        url = f'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/{station["id"]}.dly'
        
        print(f'Downloading {url}...')
        
        # download it to the local file
        urllib.request.urlretrieve(url, station_file)
        
    return station_file

@functools.lru_cache()
def getdata(station_name):
    
    station_file = getfile(station_name)
    
    # load the fixed-width file following its definition in readme.txt
    # note that there are 31 sequences of values + flags, one of each day of the month
    # (some will be undefined for some months)
    w = np.genfromtxt(station_file,
                      delimiter=[11,4,2,4] + [5,1,1,1]*31,
                      # we will not use the daily flags, so this list becomes
                      # 0, 1, 2, 3, 4, 8, 12, 16, 20, 24...
                      usecols=[0,1,2,3] + list(range(4,4*32,4)),
                      # the names of the daily observations will be day1, day2, day3, ...
                      names=['id','year','month','element'] + [f'day{i}' for i in range(1,32)],
                      dtype=['U11','i','i','U4'] + ['d']*31,
                      autostrip=True)

    # convert the numpy record array to a pandas DataFrame, a more powerful object
    # for cleaning and restructuring data
    pw = pd.DataFrame(w)

    # "melt" the daily observations into one record per daily observation,
    # storing the column name in 'day'
    pw = pd.melt(pw, id_vars=['id','year','month','element'], var_name='day', value_name='value')
    
    # throw away null observations
    pw = pw[pw.value != -9999]

    # keep only min/max temperatures, precipitation, and snow
    pw = pw[pw.element.isin(['TMAX','TMIN'])]

    # convert 'day1', 'day2', etc. to the number of the day 
    pw['day'] = pw.day.apply(lambda x: int(x[3:]))
    
    # make a date out of year, month, day
    pw['date'] = pd.to_datetime(pw[['year','month','day']])

    # keep only data, element, and value
    pw = pw[['date','element','value']]

    # restructure the DataFrame so that different elements for the same day appear in the same row
    # (basically the opposite of melt)
    pw = pw.pivot(index='date', columns='element')['value']
    pw.columns.name = None    
    pw = pw[['TMIN','TMAX']]

    pw['TMIN'] /= 10.0
    pw['TMAX'] /= 10.0
    
    return pw

def getyear(station_name, elements, year):
 
    alldata = getdata(station_name)
    
    # select data by year, and get rid of the extra day in leap years
    # then pick out the "element" column
    yeardata = alldata[(alldata.index.year == year) & (alldata.index.dayofyear < 366)]
    
    # make an empty record array full of nans
    empty = np.full(365, np.nan, dtype=[(element, np.float64) for element in elements])
    
    # fill it with values, using day of the year (1 to 365) as index
    #empty[yeardata.index.dayofyear - 1] = yeardata.values[yeardata.index.dayofyear - 1]
    for element in elements:    
        # fill it with values, using day of the year (1 to 365) as index
        empty[element][yeardata.index.dayofyear - 1] = yeardata[element].values

    return empty

def fillnans(array):
    x = np.arange(len(array))
    good = ~np.isnan(array)
    return np.interp(x, x[good], array[good])

def data_to_plot(station, year):

    allyears = np.vstack([getyear(station, ['TMIN','TMAX'], year) for year in range(1910, 2019)])
    
    tmin_record = np.nanmin(allyears['TMIN'], axis=0)
    tmax_record = np.nanmax(allyears['TMAX'], axis=0)
    
    normal = np.vstack([getyear(station, ['TMIN','TMAX'], year) for year in range(1981, 2011)])
    
    tmin_normal = np.nanmean(normal['TMIN'], axis=0)
    tmax_normal = np.nanmean(normal['TMAX'], axis=0)
    
    thisyear = getyear(station, ['TMIN', 'TMAX'], year)
    
    days = np.arange(1, 366)
    avg = 0.5*(np.nanmean(thisyear['TMIN']) + np.nanmean(thisyear['TMAX']))

    return days, tmin_normal, tmax_normal, tmin_record, tmax_record, thisyear, avg

#pp.figure(figsize=(15,4.5))
#pp.fill_between(days, tmin_record, tmax_record, color=(0.92,0.92,0.89), step='mid')
#pp.fill_between(days, tmin_normal, tmax_normal, color=(0.78,0.72,0.72))
#
#pp.fill_between(days, thisyear['TMIN'], thisyear['TMAX'],
#                color=(0.73,0.21,0.41), alpha=0.6, step='mid')
#
#pp.axis(xmin=1, xmax=365, ymin=-15, ymax=50)
#pp.title(f'{station}, {year}: average temperature = {avg:.2f} C')
#pp.ylabel("Temperature (Celcius)")
#pp.xlabel("Day of the year")
#pp.legend(["Record temperatures", "Average temperatures", "Year temperatures"])
#pp.show()



