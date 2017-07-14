#!/usr/bin/env python
import numpy as np
from pygeons.io.parser import _get_field
from pygeons.main.gpstation import fogm
import os
import matplotlib.pyplot as plt
np.random.seed(0)

def iqr(x):
  return np.subtract(*np.percentile(x,[75.0,25.0]))

def get_meridians_and_parallels(bm,ticks):
  ''' 
  returns the meridians and parallels that should be plotted.
  '''
  diff_lon = (bm.urcrnrlon-bm.llcrnrlon)
  round_digit = int(np.ceil(np.log10(ticks/diff_lon)))
  dlon = np.round(diff_lon/ticks,round_digit)

  diff_lat = (bm.urcrnrlat-bm.llcrnrlat)
  round_digit = int(np.ceil(np.log10(ticks/diff_lat)))
  dlat = np.round(diff_lat/ticks,round_digit)

  meridians = np.arange(np.floor(bm.llcrnrlon),
                        np.ceil(bm.urcrnrlon),dlon)
  parallels = np.arange(np.floor(bm.llcrnrlat),
                        np.ceil(bm.urcrnrlat),dlat)

  return meridians,parallels

bins = 20
files = os.listdir('results')

params_beta = {'east':[],'north':[],'vertical':[]}
params_alpha = {'east':[],'north':[],'vertical':[]}
lons = []
lats = []
for f in files:
  buff = open('results/%s' % f,'r')
  content = buff.read()
  buff.close()
  lat = _get_field('latitude range',content)
  lat = float(lat.strip().split(',')[0])
  lon = _get_field('longitude range',content)
  lon = float(lon.strip().split(',')[0])
  lons += [lon]
  lats += [lat]
  content = content[content.find('REML RESULTS'):]
  content = content[content.find('station :'):]
  for dir in ['east','north','vertical']:
    params = _get_field('optimal %s parameters' % dir,content).strip().split(',')
    params_beta[dir] += [float(params[0])]
    params_alpha[dir] += [float(params[1])]

east_beta = params_beta['east']
north_beta = params_beta['north']
vertical_beta = params_beta['vertical']
east_alpha = params_alpha['east']
north_alpha = params_alpha['north']
vertical_alpha = params_alpha['vertical']

stats_box = {'facecolor':'w','alpha':0.8,'boxstyle':'round','edgecolor':'0.8'}

fig,axs = plt.subplots(3,2,figsize=(7.0,5.5))

axs[0][1].hist(east_beta,np.linspace(0.0,2.0,bins),color='C0',zorder=2)
text = 'median : %.2f\nIQR : %.2f' % (np.median(east_beta),iqr(east_beta))
axs[0][1].text(0.55,0.68,text,transform=axs[0][1].transAxes,bbox=stats_box,fontsize=10)
axs[0][1].grid(zorder=0)
axs[0][1].set_ylabel('count',fontsize=10)
axs[0][1].set_xlabel(r'east $\mathregular{\beta}$ [mm/yr$^{0.5}$]',fontsize=10)
axs[0][1].tick_params(labelsize=10)

axs[1][1].hist(north_beta,np.linspace(0.0,2.0,bins),color='C0',zorder=2)
text = 'median : %.2f\nIQR : %.2f' % (np.median(north_beta),iqr(north_beta))
axs[1][1].text(0.55,0.68,text,transform=axs[1][1].transAxes,bbox=stats_box,fontsize=10)
axs[1][1].grid(zorder=0)
axs[1][1].set_ylabel('count',fontsize=10)
axs[1][1].set_xlabel(r'north $\mathregular{\beta}$ [mm/yr$^{0.5}$]',fontsize=10)
axs[1][1].tick_params(labelsize=10)

axs[2][1].hist(vertical_beta,np.linspace(0.0,50.0,bins),color='C0',zorder=2)
text = 'median : %.1f\nIQR : %.1f' % (np.median(vertical_beta),iqr(vertical_beta))
axs[2][1].text(0.55,0.68,text,transform=axs[2][1].transAxes,bbox=stats_box,fontsize=10)
axs[2][1].grid(zorder=0)
axs[2][1].set_ylabel('count',fontsize=10)
axs[2][1].set_xlabel(r'vertical $\mathregular{\beta}$ [mm/yr$^{0.5}$]',fontsize=10)
axs[2][1].tick_params(labelsize=10)

