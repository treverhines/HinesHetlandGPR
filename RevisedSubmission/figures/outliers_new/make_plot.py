import numpy as np
import matplotlib.pyplot as plt
import pygeons
from matplotlib import colors
import rbf
import logging
logging.basicConfig(level=logging.DEBUG)

def trend(u1,t1):
  idx = np.isfinite(u1)
  u2 = u1[idx]
  t2 = t1[idx]
  G = np.array([np.ones(t2.shape[0]),t2]).T
  m = np.linalg.pinv(G.T.dot(G)).dot(G.T).dot(u2)
  return m
  
xtick_dates = ['2011-01-01','2012-01-01','2013-01-01','2014-01-01']
xticks = [pygeons.mjd.mjd(i,'%Y-%m-%d') for i in xtick_dates]
xtick_labels = ['2011-01-01','2012-01-01','2013-01-01','2014-01-01']
# start and end time in MJD
xmin,xmax = 55378.0,56839.0

c1 = colors.to_rgb('C0')
c1t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C0')))
c2 = colors.to_rgb('C1')
c2t = tuple(0.6 + 0.4*np.array(colors.to_rgb('C1')))

# plot raw data

data = pygeons.io.io.dict_from_hdf5('data-2017-05-17.h5')

name = 'SC03'
idx = (data['id'] == name).nonzero()[0][0]
lon = data['longitude'][idx]
lat = data['latitude'][idx]

t = data['time']
u = 1000*data['east'][:,idx]
us = 1000*data['east_std_dev'][:,idx]

# toss out times that are out of range or have missing data
tidx = (t >= xmin) & (t <= xmax) & np.isfinite(u)

fig,axs = plt.subplots(2,1,figsize=(7,4.5),sharex=True)
pygeons.plot.plot._setup_ts_ax(axs)

axs[0].set_xticks(xticks)
axs[0].set_xticklabels(xtick_labels)
axs[0].tick_params(labelsize=10)
axs[0].set_xlim((xmin,xmax))
axs[0].set_ylim((-10.0,15.0))
axs[0].grid()

axs[1].set_xticks(xticks)
axs[1].set_xticklabels(xtick_labels)
axs[1].tick_params(labelsize=10)
axs[1].set_xlim((xmin,xmax))
axs[1].set_ylim((-10.0,15.0))
axs[1].grid()

t = t[tidx]
u = u[tidx]
us = us[tidx]

# detrend for viewing ease
m = trend(u,t)
u = u - m[0] - m[1]*t

# identify outliers!
def basis(t):
  return np.array([t[:,0]**0,
                   t[:,0]**1,
                   np.sin(2*np.pi*t[:,0]/365.25),
                   np.cos(2*np.pi*t[:,0]/365.25),
                   np.sin(4*np.pi*t[:,0]/365.25),
                   np.cos(4*np.pi*t[:,0]/365.25)]).T
                   
# parameters
tol = 2.5

# using just basis functions
gp = rbf.gauss.gpbfci(basis)

# find outliers
is_outlier = gp.outliers(t[:,None],u,us,tol=tol)

# find the best fit with non-outliers
fit = gp.condition(t[~is_outlier,None],
                   u[~is_outlier],
                   us[~is_outlier]).mean(t[:,None])

axs[0].text(0.02,0.85,'A',fontsize=16,transform=axs[0].transAxes)
axs[0].errorbar(t,u,us,marker='.',linestyle='None',color=c1,ecolor=c1t,ms=4.99,zorder=1)
axs[0].errorbar(t[is_outlier],
                u[is_outlier],
                us[is_outlier],
                marker='.',linestyle='None',color=c2,ecolor=c2t,ms=5.0,zorder=2)
axs[0].plot(t,fit,'C1-',zorder=3)


# using basis functions and GPSE
gp = rbf.gauss.gpbfci(basis)
# SE with 10 day timescale
gp += rbf.gauss.gpiso(rbf.basis.se,(0.0,1.0,0.027*365.25))

# find outliers
is_outlier = gp.outliers(t[:,None],u,us,tol=tol)
# find the best fit with non-outliers
fit = gp.condition(t[~is_outlier,None],
                   u[~is_outlier],
                   sigma=us[~is_outlier]).mean(t[:,None])

axs[1].text(0.02,0.85,'B',fontsize=16,transform=axs[1].transAxes)
axs[1].errorbar(t,u,us,marker='.',linestyle='None',color=c1,ecolor=c1t,ms=4.99,zorder=1)
axs[1].errorbar(t[is_outlier],
                u[is_outlier],
                us[is_outlier],
                marker='.',linestyle='None',color=c2,ecolor=c2t,ms=5.0,zorder=2)
axs[1].plot(t,fit,'C1-',zorder=3)

axs[0].set_title('station %s (%.1f$^\mathregular{\circ}$W, %.1f$^\mathregular{\circ}$N)' % 
                 (name,-lon,lat),fontsize=10)

axs[0].set_ylabel('easting [mm]',fontsize=10)
axs[1].set_ylabel('easting [mm]',fontsize=10)
fig.tight_layout()
plt.savefig('outliers.pdf',format='pdf')
plt.show()

 
