# data_try_1 is Brett's first attempt at creating a netCDF file 
# using data from one of Daniel Lecoanet's simulations

# last edited 01/27/18 by Brett McKim

import pickle
import numpy as np
import netCDF4 as nc4
import time as time_mod

# get data from Daniel
inputFile = open('./data_10_2.pkl','rb')

simdata = pickle.load(inputFile)
inputFile.close()

# organize data from simulation (256x256x512)
x_pos = simdata['x'] # 256x1
y_pos = simdata['y'] # 256x1
z_pos = simdata['z'] # 512x1
u_vel = simdata['u'] # 256x256x512
v_vel = simdata['v'] # 256x256x512
w_vel = simdata['w'] # 256x256x512
rho_dens = simdata['rho'] # 256x256x512
times = simdata['t'] # no dimensions

# create a dataset
f = nc4.Dataset('simdata.nc','w', format='NETCDF4')
grp = f.createGroup('Sim_data')

# specify dimensions
grp.createDimension('lon',len(x_pos))
grp.createDimension('lat',len(y_pos))
grp.createDimension('height',len(z_pos))
grp.createDimension('x_vel',len(u_vel))
grp.createDimension('y_vel',len(v_vel))
grp.createDimension('z_vel',len(w_vel))
grp.createDimension('density',len(rho_dens))
grp.createDimension('time', None)

# build variables
x = grp.createVariable('x_position','f4',('lon',))
y = grp.createVariable('y_position','f4',('lat',))
z = grp.createVariable('z_position','f4',('height',))
u = grp.createVariable('u_velocity','f4',('time','lon','lat','height',))
v = grp.createVariable('v_velocity','f4',('time','lon','lat','height',))
w = grp.createVariable('w_velocity','f4',('time','lon','lat','height',))
rho = grp.createVariable('density_pert','f4',('time','lon','lat','height',))
t = grp.createVariable('times','f4','time')

# pass data into variable
x[:] = x_pos
y[:] = y_pos
z[:] = z_pos
u[0,:,:,:] = u_vel
v[0,:,:,:] = v_vel
w[0,:,:,:] = w_vel
rho[0,:,:,:] = rho_dens
t[0] = times

# global attributes
f.description = 'Dataset from first convection simulation'
f.history = 'Create ' + time_mod.ctime(time_mod.time())

# local attributes
x.units = 'meters?'
y.units = 'meters?'
z.units = 'meters?'
u.units = 'meters/sec?'
v.units = 'meters/sec?'
w.units = 'meters/sec?'
t.units = 'sec?'
rho.units = 'kg/meters^3?'

f.close()