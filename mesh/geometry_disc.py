import numpy as np

from copy import deepcopy

# |----------------------------------------------------------------------|
# |  This code aims to approach the mapping points of the disc geometry, |
# |  this is necessery to generate the patterned mesh.                   |
# |----------------------------------------------------------------------|

# This function has as inputs the function curves and how many point the
# user want to use in each curve. The fist curve is the nucleo top curve of 
# the disc. The second curve is the annulus (external) top curve. The third
# is the nucleo bottom curve of the disc, and finally, the fourth is the an-
# nulus (external) bottom curve of the disc.

def disc_geometry(curve_1, curve_2, curve_3, curve_4, n_points):

    # delta_tetha is the distance between the points of the curve

    delta_tetha = 1/(4*(n_points-1))

    # These curve points lists are the points sets of each of the four curves
    # of the geometry of the disc. The curves points has three coordenates (x,
    # y, z), and z is changed when points are in bottom or top face of the disc

    points_curve_1 = []

    points_curve_2 = []

    points_curve_3 = []

    points_curve_4 = []

    # Iterate four times because the curves pass through four parts of the disc

    for i in range(4):

        points_curve_1.append([])

        points_curve_2.append([])

        points_curve_3.append([])

        points_curve_4.append([])

        # The steps below is necesary because the last point of the curve segment 
        # in one of the four regions is the first point of the next curve segment.
        # Exemple: [[1, 2, 3, 4], [4, 5, 6, 7]]

        for j in range(n_points):

            tetha = ((i*(n_points-1))+j)*delta_tetha

            points_curve_1[-1].append(curve_1(tetha))

            points_curve_2[-1].append(curve_2(tetha))

            points_curve_3[-1].append(curve_3(tetha))

            points_curve_4[-1].append(curve_4(tetha))

        # This step is necessary because when the process satars in the first part
        # of the disc, there is no previous reference.

        if i>0:
    
            points_curve_1[-1][0] = deepcopy(points_curve_1[-2][-1])
            
            points_curve_2[-1][0] = deepcopy(points_curve_2[-2][-1])
            
            points_curve_3[-1][0] = deepcopy(points_curve_3[-2][-1])
            
            points_curve_4[-1][0] = deepcopy(points_curve_4[-2][-1])
    
    # Note: Computacional truncation generates values thats can harm the mesh generation 
    # (the volums can be kept separeted). Thats why we need to ensure the values are the 
    # same. Exemple: [2, 1, 0], [0, 1, 2], and not [2, 1, 0], [-2e-15, 1, 2]

    points_curve_1[-1][-1] = deepcopy(points_curve_1[0][0])
    
    points_curve_2[-1][-1] = deepcopy(points_curve_2[0][0])
    
    points_curve_3[-1][-1] = deepcopy(points_curve_3[0][0])
    
    points_curve_4[-1][-1] = deepcopy(points_curve_4[0][0])

    # Test

    for sublist in points_curve_1:

        print(sublist)

        print("")

if __name__=="__main__":

    # r is the small radius of the disc (is an important parameter to describe
    # the internal curves of the nucleo)

    r = 0.9

    # R is the bigger radiu of the disc (is an important parameter to describe
    # the external curves of the annulus)

    R = 1.8

    # z is the high of the disc

    z = 1.0

    n_points = 4

    # f_i(tetha) = (rsen(2pitetha), rcos(2pitetha), z), can be r or R, it depends
    # on each curve.

    def function_curve_1(tetha_value):

        return [r*np.sin(2*np.pi*tetha_value), r*np.cos(2*np.pi*tetha_value), z]
    
    def function_curve_3(tetha_value):

        return [r*np.sin(2*np.pi*tetha_value), r*np.cos(2*np.pi*tetha_value), 0.0]
    
    def function_curve_2(tetha_value):

        return [R*np.sin(2*np.pi*tetha_value), R*np.cos(2*np.pi*tetha_value), z]
    
    def function_curve_4(tetha_value):

        return [R*np.sin(2*np.pi*tetha_value), R*np.cos(2*np.pi*tetha_value), 0.0]
    
    disc_geometry(function_curve_1, function_curve_2, function_curve_3, function_curve_4, n_points)
    
    
