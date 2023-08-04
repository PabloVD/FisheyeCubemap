# Blend and combine two images for proper comparison

import cv2

alpha = 0.5

path = "images/projections/"


#projections = ["Stereographic","Equidistant","Equisolid","Orthographic","Kannala-Brandt"]
projections = ["Equidistant"]
#projections = ["Kannala-Brandt"]

def remove_white(src1, h, w):

    coords = cv2.findNonZero(255-cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)) # Find all non-zero points (text)
    x, y, ww, hh = cv2.boundingRect(coords) # Find minimum spanning bounding box
    src1 = src1[y:y+hh, x:x+ww]
    src1 = cv2.resize(src1, (h,w))

    return src1

for projection in projections:

    # [load]
    src1 = cv2.imread(path+projection+".png")
    src2 = cv2.imread(path+projection+"_rendered.png")

    h, w = src1.shape[:2]

    src1 = remove_white(src1, h, w)
    src2 = remove_white(src2, h, w)

    dst = cv2.addWeighted(src1, alpha, src2, 1. - alpha, 0.0)

    # [blend_images]
    # [display]
    cv2.imshow(projection, dst)
    cv2.imwrite("images/blended/"+projection+"_blended.png", dst)
    cv2.waitKey(0)
    # [display]
    cv2.destroyAllWindows()