import numpy as np
import matplotlib.pyplot as plt
import pygeons
from matplotlib import colors

xtick_dates = ['2015-12-01','2016-02-01']
xticks = [pygeons.mjd.mjd(i,'%Y-%m-%d') for i in xtick_dates]
xtick_labels = ['2015-12-01','2016-02-01']

c0 = colors.to_rgb('C0')
c0t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C0')))

fig,axs = plt.subplots(3,1,figsize=(4,6),sharex=True)
pygeons.plot.plot._setup_ts_ax(axs)
for i,name in enumerate(['SC02','ALBH','P436']):
  axs[i].set_xticks(xticks)
  axs[i].set_xticklabels(xtick_labels)
  axs[i].tick_params(labelsize=10)
  axs[i].set_xlim((57327.0,57448.0))
  axs[i].set_ylabel('easting [mm]')
  #axs[i].set_ylim((-10.0,15.0))
  axs[i].grid()
  
  # OBSERVED
  data = pygeons.io.io.dict_from_hdf5('data/data.h5')
  idx = (data['id'] == name).nonzero()[0][0]
  lon = data['longitude'][idx]
  lat = data['latitude'][idx]
  t = data['time']
  u = 1000*data['east'][:,idx]
  u -= np.mean(u)
  us = 1000*data['east_std_dev'][:,idx]
  
  axs[i].set_title('station %s' %
              (name,),fontsize=10)
  
  axs[i].errorbar(t,u,us,marker='.',linestyle='None',color=c0,ecolor=c0t,ms=5.0,zorder=1,label='observed')

plt.tight_layout()
#plt.savefig('signal-fit.pdf',format='pdf')
plt.show()
  
  
