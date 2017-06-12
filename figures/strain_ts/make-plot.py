import numpy as np
import pygeons
import matplotlib.pyplot as plt
import h5py
from mpl_toolkits.basemap import Basemap
from pygeons.plot.plot import _setup_ts_ax
import rbf
import sympy

# Parameters
station = 'I0049'
radius = 150000.0

r,eps = rbf.basis.get_r(),rbf.basis.get_eps()
expr = 1.0/sympy.sqrt((2*sympy.pi)*eps**2)*sympy.exp(-r**2/(2*eps**2))
normal1d = rbf.basis.RBF(expr)

bm = Basemap(projection='tmerc',
          resolution='i',
          lon_0 = -123.0,lat_0 = 45.0,
          llcrnrlon = -127.5,llcrnrlat = 45.5,
          urcrnrlon = -120.0,urcrnrlat = 50.0)
                                        
start_day = pygeons.mjd.mjd('2010-01-01','%Y-%m-%d')
end_day = pygeons.mjd.mjd('2017-05-15','%Y-%m-%d')
total_days = end_day - start_day
xtick_dates = ['2010-01-01','2011-01-01','2012-01-01','2013-01-01','2014-01-01','2015-01-01','2016-01-01','2017-01-01']
xticks = [pygeons.mjd.mjd(i,'%Y-%m-%d') for i in xtick_dates]
xtick_labels = [' ','2011-01-01',' ','2013-01-01',' ','2015-01-01',' ','2017-01-01']

fdx = h5py.File('merged.dudx.h5')
fdy = h5py.File('merged.dudy.h5')
time = fdx['time'][...]
tidx = np.nonzero((time > start_day) & (time < end_day))[0]
time = time[tidx]

xidx = np.nonzero(fdx['id'][...] == station)[0][0]
sta_lon = fdx['longitude'][xidx]
sta_lat = fdx['latitude'][xidx]
sta_x,sta_y = bm(sta_lon,sta_lat)
print(sta_lon)
print(sta_lat)

# convert to microstrain/year
dudx = fdx['east'][tidx,xidx] * 1.0e6 * 365.25
dudx_std = fdx['east_std_dev'][tidx,xidx] * 1.0e6 * 365.25
dudy = fdy['east'][tidx,xidx] * 1.0e6 * 365.25
dudy_std = fdy['east_std_dev'][tidx,xidx] * 1.0e6 * 365.25
dvdx = fdx['north'][tidx,xidx] * 1.0e6 * 365.25
dvdx_std = fdx['north_std_dev'][tidx,xidx] * 1.0e6 * 365.25
dvdy = fdy['north'][tidx,xidx] * 1.0e6 * 365.25
dvdy_std = fdy['north_std_dev'][tidx,xidx] * 1.0e6 * 365.25
# calculate strain
exx = dudx
exx_std = dudx_std
eyy = dvdy
eyy_std = dvdy_std
exy = 0.5*(dudy + dvdx)
exy_std = 0.5*np.sqrt(dudy_std**2 + dvdx_std**2)
mag = np.sqrt(exx**2 + eyy**2 + 2*exy**2)
mag_std = np.sqrt((exx_std*exx/mag)**2 + (eyy_std*eyy/mag)**2 + (exy_std*2*exy/mag)**2)


fig,axs = plt.subplots(3,1,sharex=True,figsize=(7,5))
_setup_ts_ax(axs)
axs[0].plot(time,exx,'C0-',lw=1.5,zorder=2)
axs[0].fill_between(time,exx-exx_std,exx+exx_std,edgecolor='none',facecolor='C0',alpha=0.4,zorder=2)
axs[0].grid()
axs[0].set_ylabel('east normal\n[$\mathregular{\mu}$strain/yr]',fontsize=10)

axs[1].plot(time,eyy,'C0-',lw=1.5,zorder=2)
axs[1].fill_between(time,eyy-eyy_std,eyy+eyy_std,edgecolor='none',facecolor='C0',alpha=0.4,zorder=2)
axs[1].grid()
axs[1].set_ylabel('north normal\n[$\mathregular{\mu}$strain/yr]',fontsize=10)

axs[2].plot(time,exy,'C0-',lw=1.5,zorder=2)
axs[2].fill_between(time,exy-exy_std,exy+exy_std,edgecolor='none',facecolor='C0',alpha=0.4,zorder=2)
axs[2].grid()
axs[2].set_ylabel('east-north shear\n[$\mathregular{\mu}$strain/yr]',fontsize=10)


axs[2].set_xticks(xticks)
axs[2].set_xticklabels(xtick_labels) 
axs[2].tick_params(labelsize=10)
axs[2].set_xlim(start_day,end_day)

fig.tight_layout()
plt.savefig('strain-ts.pdf',fmt='pdf')

fig,axs = plt.subplots(2,1,sharex=True,figsize=(7,4))
_setup_ts_ax(axs)
axs[0].fill_between(time,mag/mag_std,0,color='C0',zorder=2)
axs[0].grid()
axs[0].set_ylabel('normalized strain rate\nmagnitude',fontsize=10)
axs[0].set_ylim((0,8.5))

# LOAD IN TREMORS
data = np.loadtxt('08_01_2009_05_22_2017.txt',skiprows=16,dtype=str)
tremor_dates = data[:,0]
tremor_times = np.array([pygeons.mjd.mjd(i,'%Y-%m-%d') for i in tremor_dates])
tremor_lons = data[:,3].astype(float)
tremor_lats = data[:,2].astype(float)
tremor_x,tremor_y = bm(tremor_lons,tremor_lats)
sidx = np.sqrt((tremor_x - sta_x)**2 + (tremor_y - sta_y)**2) < radius
tremor_times = tremor_times[sidx]
density = np.sum(normal1d(time[:,None],tremor_times[:,None],eps=1.0),axis=1)
#axs[1].hist(tremor_times,range(start_day,end_day))
axs[1].fill_between(time,density,0,color='C1',zorder=2)
axs[1].grid()
axs[1].set_ylabel('tremors per day',fontsize=10)
axs[1].set_ylim((0,700.0))
axs[1].set_xticks(xticks)
axs[1].set_xticklabels(xtick_labels)
axs[1].tick_params(labelsize=10)
axs[1].set_xlim(start_day,end_day)
plt.savefig('mag-ts.pdf',fmt='pdf')

fig.tight_layout()
plt.show()