axs[0][0].hist(east_alpha,np.linspace(0.0,8.0,bins),color='C0',zorder=2)
text = 'median : %.2f\nIQR : %.2f' % (np.median(east_alpha),iqr(east_alpha))
axs[0][0].text(0.55,0.68,text,transform=axs[0][0].transAxes,bbox=stats_box,fontsize=10)
axs[0][0].grid(zorder=0)
axs[0][0].set_ylabel('count',fontsize=10)
axs[0][0].set_xlabel(r'east $\mathregular{\alpha}$ [1/yr]',fontsize=10)
axs[0][0].tick_params(labelsize=10)

axs[1][0].hist(north_alpha,np.linspace(0.0,8.0,bins),color='C0',zorder=2)
text = 'median : %.2f\nIQR : %.2f' % (np.median(north_alpha),iqr(north_alpha))
axs[1][0].text(0.55,0.68,text,transform=axs[1][0].transAxes,bbox=stats_box,fontsize=10)
axs[1][0].grid(zorder=0)
axs[1][0].set_ylabel('count',fontsize=10)
axs[1][0].set_xlabel(r'north $\mathregular{\alpha}$ [1/yr]',fontsize=10)
axs[1][0].tick_params(labelsize=10)

axs[2][0].hist(vertical_alpha,np.linspace(0.0,50.0,bins),color='C0',zorder=2)
text = 'median : %.2f\nIQR : %.2f' % (np.median(vertical_alpha),iqr(vertical_alpha))
axs[2][0].text(0.55,0.68,text,transform=axs[2][0].transAxes,bbox=stats_box,fontsize=10)
axs[2][0].grid(zorder=0)
axs[2][0].set_ylabel('count',fontsize=10)
axs[2][0].set_xlabel(r'vertical $\mathregular{\alpha}$ [1/yr]',fontsize=10)
axs[2][0].tick_params(labelsize=10)
fig.tight_layout(h_pad=0.25,w_pad=0.25)
plt.savefig('noise-params.pdf',format='pdf')

# plot samples of the median noise models
fig,ax = plt.subplots(3,1,figsize=(7,4),sharex=True)

dt = 1.0/365.25
time = np.arange(0.0,5.0,dt)

gp = fogm(np.median(east_beta),np.median(east_alpha),convert=False)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[0].plot(time,sample,'C0',lw=1.5)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[0].plot(time,sample,'C1',lw=1.5)
ax[0].grid(zorder=0)
#ax[0].set_xlabel('time [yr]',fontsize=10)
ax[0].set_ylabel('easting [mm]',fontsize=10)
#ax[0].tick_params(labelsize=10)
#ax[0].set_xlim((0.0,7.0))

gp = fogm(np.median(north_beta),np.median(north_alpha),convert=False)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[1].plot(time,sample,'C0',lw=1.5)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[1].plot(time,sample,'C1',lw=1.5)
ax[1].grid(zorder=0)
#ax[1].set_xlabel('time [yr]',fontsize=10)
ax[1].set_ylabel('northing [mm]',fontsize=10)
#ax[1].tick_params(labelsize=10)
#ax[1].set_xlim((0.0,7.0))

gp = fogm(np.median(vertical_beta),np.median(vertical_alpha),convert=False)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[2].plot(time,sample,'C0',lw=1.5)
sample = gp.sample(time[:,None],use_cholesky=True)
ax[2].plot(time,sample,'C1',lw=1.5)
ax[2].grid()
ax[2].set_xlabel('time [yr]',fontsize=10)
ax[2].set_ylabel('vertical [mm]',fontsize=10)
ax[2].tick_params(labelsize=10)
ax[2].set_xlim((0.0,5.0))
fig.tight_layout()
plt.savefig('noise-samples.pdf',format='pdf')

plt.show()


