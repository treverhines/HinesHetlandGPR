import numpy as np
import matplotlib.pyplot as plt
import pygeons
from mpl_toolkits.basemap import Basemap
import h5py
from matplotlib.colors import ListedColormap
from matplotlib.patches import Ellipse
from matplotlib.cm import viridis
from myplot.colorbar import pseudo_transparent_cmap,transparent_colorbar
from sympy import sqrt,pi,exp
import rbf

r,eps = rbf.basis.get_r(),rbf.basis.get_eps()
expr = 1.0/sqrt((2*pi)**2*eps**4)*exp(-r**2/(2*eps**2))
normal2d = rbf.basis.RBF(expr)

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

def setup_ax(bm,ax):
  # function which prints out the coordinates on the bottom left 
  # corner of the figure
  def coord_string(x,y):
    str = 'x : %g  y : %g  ' % (x,y)
    str += '(lon : %g E  lat : %g N)' % bm(x,y,inverse=True)
    return str

  ax.format_coord = coord_string
  bm.drawcountries(ax=ax,zorder=1)
  bm.drawstates(ax=ax,zorder=1)
  bm.drawcoastlines(ax=ax,zorder=1)
  bm.drawmapboundary(ax=ax,fill_color=(0.8,0.8,0.8),zorder=0)
  bm.fillcontinents(ax=ax,color=(1.0,1.0,1.0),lake_color=(0.8,0.8,0.8),zorder=0)
  mer,par = get_meridians_and_parallels(bm,3)
  bm.drawmeridians(mer,
                   labels=[0,0,0,1],dashes=[2,2],fontsize=10,
                   ax=ax,zorder=1,color=(0.3,0.3,0.3,1.0))
  bm.drawparallels(par,
                   labels=[1,0,0,0],dashes=[2,2],fontsize=10,
                   ax=ax,zorder=1,color=(0.3,0.3,0.3,1.0))
  scale_lon,scale_lat = bm(*ax.transData.inverted().transform(ax.transAxes.transform([0.15,0.08])),
                           inverse=True)
  scale_size = 100.0
  bm.drawmapscale(scale_lon,scale_lat,scale_lon,scale_lat,scale_size,
                  ax=ax,barstyle='fancy',fontsize=10,zorder=4)
  return

bm = Basemap(projection='tmerc',
             resolution='i',
             lon_0 = -123.0,lat_0 = 45.0,
             llcrnrlon = -125.8,llcrnrlat = 45.4,
             urcrnrlon = -119.5,urcrnrlat = 49.5)

fig,ax = plt.subplots(figsize=(7.0,5.5))
setup_ax(bm,ax)

# LOAD IN STATION LOCATIONS
data = h5py.File('data.final.h5')
lon = data['longitude'][...]
lat = data['latitude'][...]
x,y = bm(lon,lat)
ax.plot(x,y,'ko',ms=4,zorder=3)
# Show locations for SC03 and P436
idx = np.nonzero(data['id'][...] == 'SC03')[0][0]
stax,stay = x[idx],y[idx]
ax.plot(stax,stay,'ro',ms=10,zorder=4)
ax.text(stax-17000.0,stay-23000.0,'SC03',color='r',fontsize=10)
idx = np.nonzero(data['id'][...] == 'P436')[0][0]
stax,stay = x[idx],y[idx]
ax.plot(stax,stay,'ro',ms=10,zorder=4)
ax.text(stax-17000.0,stay-23000.0,'P436',color='r',fontsize=10)
# plot location of strain time series
stax,stay = bm(-124.03,47.9)
radius = 150000.0
ax.plot(stax,stay,'C0o',ms=10,zorder=4)
art = Ellipse((stax,stay),2*radius,2*radius,fc='none',ls='--',ec='C0',zorder=4)
ax.add_artist(art)

# PLOT TREMOR DENSITY
N = 50
xlim = ax.get_xlim()
ylim = ax.get_ylim()
xitp = np.linspace(xlim[0],xlim[1],N)
yitp = np.linspace(ylim[0],ylim[1],N)
xg,yg = np.meshgrid(xitp,yitp)
xy = np.array([xg.ravel(),yg.ravel()]).T

data = np.loadtxt('08_01_2009_05_22_2017.txt',skiprows=16,dtype=str)
start_day = pygeons.mjd.mjd('2009-08-01','%Y-%m-%d')
end_day = pygeons.mjd.mjd('2017-05-22','%Y-%m-%d')
total_days = end_day - start_day
tremor_lons = data[:,3].astype(float)
tremor_lats = data[:,2].astype(float)
tremor_xy = np.array(bm(tremor_lons,tremor_lats)).T
# tremors per km^2
density = [1000**2/(total_days/365.25)*np.sum(normal2d([xyi],tremor_xy,eps=20000.0),axis=1) for xyi in xy]
u = np.reshape(density,(N,N))

colors = np.zeros((256,4))
val = np.linspace(0.0,1.0,256)
colors = np.array(viridis(val))
colors[:,3] = val
cmap = ListedColormap(colors)
p = ax.imshow(u,cmap=cmap,zorder=2,extent=(xlim+ylim),origin='lower',
              interpolation='bicubic')
cbar = transparent_colorbar(p,ax=ax)
cbar.ax.tick_params(labelsize=10)
cbar.set_label('tremors per km$\mathregular{^2}$ per year',fontsize=10)
plt.tight_layout(pad=3.0)
plt.savefig('context-map.pdf',fmt='pdf')
plt.show()
quit()
