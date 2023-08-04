# Undistort fisheye image to get the correspondent perspective projection

import cv2
import numpy as np
import sys

# You should replace these 3 lines with the output in calibration step
f = 320
#D=np.array([[0.08309221636708493], [0.01112126630599195], [0.008587261043925865], [0.0008542188930970716]])
D=np.array([[0.0], [0.0], [0.0], [0.0]])

def undistort(img_path):    

    img = cv2.imread(img_path)
    h,w = img.shape[:2]  
    print(h,w)  
    K=np.array([[f, 0.0, h/2], [0.0, f, w/2], [0.0, 0.0, 1.0]])

    print(K, D, np.eye(3), K, (h,w), cv2.CV_16SC2)

    undistorted_img = cv2.fisheye.undistortImage(img, K, D, None, K)
    
    cv2.imshow("undistorted", undistorted_img)
    cv2.imwrite(img_path.replace(".png","_undistorted.png"), undistorted_img)
    #cv2.imwrite("images/equi_undistorted.png", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # This gives the same than above
    # map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    # undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)   
    
    
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)