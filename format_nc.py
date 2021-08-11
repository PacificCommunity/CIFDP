## -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 22:52:48 2021

@author: Sachindra Singh, herve damlamian
"""

from netCDF4 import Dataset    
import numpy as np
import datetime as dt
from netCDF4 import date2num, num2date
import sys, getopt

def argparse(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('format_nc.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('format_nc.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   return inputfile,outputfile


infile,outfile=argparse(sys.argv[1:])
in_nc = Dataset(infile)

out_nc = Dataset(outfile, 'w', format='NETCDF4_CLASSIC', diskless=False)

#grid - 3 degree spacing in x and y
#y = np.arange(176.73, 178.87, 0.003)
#x = np.arange(-19.33, -17.73, 0.003)

#dimensions
lat_dim = out_nc.createDimension('lat', in_nc.dimensions['lat'].size) # latitude axis
lon_dim = out_nc.createDimension('lon', in_nc.dimensions['lon'].size) # longitude axis
time_dim = out_nc.createDimension('time', None) # unlimited axis (can be appended to).

#variables
lat = out_nc.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon = out_nc.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
time = out_nc.createVariable('time', np.float64, ('time',))
time.long_name = 'time'

#time population
temp=infile.split('_')
year=int(temp[2].split('-')[0])
month=int(temp[2].split('-')[1])
day=int(temp[2].split('-')[2].split('T')[0])
hr=int(temp[2].split('-')[2].split('T')[1])
start = dt.datetime(year, month, day, hr, 0, 0, 0) #define start date
#h=int(temp[3].split('.')[0])
times = np.array([start])
time.units = 'hours since {:%Y-%m-%d 00:00}'.format(times[0])
time_vals = date2num(times, time.units) 
time[:] = time_vals
time.axis = 'T' 
time.standard_name = 'time'  
time.long_name = 'time'  

#coordinate population
nlats = len(lat_dim); nlons = len(lon_dim); ntimes = times.size
#lat[:] = -90. + (180./nlats)*np.arange(nlats) 
#lon[:] = (180./nlats)*np.arange(nlons) 
lat[:] = in_nc['lat'][:]
lon[:] = in_nc['lon'][:]

# Define a 3D variable to hold the data
var_z = out_nc.createVariable('z',np.float64,('time','lat','lon'))
var_z.units = 'm' 
var_z.long_name = 'FlowDepth' 
var_z.coordinates = 'lon lat'

var_z[0,:,:] = in_nc['z'][:]

#CF attributes metadata 
out_nc.Conventions = 'CF-1.7'
out_nc.title = 'CIFDP Forecast Model Runup_'+temp[1]
out_nc.institution = 'Pacific Community (SPC)'
out_nc.source = 'CIFDP'
out_nc.history = str(dt.datetime.utcnow()) + ' Python'
out_nc.references = 'SPC'
out_nc.comment = 'Coastal Inundation Forecasting Demonstration Project Fiji'

out_nc.close()
in_nc.close()
print("Finished.")