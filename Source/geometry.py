import numpy as np
import matplotlib.pyplot as plt

#---------------
# Geometry utils
#---------------

# Apply rigid motion transformation
def rigid_motion(x, alpha=0, beta=0, gamma=0, trans=[0,0,0]):
    
    rot_x = np.array([[ 1, 0 ,0],
                      [ 0, np.cos(alpha), np.sin(alpha)], 
                      [ 0, -np.sin(alpha), np.cos(alpha)]])
    rot_y = np.array([[ np.cos(beta), 0, np.sin(beta)], 
                      [ 0, 1 ,0],
                      [ -np.sin(beta), 0, np.cos(beta) ]])
    rot_z = np.array([[ np.cos(gamma), np.sin(gamma), 0], 
                      [ -np.sin(gamma), np.cos(gamma) ,0], 
                      [ 0, 0 ,1]])
    
    rot = rot_x.dot(rot_y.dot(rot_z))
    trans = np.array(trans).reshape(1,3)
    
    return rot.dot(x.T).T + trans

# Create grid in 3D of given size
def get_plane(z = 0, w = 10, h = 10):
    
    a = np.zeros((w*h,3))
    a[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1, 2)
    a[:,2] += z
    a -= a.mean(0)
    scale = a.max(0)[0]
    a /= scale
    
    return a

# Create cube from transformations of planes
def get_cube(axissize = 15):

    plane = get_plane(0, w=axissize, h=axissize)
    
    plane1 = rigid_motion(plane, trans=[0,0,+1])
    plane2 = rigid_motion(plane, trans=[0,0,-1])
    plane3 = rigid_motion(plane, alpha=np.pi/2, trans=[0,+1,0])
    plane4 = rigid_motion(plane, alpha=np.pi/2, trans=[0,-1,0])
    plane5 = rigid_motion(plane, beta=np.pi/2, trans=[+1,0,0])
    plane6 = rigid_motion(plane, beta=np.pi/2, trans=[-1,0,0])

    cube = np.concatenate([plane1, plane2, plane3, plane4, plane5, plane6])
    
    return cube

# Cube to sphere mapping, following different methods
# Radial is radial contraction, same than used in opengl, unreal etc.
# Nowell from http://mathproofs.blogspot.com/2005/07/mapping-cube-to-sphere.html
# vanLangen from https://hvlanalysis.blogspot.com/2023/05/mapping-cube-to-sphere.html?lr=1
def cube2sphere(points, method="radial"):
    
    x, y, z = points[:,0], points[:,1], points[:,2]
    
    if method=="radial":
        
        r = np.sqrt(x**2. + y**2. + z**2.)
    
        xprime = x/r
        yprime = y/r
        zprime = z/r
    
    elif method=="Nowell":
    
        xprime = x*np.sqrt( 1 - y**2./2. - z**2./2. + y**2.*z**2./3. )
        yprime = y*np.sqrt( 1 - x**2./2. - z**2./2. + x**2.*z**2./3. )
        zprime = z*np.sqrt( 1 - y**2./2. - x**2./2. + y**2.*x**2./3. )
        
    elif method=="vanLangen":
        
        pfac = 50
        
        xp = np.sqrt(x**pfac + y**2. + z**2.)
        yp = np.sqrt(y**pfac + x**2. + z**2.)
        zp = np.sqrt(z**pfac + y**2. + x**2.)
        
        xc = xp*np.tan(x*np.arctan(1./xp))
        yc = yp*np.tan(y*np.arctan(1./yp))
        zc = zp*np.tan(z*np.arctan(1./zp))
        
        rc = np.sqrt(xc**2. + yc**2. + zc**2.)
        
        xprime = xc/rc
        yprime = yc/rc
        zprime = zc/rc
    
    return np.concatenate([xprime.reshape(-1,1), yprime.reshape(-1,1), zprime.reshape(-1,1)], axis=1)

# TODO
# write sphere2cube mapping, i.e., inverse mapping

# 3D plot
def threedplot(x0, scale=1, cols = None, edgecolors='black'):

    w = 10
    fig = plt.figure(figsize=(w*scale,w))
    ax1 = fig.add_subplot(1,2,1, projection ="3d")
    if cols is None: cols = "orange"
    ax1.scatter(x0[:, 0], x0[:, 1], x0[:, 2], c=cols, edgecolors=edgecolors)

