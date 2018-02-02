# hdf5-netcdf is Brett's first attempt at creating a netCDF file 
# using data from one of Daniel Lecoanet's simulations

# last edited 02/02/18 by Brett McKim

import pickle
import netCDF4 as nc4
import time as time_mod

# get data from Daniel
inputFile = open('./data_10_2.pkl','rb')
data = pickle.load(inputFile)
inputFile.close()

# print(simdata['t'].shape) # useful for figuring out dimensions

# organize data from simulation (256x256x512)
x_pos = data['x'] # 256x1
y_pos = data['y'] # 256x1
z_pos = data['z'] # 512x1
u_vel = data['u'] # 256x256x512
v_vel = data['v'] # 256x256x512
w_vel = data['w'] # 256x256x512
rho_dens = data['rho'] # 256x256x512
times = data['t'] # 1x1

# create a dataset
f = nc4.Dataset('simdata.nc','w', format='NETCDF4')
# grp = f.createGroup('Sim_data') # I don't think we need this line anymore

# specify dimensions
f.createDimension('x',len(x_pos))
f.createDimension('y',len(y_pos))
f.createDimension('z',len(z_pos))
f.createDimension('time', None)

# build variables
x = f.createVariable('x','f8',('x',))
y = f.createVariable('y','f8',('y',))
z = f.createVariable('z','f8',('z',))
u = f.createVariable('u','f8',('time','x','y','z',))
v = f.createVariable('v','f8',('time','x','y','z',))
w = f.createVariable('w','f8',('time','x','y','z',))
rho = f.createVariable('rho','f8',('time','x','y','z',))
t = f.createVariable('t','f8','time')

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
f.title = ''
f.description = 'one time snapshot of data from an atmospheric convection simulation'
f.history = 'created ' + time_mod.ctime(time_mod.time())

# local attributes
x.units = 'unitless'
y.units = 'unitless'
z.units = 'unitless'
u.units = 'unitless'
v.units = 'unitless'
w.units = 'unitless'
t.units = 'unitless'
rho.units = 'unitless'
rho.long_name = 'mean density'

f.close()