import numpy as np

from copy import deepcopy
from Grante.CuboidGmsh.solids import cuboid_prisms as prisms
from Grante.CuboidGmsh.tool_box import meshing_tools as tools
from Grante.PythonicUtilities.interpolation_tools import spline_3D_interpolation


# |----------------------------------------------------------------------|
# |  This code aims to approach the mapping points of the disc geometry, |
# |  this is necessery to generate the patterned mesh.                   |
# |----------------------------------------------------------------------|

# This function has as inputs the function curves and how many point the
# user want to use in each curve. The fist curve is the nucleo top curve of 
# the disc. The second curve is the annulus (external) top curve. The third
# is the nucleo bottom curve of the disc, and finally, the fourth is the an-
# nulus (external) bottom curve of the disc.

def disc_geometry(top_internal, top_external, bottom_internal, bottom_external, n_points):

    print(len(bottom_internal[0]))

    # Names the parts of the disc to show in gmsh in tools -> visibility -> ...

    surfaces_regions_names = ["bottom", "top", "lateral"]

    volumes_regions_names = ["nucleus", "annulus"]

    # Calls the class (library)

    geometric_data = tools.gmsh_initialization(surface_regionsNames = 
    surfaces_regions_names, volume_regionsNames = volumes_regions_names)

    print(len(bottom_internal[0]))

    # Starts to do the splines of the geometry
    
    top_internal_curve = spline_3D_interpolation(points_array = top_internal, add_initial_point_as_end_point=True)

    print(len(bottom_internal[0]))
    
    top_external_curve = spline_3D_interpolation(points_array = top_external, add_initial_point_as_end_point=True)

    print(len(bottom_internal[0]))
    
    bottom_internal_curve = spline_3D_interpolation(points_array = bottom_internal, add_initial_point_as_end_point=True)
    
    bottom_external_curve = spline_3D_interpolation(points_array = bottom_external, add_initial_point_as_end_point=True)

    # Defines the eight point of the top square corners

    square_top_curve = spline_3D_interpolation(points_array = [[5.0, 5.0, 14.0], [5.0, -3.0, 14.0], [-5.0, -3.0, 14.0], 
                                                               [-3.8, 7.0, 14.0]], add_initial_point_as_end_point=True)

    square_bottom_curve = spline_3D_interpolation(points_array = [[5.0, 5.0, 0.0], [5.0, -3.0, 0.0], [-5.0, -3.0, 0.0], 
                                                                  [-3.8, 7.0, 0.0]], add_initial_point_as_end_point=True)
    
    parametric_curves = {"square top": square_top_curve, "square bottom": square_bottom_curve,
                         "top internal":top_internal_curve, "top external": top_external_curve, 
                         "bottom internal": bottom_internal_curve, "bottom external": bottom_external_curve}
    
    # Defines witch angle there are the flares lines
    
    theta_1 = 0.0

    theta_2 = 0.25

    theta_3 = 0.5

    theta_4 = 0.7

    theta_5 = 1.0

    # ***********************************************************************
    # *                        internal curve setup    (nucleus)            *                                                   
    # ***********************************************************************

    # Defines the setup of the cube (squares) to do the central cuboid

    corner_points = [["square bottom", theta_1], ["square bottom", theta_2], ["square bottom", theta_3], ["square bottom", theta_4],
                     ["square top", theta_1], ["square top", theta_2], ["square top", theta_3], ["square top", theta_4]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "nucleus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"})
    
    # Defines the setup of the first cuboid of the nucleus
    
    corner_points = [["bottom internal", theta_1], ["bottom internal", theta_2], ["square bottom", theta_2], ["square bottom", theta_1],
                     ["top internal", theta_1], ["top internal", theta_2], ["square top", theta_2], ["square top", theta_1]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "nucleus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom internal", theta_1, theta_2, n_points], 
                                                    5: ["top internal", theta_1, theta_2, n_points]})
    
    # Defines the setup of the second cuboid of the nucleus
    
    corner_points = [["bottom internal", theta_2], ["bottom internal", theta_3], ["square bottom", theta_3], ["square bottom", theta_2],
                     ["top internal", theta_2], ["top internal", theta_3], ["square top", theta_3], ["square top", theta_2]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "nucleus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom internal", theta_2, theta_3, n_points], 
                                                    5: ["top internal", theta_2, theta_3, n_points]})
    
    # Defines the setup of the third cuboid of the nucleus
    
    corner_points = [["bottom internal", theta_3], ["bottom internal", theta_4], ["square bottom", theta_4], ["square bottom", theta_3],
                     ["top internal", theta_3], ["top internal", theta_4], ["square top", theta_4], ["square top", theta_3]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "nucleus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom internal", theta_3, theta_4, n_points], 
                                                    5: ["top internal", theta_3, theta_4, n_points]})
    
    # Defines the setup of the fourth cuboid of the nucleus
    
    corner_points = [["bottom internal", theta_4], ["bottom internal", theta_5], ["square bottom", theta_5], ["square bottom", theta_4],
                     ["top internal", theta_4], ["top internal", theta_5], ["square top", theta_5], ["square top", theta_4]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "nucleus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom internal", theta_4, theta_5, n_points], 
                                                    5: ["top internal", theta_4, theta_5, n_points]})
    
    # ***********************************************************************
    # *                        external curve setup   (annulus)             *                                                   
    # ***********************************************************************

    # Defines the setup of the first cuboid of the annulus 

    corner_points = [["bottom external", theta_1], ["bottom external", theta_2], ["bottom internal", theta_2], ["bottom internal", theta_1],
                     ["top external", theta_1], ["top external", theta_2], ["top internal", theta_2], ["top internal", theta_1]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "annulus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom external", theta_1, theta_2, n_points], 
                                                    5: ["top external", theta_1, theta_2, n_points]})
    
    # Defines the setup of the second cuboid of the annulus 
    
    corner_points = [["bottom external", theta_2], ["bottom external", theta_3], ["bottom internal", theta_3], ["bottom internal", theta_2],
                     ["top external", theta_2], ["top external", theta_3], ["top internal", theta_3], ["top internal", theta_2]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "annulus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom external", theta_2, theta_3, n_points], 
                                                    5: ["top external", theta_2, theta_3, n_points]})
    
    # Defines the setup of the third cuboid of the annulus 
    
    corner_points = [["bottom external", theta_3], ["bottom external", theta_4], ["bottom internal", theta_4], ["bottom internal", theta_3],
                     ["top external", theta_3], ["top external", theta_4], ["top internal", theta_4], ["top internal", theta_3]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "annulus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom external", theta_3, theta_4, n_points], 
                                                    5: ["top external", theta_3, theta_4, n_points]})
    
    # Defines the setup of the fourth cuboid of the annulus 
    
    corner_points = [["bottom external", theta_4], ["bottom external", theta_5], ["bottom internal", theta_5], ["bottom internal", theta_4],
                     ["top external", theta_4], ["top external", theta_5], ["top internal", theta_5], ["top internal", theta_4]]

    geometric_data = prisms.hexahedron_from_corners(corner_points, transfinite_directions = [15, 15, 15], 
                                                    geometric_data = geometric_data, 
                                                    parametric_curves = parametric_curves,
                                                    explicit_volume_physical_group_name = "annulus", 
                                                    explicit_surface_physical_group_name = {1: "bottom", 6: "top"},
                                                    edges_points = {1: ["bottom external", theta_4, theta_5, n_points], 
                                                    5: ["top external", theta_4, theta_5, n_points]})
    
    # Calls the function to generate the mesh 
    
    tools.gmsh_finalize(geometric_data = geometric_data, file_name = "intervertebral_disc_mesh")

    """# delta_tetha is the distance between the points of the curve

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

    # Test square points:

    theta_list = [0.125, 0.375, 0.625, 0.875]

    for theta in theta_list:
       
       print(f"Coordinate point of the top square:{square_top_curve(theta)}")

    for theta in theta_list:

        print(f"Coordinate point of the bottom square:{square_bottom_curve(theta)}")"""

