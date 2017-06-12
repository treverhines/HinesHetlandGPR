import numpy as np
import matplotlib.pyplot as plt
import pygeons
from mpl_toolkits.basemap import Basemap
import h5py
from pygeons.plot.strain_glyph import strain_glyph
from matplotlib.text import Text
from matplotlib.patches import Rectangle

# PARAMETERS
strain_scale = 25000.0
plot_date = '2016-01-01'

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
  scale_lon,scale_lat = bm(*ax.transData.inverted().transform(ax.transAxes.transform([0.815,0.06])),
                           inverse=True)
  scale_size = 100.0
  bm.drawmapscale(scale_lon,scale_lat,scale_lon,scale_lat,scale_size,
                  ax=ax,barstyle='fancy',fontsize=10,zorder=4)
  return

bm = Basemap(projection='tmerc',
             resolution='i',
             lon_0 = -123.0,lat_0 = 45.0,
             llcrnrlon = -125.7,llcrnrlat = 46.0,
             urcrnrlon = -120.0,urcrnrlat = 49.8)


fig,ax = plt.subplots(figsize=(6,6.0))
setup_ax(bm,ax)

# LOAD FILE
fdx = h5py.File('merged.dudx.h5')
fdy = h5py.File('merged.dudy.h5')
mjd_date = pygeons.mjd.mjd(plot_date,'%Y-%m-%d')

# convert to microstrain/year
tidx = np.nonzero(fdx['time'][...] == mjd_date)[0][0]
dudx = fdx['east'][tidx] * 1.0e6 * 365.25
dudx_std = fdx['east_std_dev'][tidx] * 1.0e6 * 365.25
dudy = fdy['east'][tidx] * 1.0e6 * 365.25
dudy_std = fdy['east_std_dev'][tidx] * 1.0e6 * 365.25

dvdx = fdx['north'][tidx] * 1.0e6 * 365.25
dvdx_std = fdx['north_std_dev'][tidx] * 1.0e6 * 365.25
dvdy = fdy['north'][tidx] * 1.0e6 * 365.25
dvdy_std = fdy['north_std_dev'][tidx] * 1.0e6 * 365.25

# Plot strain glyphs
glyphs = []
lon = fdx['longitude'][...]
lat = fdx['latitude'][...]
x,y = bm(lon,lat)

for xidx in range(len(x)):
  pos = [x[xidx],y[xidx]]
  strain = [dudx[xidx],    dvdy[xidx],    0.5*(dudy[xidx] + dvdx[xidx])]
  sigma =  [dudx_std[xidx],dvdy_std[xidx],0.5*np.sqrt(dudy_std[xidx]**2 + dvdx_std[xidx]**2)]
  glyph = strain_glyph(pos,strain,sigma,
                       scale=strain_scale,
                       ext_color='C0',
                       cmp_color='C1',
                       alpha=0.4,
                       linewidth=1.5,
                       vert=500,
                       zorder=2,
                       snr_mask=False)
  for g in glyph: 
    ax.add_artist(g)

# Plot key
mag = 1.0
strain = [mag,-mag,0.0]
sigma = [0.25*mag,0.25*mag,0.25*mag]
key_pos_display = ax.transAxes.transform((0.725,0.205))
key_pos_data = ax.transData.inverted().transform(key_pos_display)
posx,posy = key_pos_data
glyph_key = strain_glyph(key_pos_data,strain,sigma=sigma,
                         scale=strain_scale,
                         ext_color='C0',
                         cmp_color='C1',
                         alpha=0.4,
                         linewidth=1.5,
                         zorder=4,
                         vert=500)

text_str = '%s $\mathregular{\mu}$strain/yr' % mag
textx = posx + 1.2*mag*strain_scale
texty = posy - 0.1*mag*strain_scale
glyph_key += Text(textx,texty,text_str,
                   fontsize=10,
                   color='C0',zorder=4),

textx = posx + 0.4*mag*strain_scale
texty = posy - 1.2*mag*strain_scale
glyph_key += Text(textx,texty,'-' + text_str,
                   fontsize=10,
                   color='C1',zorder=4),

for a in glyph_key: 
  ax.add_artist(a)

# plot rectangle
rect = Rectangle([0.63,0.0],0.37,0.3,transform=ax.transAxes,zorder=3,
                 ec=(0.0,0.0,0.0,1.0),
                 fc=(1.0,1.0,1.0,0.7),
                 joinstyle='round', 
                 capstyle='round')
ax.add_artist(rect)
ax.legend()
plt.tight_layout(pad=3.0)
plt.savefig('strain-map.pdf',fmt='pdf')
plt.show()
