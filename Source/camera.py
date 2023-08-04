import numpy as np
import matplotlib.pyplot as plt

#---------------
# Fisheye camera theory
#---------------

# Perspective pinhole projection
def pinhole_projection(x, y, z):
    
    return x/z, y/z

# Distance-angle relation for different projection models, output is r/f, where f is the focal length
def r_theta(theta, projection="Kannala-Brandt"):

    if projection=="Perspective":
        r_dist = np.tan(theta)  # = r
    
    elif projection=="Stereographic":
        r_dist = 2.*np.tan(theta/2.)
    
    elif projection=="Equidistant":
        r_dist = theta
    
    elif projection=="Equisolid":
        r_dist = 2.*np.sin(theta/2.)

    elif projection=="Orthographic":
        r_dist = np.sin(theta)
    
    elif projection=="Kannala-Brandt":
        k1, k2, k3, k4 = 0.08309221636708493, 0.01112126630599195, 0.008587261043925865, 0.0008542188930970716  # Marcel values
        r_dist = theta*(1. + k1*theta**2 + k2*theta**4 + k3*theta**6 + k4*theta**8)
    
    else:
        print("Projection model not valid")
    
    return r_dist

# Fisheye distortion using different projection models
# Forward method, given theta, get r
# x y expected as perspective projection coordinates
# https://euratom-software.github.io/calcam/html/intro_theory.html
# https://oulu3dvision.github.io/calibgeneric/Kannala_Brandt_calibration.pdf
def fisheye_forward(x, y, z, projection="Kannala-Brandt"):

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(r)
    theta[z>0] = np.pi - theta[z>0]

    r_dist = r_theta(theta, projection)

    xprime, yprime = (r_dist/r)*x, (r_dist/r)*y

    # Fovs > 180º are plotted rotated for some reason, this is a hack to counteract it, but probably can be done better
    ang = np.pi
    xprime[z>0] = np.cos(ang)*xprime[z>0] + np.sin(ang)*yprime[z>0]
    yprime[z>0] = -np.sin(ang)*xprime[z>0] + np.cos(ang)*yprime[z>0]
        
    return xprime, yprime

# Fisheye distortion using different projection models
# u,v are pixel values
# Inverse method, given r_dist=r/f, get theta
def fisheye_inverse(u, v, projection="Kannala-Brandt"):

    r_dist = np.sqrt(u**2 + v**2)
    theta = np.arctan(r_dist)

    if projection=="Perspective":
        theta = np.arctan(r_dist)  # = r
    
    elif projection=="Stereographic":
        theta = 2.*np.arctan(r_dist/2.)
    
    elif projection=="Equidistant":
        theta = r_dist
    
    elif projection=="Equisolid":
        theta = 2.*np.arcsin(r_dist/2.)

    elif projection=="Orthographic":
        theta = np.arcsin(r_dist)
    
    elif projection=="Kannala-Brandt":
        k1, k2, k3, k4 = 0.08309221636708493, 0.01112126630599195, 0.008587261043925865, 0.0008542188930970716  # Marcel values

        # Iterative process as in shader (TODO: this is wrong! modify using Newton-Raphson)
        theta = r_dist
        for i in range(10):
            theta = r_dist/(1. + k1*theta**2 + k2*theta**4 + k3*theta**6 + k4*theta**8)
    
    else:
        print("Projection model not valid")
        
    return np.tan(theta)/r_dist*u, np.tan(theta)/r_dist*v

# Get focal length (in pixels) given the field of vision and image size
def focal_length(fov, imagesize, projection="Kannala-Brandt"):

    return (imagesize/2.)/r_theta(fov/2., projection)

# Show projected image
def projected_image(x, y, z, title, f=1, lim=0.4):

    fig = plt.figure(figsize=(6, 5))
    
    plt.scatter(x*f,y*f,c=z, s=1)
    plt.colorbar()
    plt.title(title)
    plt.xlim([-lim,lim])
    plt.ylim([-lim,lim])