if __name__=="__main__":

    """# r is the small radius of the disc (is an important parameter to describe
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

        return [R*np.sin(2*np.pi*tetha_value), R*np.cos(2*np.pi*tetha_value), 0.0]"""

    # |----------------------------------------------------------------------------|
    # |  Testing list set points of the curves surface of the intervertebral disc  |
    # |----------------------------------------------------------------------------|

    # Data set based on the Nicolini's article
    # top_external_curve_set_points 

    x_top_external = [17.15469348659004, 17.999521072796938, 18.891283524904217, 19.876915708812263, 20.627873563218394, 
         21.378831417624525, 22.223659003831415, 22.88074712643678, 23.397030651340998, 23.866379310344826, 
         24.241858237547895, 24.429597701149426, 24.241858237547895, 24.241858237547895, 24.00718390804598, 
         23.819444444444443, 23.44396551724138, 22.974616858237546, 22.5522030651341, 22.176724137931032, 
         21.566570881226056, 21.003352490421456, 20.393199233716473, 19.783045977011497, 18.844348659003835, 
         18.281130268199234, 17.436302681992338, 16.544540229885058, 15.605842911877396, 14.479406130268202, 
         13.49377394636015, 12.41427203065134, 11.52250957854406, 10.255268199233718, 9.175766283524908, 
         8.09626436781609, 7.063697318007662, 5.796455938697317, 4.529214559386972, 3.4027777777777786, 
         1.994731800766285, 0.9152298850574709, -0.49281609195402254, -1.6661877394636022, -2.8864942528735646, 
         -4.200670498084293, -5.467911877394634, -6.735153256704979, -7.814655172413794, -8.941091954022989, 
         -10.067528735632184, -11.006226053639846, -12.179597701149426, -13.118295019157088, -14.291666666666666, 
         -15.136494252873563, -16.169061302681992, -17.060823754789272, -18.046455938697317, -18.84434865900383, 
         -19.595306513409962, -20.34626436781609, -20.90948275862069, -21.566570881226053, -22.035919540229884, 
         -22.599137931034484, -23.115421455938698, -23.397030651340998, -23.77250957854406, -24.101053639846743, 
         -24.288793103448278, -24.52346743295019, -24.52346743295019, -24.24185823754789, -23.913314176245212, 
         -23.537835249042146, -22.833812260536398, -22.082854406130267, -21.37883141762452, -20.34626436781609, 
         -19.501436781609193, -18.51580459770115, -17.530172413793103, -16.40373563218391, -15.371168582375478, 
         -14.338601532567049, -13.259099616858238, -12.038793103448276, -11.006226053639846, -9.738984674329501, 
         -8.706417624521073, -7.579980842911876, -6.453544061302683, -5.514846743295021, -4.670019157088124, 
         -3.6374521072796924, -2.7926245210727956, -1.900862068965516, -0.8682950191570882, 0.25814176245210874, 
         1.0090996168582365, 1.994731800766285, 2.98036398467433, 3.825191570881227, 4.904693486590038, 
         5.796455938697317, 6.594348659003831, 7.814655172413794, 8.800287356321839, 9.973659003831415, 
         11.053160919540232, 12.132662835249043, 13.118295019157088, 14.010057471264368, 15.183429118773944, 
         15.981321839080458]


    y_top_external = [14.876436781609197, 14.30057471264368, 13.772701149425288, 13.100862068965519, 12.42902298850575, 
         11.709195402298853, 10.749425287356324, 9.9816091954023, 9.069827586206898, 7.822126436781609, 
         6.86235632183908, 5.7106321839080465, 4.462931034482761, 3.311206896551724, 2.1594827586206904, 
         1.1037356321839091, -0.0959770114942522, -1.1997126436781596, -2.399425287356321, -3.311206896551724, 
         -4.510919540229883, -5.422701149425286, -6.2864942528735615, -7.2462643678160905, -8.158045977011493, 
         -8.973850574712642, -9.83764367816092, -10.60545977011494, -11.229310344827585, -11.85316091954023, 
         -12.333045977011494, -12.908908045977011, -13.340804597701148, -13.820689655172412, -14.204597701149424, 
         -14.588505747126437, -15.068390804597701, -15.404310344827586, -15.644252873563218, -15.932183908045976, 
         -16.124137931034483, -16.460057471264367, -16.508045977011495, -16.316091954022987, -16.124137931034483, 
         -15.788218390804596, -15.596264367816092, -15.260344827586206, -14.972413793103447, -14.348563218390805, 
         -13.964655172413792, -13.436781609195402, -12.956896551724137, -12.477011494252872, -11.85316091954023, 
         -11.325287356321837, -10.845402298850573, -10.125574712643678, -9.309770114942527, -8.541954022988504, 
         -7.582183908045977, -6.622413793103448, -5.662643678160919, -4.558908045977011, -3.551149425287356, 
         -2.3034482758620687, -1.1037356321839074, 0, 1.151724137931037, 2.3994252873563227, 3.647126436781612, 
         4.84683908045977, 6.238505747126439, 7.4382183908046, 8.589942528735634, 9.933620689655175, 
         10.845402298850576, 11.85316091954023, 12.716954022988507, 13.340804597701151, 14.01264367816092, 
         14.684482758620693, 15.212356321839081, 15.932183908045982, 16.31609195402299, 16.747988505747127, 
         16.93994252873563, 17.27586206896552, 17.419827586206896, 17.515804597701152, 17.56379310344828, 
         17.515804597701152, 17.371839080459768, 17.323850574712647, 17.27586206896552, 17.035919540229887, 
         16.98793103448276, 16.98793103448276, 16.891954022988504, 16.747988505747127, 16.795977011494255, 
         16.98793103448276, 16.843965517241383, 17.035919540229887, 17.131896551724136, 17.179885057471264, 
         17.22787356321839, 17.22787356321839, 17.22787356321839, 17.22787356321839, 17.083908045977015, 
         16.795977011494255, 16.7, 16.172126436781614, 15.884195402298854, 15.452298850574717]

   

    z_top_external = [14.0 for i in range(len(x_top_external))]

    # top_internal_curve_set_points

    x_top_internal = [12.41427203065134, 13.118295019157088, 13.587643678160923, 14.150862068965516, 14.714080459770116, 
         15.183429118773944, 15.699712643678161, 15.981321839080458, 16.21599616858238, 16.356800766283527, 
         16.450670498084293, 16.356800766283527, 16.309865900383144, 16.122126436781606, 15.934386973180075, 
         15.652777777777779, 15.3242337164751, 14.995689655172413, 14.573275862068968, 14.244731800766282, 
         13.86925287356322, 13.446839080459768, 13.024425287356323, 12.508141762452105, 11.944923371647512, 
         11.428639846743295, 10.818486590038312, 10.208333333333336, 9.55124521072797, 8.941091954022987, 
         8.330938697318011, 7.673850574712645, 7.01676245210728, 6.312739463601535, 5.561781609195403, 
         4.904693486590038, 4.247605363984675, 3.496647509578544, 2.6518199233716473, 1.9477969348659023, 
         1.2907088122605366, 0.5397509578544053, -0.25814176245210874, -0.9621647509578537, -1.7600574712643677, 
         -2.4640804597701162, -3.215038314176244, -3.8721264367816097, -4.623084291187741, -5.327107279693486, 
         -5.937260536398469, -6.641283524904214, -7.345306513409962, -7.908524904214559, -8.51867816091954, 
         -9.26963601532567, -9.785919540229886, -10.489942528735632, -11.100095785440613, -11.66331417624521, 
         -12.226532567049809, -12.930555555555555, -13.493773946360154, -13.869252873563218, -14.1977969348659, 
         -14.620210727969349, -15.042624521072797, -15.418103448275861, -15.793582375478927, -15.934386973180077, 
         -16.40373563218391, -16.497605363984675, -16.59147509578544, -16.685344827586206, -16.638409961685824, 
         -16.40373563218391, -16.169061302681992, -15.746647509578544, -15.277298850574713, -14.667145593869732, 
         -14.103927203065133, -13.44683908045977, -12.69588122605364, -12.085727969348659, -11.381704980842912, 
         -10.630747126436782, -9.692049808429118, -8.894157088122606, -8.09626436781609, -7.345306513409962, 
         -6.547413793103448, -5.655651340996169, -4.998563218390803, -4.388409961685824, -3.6374521072796924, 
         -2.6518199233716473, -1.9947318007662815, -1.2907088122605366, -0.6805555555555536, 0.02346743295019138, 
         0.9621647509578537, 1.6192528735632195, 2.370210727969347, 3.0742337164750957, 3.778256704980844, 
         4.482279693486589, 5.092432950191572, 5.984195402298852, 6.641283524904214, 7.439176245210728, 
         8.284003831417628, 8.894157088122604, 9.692049808429118, 10.255268199233718, 10.959291187739467, 
         11.804118773946364]
    

    y_top_internal = [11.085344827586209, 10.749425287356324, 10.26954022988506, 9.741666666666667, 9.213793103448278, 
         8.589942528735634, 7.918103448275865, 7.198275862068968, 6.430459770114943, 5.662643678160922, 
         4.8948275862068975, 4.031034482758621, 3.2632183908045995, 2.5433908045977027, 1.6795977011494259, 
         1.0557471264367813, 0.28793103448276014, -0.43189655172413666, -1.1997126436781596, -1.8715517241379303, 
         -2.7353448275862053, -3.263218390804596, -3.7431034482758605, -4.414942528735631, -4.894827586206896, 
         -5.422701149425286, -5.998563218390803, -6.382471264367815, -6.7183908045977, -7.054310344827586, 
         -7.294252873563217, -7.582183908045977, -7.870114942528735, -8.110057471264367, -8.254022988505746, 
         -8.493965517241378, -8.73390804597701, -8.87787356321839, -9.213793103448275, -9.309770114942527, 
         -9.309770114942527, -9.597701149425287, -9.453735632183907, -9.453735632183907, -9.309770114942527, 
         -9.165804597701149, -8.973850574712642, -8.781896551724138, -8.589942528735632, -8.397988505747126, 
         -8.158045977011493, -7.870114942528735, -7.534195402298849, -7.294252873563217, -6.958333333333332, 
         -6.766379310344826, -6.382471264367815, -6.046551724137931, -5.6146551724137925, -5.086781609195402, 
         -4.6548850574712635, -4.127011494252873, -3.455172413793102, -2.7833333333333314, -2.1594827586206886, 
         -1.3916666666666657, -0.6718390804597689, 0.19195402298850794, 0.9597701149425291, 1.6316091954023015, 
         2.687356321839083, 3.4071839080459796, 4.270977011494253, 5.230747126436782, 5.998563218390807, 
         6.86235632183908, 7.726149425287357, 8.39798850574713, 9.16580459770115, 9.83764367816092, 
         10.41350574712644, 10.893390804597704, 11.46925287356322, 11.805172413793105, 12.14109195402299, 
         12.42902298850575, 12.812931034482759, 12.860919540229887, 12.956896551724139, 13.244827586206899, 
         13.340804597701151, 13.292816091954023, 13.340804597701151, 13.244827586206899, 13.052873563218391, 
         12.956896551724139, 12.812931034482759, 12.812931034482759, 12.764942528735634, 12.716954022988507, 
         12.668965517241382, 12.620977011494254, 12.764942528735634, 12.908908045977014, 13.004885057471267, 
         12.860919540229887, 13.004885057471267, 13.052873563218391, 13.004885057471267, 12.908908045977014, 
         12.668965517241382, 12.572988505747126, 12.42902298850575, 12.093103448275862, 11.85316091954023, 
         11.421264367816093]
 
    z_top_internal = [14.0 for i in range(len(x_top_internal))]

    #

    top_internal= [x_top_internal, y_top_internal, z_top_internal]

    top_external = [x_top_external, y_top_external, z_top_external]


    bottom_internal = [deepcopy(x_top_internal), deepcopy(y_top_internal), [0.0 for i in range(len(x_top_internal))]]

    print(len(bottom_internal[0]))

    print(len(bottom_internal[2]))

    bottom_external = [deepcopy(x_top_external), deepcopy(y_top_external), [0.0 for i in range(len(x_top_external))]]

    # Finally, Calls the principal function to parametrize the disc geometry

    disc_geometry(top_internal, top_external, bottom_internal, bottom_external, 15)


    