import numpy as np
import matplotlib.pyplot as plt
import rbf
from mpl_toolkits.mplot3d import Axes3D
np.random.seed(7)


gp_x = rbf.gauss.gpse((0.0,1.0,100.0))
gp_t = rbf.gauss.gpse((0.0,1.0,10.0))

# combined
gp = rbf.gauss.GaussianProcess(
       lambda x: np.zeros(len(x)), 
       lambda x1,x2: gp_x.covariance(x1[:,[0]],x2[:,[0]])*
                     gp_t.covariance(x1[:,[1]],x2[:,[1]]),
       dim=2)


###### PLOT COVARIANCE
#####################################################################
Nx = 20
Nt = 20
figsize = (7.0,3.0)

x = np.linspace(0.0,300.0,Nx)
t = np.linspace(0.0,30.0,Nt)
xg,tg = np.meshgrid(x,t)
p = np.array([xg.flatten(),tg.flatten()]).T

# make cov array
cov = gp.covariance([[0.0,0.0]],p)
cov = cov.reshape((Nx,Nt))

fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(1,2,1,projection='3d')
ax.view_init(35.0,35.0)

p = ax.plot_surface(xg,tg,cov,cmap='viridis',edgecolor='k',linewidth=0.5)

# set labels
ax.set_ylabel(r'$\mathregular{|t - t\prime|}$ [days]',fontsize=10)
ax.set_xlabel(r'$\mathregular{||\vec{x} - \vec{x}\prime||_2}$ [km]',fontsize=10)
ax.set_zlabel('covariance [mm$^2$]',fontsize=10)
ax.set_xticks([0,75,150,225,300])
ax.tick_params(pad=0)
ax.tick_params(labelsize=10)
ax.text2D(-0.05, 0.9, "A", fontsize=16, transform=ax.transAxes)

###### PLOT SAMPLE
#####################################################################
Nx = 30
Nt = 30
figsize = (5,4)

x = np.linspace(0.0,500.0,Nx)
t = np.linspace(0.0,50.0,Nt)
xg,tg = np.meshgrid(x,t)
p = np.array([xg.flatten(),tg.flatten()]).T

# make cov array
sample = gp.sample(p)
sample = sample.reshape((Nx,Nt))

ax = fig.add_subplot(1,2,2,projection='3d')
ax.view_init(35.0,55.0)

p = ax.plot_surface(xg,tg,sample,cmap='viridis',edgecolor='k',linewidth=0.5)

# set labels
ax.set_ylabel(r'$\mathregular{t}$ [days]',fontsize=10)
ax.set_xlabel(r'$\mathregular{x_j}$ [km]',fontsize=10)
ax.set_zlabel('displacement [mm]',fontsize=10)
ax.tick_params(pad=1.0)
ax.tick_params(labelsize=10)
ax.text2D(-0.05, 0.9, "B", fontsize=16, transform=ax.transAxes)

plt.tight_layout(pad=0.0,rect=(0.04,0.07,1.03,1.00))
plt.savefig('prior-demo.pdf',format='pdf')
plt.show()
