############################################################################################
#
# Plotting utilities for cartesian 3D output from CUMC3D
# Written by Ho Sang (Leon) Chan at 2023
# The Chinese University of Hong Kong and University of Colorado
#
############################################################################################

#import packages#
import sys
import h5py
import math
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt

############################################################################################
# define function #

# plot contour #
def plot_contour(prim,filename,domain='xy',scale='log',stream=False,bh=False):

    # set figure #
    fig, ax = plt.subplots(1, 1)

    # set axis ticks #
    if(domain == 'xy'):
        plt.xlabel('x-direction', size=15)
        plt.ylabel('y-direction', size=15)
    elif(domain == 'xz'):
        plt.xlabel('x-direction', size=15)
        plt.ylabel('z-direction', size=15)
    elif(domain == 'yz'):
        plt.xlabel('y-direction', size=15)
        plt.ylabel('z-direction', size=15)

    # set x,y axis #
    if(domain == 'xy'):
        x_plot = X_xy
        y_plot = Y_xy
    elif(domain == 'xz'):
        x_plot = X_xz
        y_plot = Z_xz
    elif(domain == 'yz'):
        x_plot = Y_yz
        y_plot = Z_yz

    # log scale plot #
    if(scale == 'log'):
        zmax = int(math.ceil(np.log10(np.max(prim))))
        zmin = int(math.floor(np.log10(np.min(prim))))
        cp = ax.contourf(x_plot, y_plot, prim, np.logspace(zmin, zmax, 100), locator=ticker.LogLocator(), cmap='plasma',extend='both')
        cbar = fig.colorbar(cp)
        rang = np.arange(int(np.log10(np.min(prim))), int(np.log10(np.max(prim))) + 1, 1)
        loca = 10 ** (np.array(rang).astype(float))
        cbar.set_ticks(loca)
        cbar.minorticks_off()
        labels = ['10$^{%.0f}$' % x for x in rang]
        cbar.ax.set_yticklabels(labels, fontsize=15)

    # linear scale plot #
    elif(scale == 'linear'):
        cp = ax.contourf(x_plot, y_plot, prim, 100, cmap='plasma', extend='both')
        cbar = fig.colorbar(cp)
        cbar.ax.tick_params(labelsize=15)
    
    # plot bfield stream line ?#
    if(stream):
        if(domain == 'xy'):
            b1 = xy_full(bx)
            b2 = xy_full(by)
        elif(domain == 'xz'):
            b1 = xz_full(bx)
            b2 = xz_full(bz)
        elif(domain == 'yz'):
            b1 = yz_full(by)
            b2 = yz_full(bz)
        plt.streamplot(x_plot, y_plot, b1, b2, density=1.5, linewidth=None, color='black', broken_streamlines=True)

    #plot a black hole at the center #
    if(bh):
        circle1 = plt.Circle((0, 0), np.min(R), color='black')
        ax.add_patch(circle1) 

    # axis properties # 
    plt.xlim(np.min(x_plot), np.max(x_plot))
    plt.ylim(np.min(y_plot), np.max(y_plot))
    ax.tick_params(axis='both', labelsize=15)
    plt.title('Time = ' + '%.3f' % time, size=15)
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig(imgdir+str(filename)+'-'+str(domain)+'-'+'%.3f' % time +'.png')
    plt.clf()
    plt.close()

############################################################################################
# define function #

# array for planar view #
def xy_full(prim):
    p_temp = np.ndarray(shape=(prim.shape[0],prim.shape[1]), dtype=float)
    p_temp[:,:] = prim[:,:,0]
    p_temp = p_temp.T
    if(p_temp.shape != X_xy.shape):
      p_temp = p_temp.T
    return p_temp

# array for birdeye view #
def xz_full(prim):
    p_temp = np.ndarray(shape=(prim.shape[0],prim.shape[2]), dtype=float)
    p_temp[:,:] = prim[:,0,:]
    p_temp = p_temp.T
    if(p_temp.shape != X_xz.shape):
      p_temp = p_temp.T
    return p_temp

# array for angular average #
def yz_full(prim):
    p_temp = np.ndarray(shape=(prim.shape[1],prim.shape[2]), dtype=float)
    p_temp[:,:] = prim[0,:,:]
    p_temp = p_temp.T
    if(p_temp.shape != Y_yz.shape):
      p_temp = p_temp.T
    return p_temp

############################################################################################
# define function #

#plotting function #
def plot(z_in,fname,stream=False):

    # choose plotting scale #
    if((np.min(z_in) == np.max(z_in)) or (np.min(z_in) <= 0) or (np.max(z_in) <= 0) or np.isnan(z_in).any()):
        scale = 'linear'
    else:
        scale = 'log'
    
    ######################################################################################
    # x-y projection variables #
    z = xy_full(z_in)

    #plot#
    plot_contour(z,fname,domain='xy',scale=scale,stream=stream,bh=False)

    ######################################################################################
    # x-z projection variables #
    z = xz_full(z_in)

    #plot#
    try:
        plot_contour(z,fname,domain='xz',scale=scale,stream=stream,bh=False)
    except:
        pass 

    ######################################################################################
    # y-z projection variables #
    z = yz_full(z_in)

    #plot#
    try:
        plot_contour(z,fname,domain='yz',scale=scale,stream=stream,bh=False)
    except:
        pass 
    
############################################################################################
#load command line parameters #

# read path #
gridfile=sys.argv[1]
hdf5file=sys.argv[2]

# get path #
imgdir = './figure/'

############################################################################################
# file input output #

#load grid#
f = h5py.File(gridfile, 'r')
dset = f['x-direction']
xaxis = dset[:]
dset = f['y-direction']
yaxis = dset[:]
dset = f['z-direction']
zaxis = dset[:]

############################################################################################
#gridding#

#mesh grid, half x-y plane#
X_xy, Y_xy = np.meshgrid(xaxis, yaxis)

#mesh grid, half x-z plane#
X_xz, Z_xz = np.meshgrid(xaxis, zaxis)

#mesh grid, half y-z plane#
Y_yz, Z_yz = np.meshgrid(yaxis, zaxis)

########################################################################################
# main plotting functions #

# load hdf5 file #
f = h5py.File(hdf5file, 'r')

# load primitive variables #
dset = f['primitive']
primitive = dset[:]
primitive = primitive.T

# get primitive variables #
rho = primitive[0,:,:,:]
velx = primitive[1,:,:,:]
vely = primitive[2,:,:,:]
velz = primitive[3,:,:,:]
p = primitive[4,:,:,:]

# load magnetic field #
dset = f['bfield']
bfield = dset[:]
bfield = bfield.T

#magnetic fields#
bx = bfield[0,:,:,:]
by = bfield[1,:,:,:]
bz = bfield[2,:,:,:]

#load epsilon#
dset = f['epsilon']
epsilon = dset[:]
epsilon = epsilon.T
epsilon = epsilon[:,:,:]

#time#
dset = f['time']
time = dset[:][0]

########################################################################################
#plot#

# density #
z = rho
plot(z,'rho',stream=True)

# plasma beta #
z = 2*p/(bx**2 + by**2 + bz**2 + 1e-10)
plot(z,'beta',stream=False)

########################################################################################