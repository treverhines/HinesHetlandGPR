import numpy as np
import matplotlib.pyplot as plt
import pygeons
from matplotlib import colors

xtick_dates = ['2015-11-01','2015-12-01','2016-01-01','2016-02-01','2016-03-01']
xticks = [pygeons.mjd.mjd(i,'%Y-%m-%d') for i in xtick_dates]
xtick_labels = ['2015-11-01','2015-12-01','2016-01-01','2016-02-01','2016-03-01']

c0 = colors.to_rgb('C0')
c0t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C0')))
c1 = colors.to_rgb('C1')
c1t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C1')))
c2 = colors.to_rgb('C2')
c2t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C2')))
c3 = colors.to_rgb('C3')
c3t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C3')))

fig,ax = plt.subplots(figsize=(7,3.5))
pygeons.plot.plot._setup_ts_ax([ax])
ax.set_xticks(xticks)
ax.set_xticklabels(xtick_labels)
ax.tick_params(labelsize=10)
ax.set_xlim((57327.0,57448.0))
ax.set_ylabel('displacement [mm]')
#ax.set_ylim((-10.0,15.0))
ax.grid()

# OBSERVED
data = pygeons.io.io.dict_from_hdf5('data/data.h5')
idx = (data['id'] == 'P436').nonzero()[0][0]
lon = data['longitude'][idx]
lat = data['latitude'][idx]
t = data['time']
u = 1000*data['east'][:,idx]
us = 1000*data['east_std_dev'][:,idx]
ax.errorbar(t,u,us,marker='.',linestyle='None',color=c0,ecolor=c0t,ms=5.0,zorder=1,label='observed')

# SE
data = pygeons.io.io.dict_from_hdf5('data/se.per.fit.h5')
idx = (data['id'] == 'P436').nonzero()[0][0]
lon = data['longitude'][idx]
lat = data['latitude'][idx]
t = data['time']
u = 1000*data['east'][:,idx]
us = 1000*data['east_std_dev'][:,idx]
ax.plot(t,u,'-',color=c1,zorder=2,lw=1.5,label='SE')
ax.fill_between(t,u-us,u+us,color=c1,zorder=2,alpha=0.4)

# WEN
data = pygeons.io.io.dict_from_hdf5('data/wen12.per.fit.h5')
idx = (data['id'] == 'P436').nonzero()[0][0]
lon = data['longitude'][idx]
lat = data['latitude'][idx]
t = data['time']
u = 1000*data['east'][:,idx]
us = 1000*data['east_std_dev'][:,idx]
ax.plot(t,u,'-',color=c2,zorder=3,lw=1.5,label='Wendland')

# IBM
data = pygeons.io.io.dict_from_hdf5('data/ibm.per.fit.h5')
idx = (data['id'] == 'P436').nonzero()[0][0]
lon = data['longitude'][idx]
lat = data['latitude'][idx]
t = data['time']
u = 1000*data['east'][:,idx]
us = 1000*data['east_std_dev'][:,idx]
ax.plot(t,u,'-',color=c3,zorder=4,lw=1.5,label='IBM')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('signal-fit.pdf',format='pdf')
plt.show()

