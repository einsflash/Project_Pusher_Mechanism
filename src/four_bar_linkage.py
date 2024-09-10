import math
import numpy as np
import pandas as pd
class FourBarLinkage:
    # Parameter Check
    Linkage_Type = "Undefined"  # This will be either "Grashof" or "non-Grashof" after check_Parameter()
    geometric_Validity = True  # Bool: True or False (possible geometry)
    # Parameter to display in GUI
    Input_Link_Type = "Undefined" # Type of input linkage (e.g., 'crank', 'π-rocker', '0-rocker')
    Output_Link_Type = "Undefined" # Type of output linkage (e.g., 'rocker', 'π-rocker', 'crank', '0-rocker')

    # Record Trajectories for Animation ==== function is update_trajectory
    trajectory_df = pd.DataFrame(columns=[
        'A_x', 'A_y', 'B_x', 'B_y', 'C_x', 'C_y',
        'D_x', 'D_y', 'P_x', 'P_y'
    ])

    # all parameters you need to calculate coordinates, default initializing
    # bars lengths
    AB = 0. # AB
    BC = 0. # BC
    CD = 0. # CD
    DA = 0.  # DA
    # input angle in degrees
    alpha = 0.
    # angle in degrees between ground bar and horizont
    theta = 0.
    # convert angle from degrees to radians
    alpha_rad = 0.
    theta_rad = 0.
    # limits for angle alpha
    alpha_lims = [0., 0.]
    alpha_rad_lims = [0., 0.]
    # coupler positions
    coupler_position = 0. # 0% from DC midpoint towards C
    coupler_offset = 0. # 0% of DC length
    # all coordinates of conection points A,B,C,D,P
    A  = np.array([0.0, 0.0]) # coordinates of A are always (0,0)
    B  = np.array([0.0, 0.0])
    C = np.array([0.0, 0.0])  # C is chosen point for GUI
    C1 = np.array([0.0, 0.0]) # C1 is always with positive cross product
    C2 = np.array([0.0, 0.0]) # C2 is always with negative cross product
    D  = np.array([0.0, 0.0])
    P = np.array([0.0, 0.0])  # P is chosen point for GUI
    P1  = np.array([0.0, 0.0]) # P1 is always with positive cross product
    P2 = np.array([0.0, 0.0])  # P2 is always with negative cross product

    # you can classify motions using following values
    T1 = 0. # AB + CD - BC - DA
    T2 = 0. # BC + AB - CD - DA
    T3 = 0. # CD + BC - AB - DA
    L =  0.  # AB + BC + CD + DA
    # consult https://en.wikipedia.org/wiki/Four-bar_linkage, all values are like in wikipedia, and in four_bar_linkage.png

    # timeinterval (second)
    t = 0.01
    # angular velocity per second
    alpha_velocity = 0.
    # this is constructor that will be used from GUI to initialize all needed parameters,
    # lengths, angles, coordinated of fixed points and so one
    def __init__(self, AB, BC, CD, DA, alpha, theta, coupler_position, coupler_offset , timeinterval , alpha_velocity):
        # initialize all parameters
        self.AB = AB
        self.BC = BC
        self.CD = CD
        self.DA = DA
        self.alpha = alpha
        self.theta = theta
        self.alpha_rad = math.radians(alpha)
        self.theta_rad = math.radians(theta)
        self.coupler_position = coupler_position
        self.coupler_offset = coupler_offset
        self.t = timeinterval
        self.alpha_velocity = alpha_velocity
        # initialize coordinates of connection points
        self.run()
        return



    # implement here geometry to calculate coordinates of all points from parameters (lengths, angles, ...)
    # this function will be called from GUI after updating some parameters to get coordinates for GUI animation
    def run(self):
        # calculate classification values
        self.calculate_Classification_Value()
        
        # check_Parameter
        self.check_Parameter

        # find_Linkage_Type
        self.find_Linkage_Type()

        # calculate alpha limits
        self.calculate_alpha_lims()

        # calculate all coordinates A, B, C, D, P
        self.calculate_Point_Position()
        return


        
    # add some functions, if you need it to implement run function. Keep it simple, 
    # split run() in subfunctions, that you will call from run().
    # The important thing is that GUI needs to call only run() to update coordinates!

    """ 
    check Parameter 
    calculate two values ---- Grashof index G and Validity index V
    Linkage_Type and geometric_Validity is for GUI
    """
    def check_Parameter(self):
        # Determine the longest (l) and shortest (s) sides
        lengths = [self.AB, self.BC, self.CD, self.DA]
        l = max(lengths)
        s = min(lengths)

        # Find the remaining two sides (p, q)
        lengths.remove(l)
        lengths.remove(s)
        p, q = lengths

        # Calculate Grashof index G and Validity index V
        G = l + s - p - q
        V = l - s - p - q

        # Determine linkage type based on Grashof index
        if G < 0:
            self.Linkage_Type = "non-Grashof"
        else:
            self.Linkage_Type = "Grashof"

        # Determine geometric validity based on Validity index
        if V < 0:
            self.geometric_Validity = False  # impossible geometry
        else:
            self.geometric_Validity = True  # possible geometry

        return


    """
    Determines the types of input and output linkages based on the values of T1, T2, and T3.
    Sets the input linkage type in self.Input_Link_Type 
    and the output linkage type in self.Output_Link_Type.
    """
    def find_Linkage_Type(self):
        # Define a dictionary that maps (T1, T2, T3) to (Input α, Output β)
        linkage_map = {
            ('+', '+', '+'): ('crank', 'rocker'),
            ('0', '+', '+'): ('crank', 'π-rocker'),
            ('-', '+', '+'): ('π-rocker', 'π-rocker'),
            ('+', '0', '+'): ('crank', '0-rocker'),
            ('0', '0', '+'): ('crank', 'crank'),
            ('-', '0', '+'): ('crank', 'crank'),
            ('+', '-', '+'): ('π-rocker', '0-rocker'),
            ('0', '-', '+'): ('crank', 'crank'),
            ('-', '-', '+'): ('crank', 'crank'),

            ('+', '+', '0'): ('crank', 'π-rocker'),
            ('0', '+', '0'): ('crank', 'π-rocker'),
            ('-', '+', '0'): ('π-rocker', 'π-rocker'),
            ('+', '0', '0'): ('crank', 'crank'),
            ('0', '0', '0'): ('crank', 'crank'),
            ('-', '0', '0'): ('crank', 'crank'),
            ('+', '-', '0'): ('π-rocker', 'crank'),
            ('0', '-', '0'): ('crank', 'crank'),
            ('-', '-', '0'): ('crank', 'crank'),

            ('+', '+', '-'): ('0-rocker', 'π-rocker'),
            ('0', '+', '-'): ('0-rocker', 'π-rocker'),
            ('-', '+', '-'): ('rocker', 'rocker'),
            ('+', '0', '-'): ('0-rocker', 'crank'),
            ('0', '0', '-'): ('0-rocker', 'crank'),
            ('-', '0', '-'): ('0-rocker', '0-rocker'),
            ('+', '-', '-'): ('rocker', 'crank'),
            ('0', '-', '-'): ('0-rocker', 'crank'),
            ('-', '-', '-'): ('0-rocker', '0-rocker')
        }

        # Change the values of T1, T2, T3 into strings for lookup in the dictionary
        T1_str = '+' if self.T1 > 0 else '0' if self.T1 == 0 else '-'
        T2_str = '+' if self.T2 > 0 else '0' if self.T2 == 0 else '-'
        T3_str = '+' if self.T3 > 0 else '0' if self.T3 == 0 else '-'

        # Find the corresponding linkage types from the dictionary
        input_alpha, output_beta = linkage_map.get((T1_str, T2_str, T3_str), ('Undefined', 'Undefined'))

        # Set the linkage types as class variables
        self.Input_Link_Type = input_alpha  # String for input α type
        self.Output_Link_Type = output_beta  # String for output β type

        return



    """ calculate classification values according to given 4 edges"""
    def calculate_Classification_Value(self):
        self.T1 = self.AB + self.CD - self.BC - self.DA
        self.T2 = self.BC + self.AB - self.CD - self.DA
        self.T3 = self.CD + self.BC - self.AB - self.DA
        self.L =  self.AB + self.BC + self.CD + self.DA
        return

    """ calculate 4 edges according to given classification values """
    def calculate_Edge_Value(self):
        self.AB = (self.L / 4) + (self.T1 / 4) + (self.T2 / 4) - (self.T3 / 4)
        self.BC = (self.L / 4) - (self.T1 / 4) + (self.T2 / 4) + (self.T3 / 4)
        self.CD = (self.L / 4) + (self.T1 / 4) - (self.T2 / 4) + (self.T3 / 4)
        self.DA = (self.L / 4) - (self.T1 / 4) - (self.T2 / 4) - (self.T3 / 4)
        return
    
    
    # calculate limits of angle alpha
    def calculate_alpha_lims(self):
        # using law of cosines
        a = self.BC + self.CD
        b = self.AB
        c = self.DA
        cos_alpha_lims = (b**2 + c**2 - a**2)/(2*b*c)
        if np.abs(cos_alpha_lims) >= 1:
            self.alpha_rad_lims = [0, 0]
        else:
            self.alpha_rad_lims = [-np.arccos(cos_alpha_lims) + self.theta_rad, np.arccos(cos_alpha_lims) + self.theta_rad]
            self.alpha_lims = [math.degrees(self.alpha_rad_lims[0]), math.degrees(self.alpha_rad_lims[1])]
    


    # calculate position with given angle
    def calculate_Point_Position(self):
        # A and B are static

        # calculate B
        B_x = np.cos(self.theta_rad) * self.AB
        B_y = np.sin(self.theta_rad) * self.AB
        self.B = np.array([B_x, B_y])

        # calculate D
        D_x = np.cos(self.alpha_rad) * self.DA
        D_y = np.sin(self.alpha_rad) * self.DA
        self.D = np.array([D_x, D_y])

        # calculate C1 and C2
        self.calculate_C_Position()

        # calculate P
        self.calculate_P_Position()

        return



    # calculate position of point C (2 possible points)
    def calculate_C_Position(self):
        ### calculate C (2 possible position)
            # calculate vector BD
            BD_vector = self.D - self.B
            BD_length = np.linalg.norm(BD_vector)
            BD_unit_vector = BD_vector / BD_length

            # calculate normal vector , which is orthogonal to BD
            normal_vector_toBD = np.array([-BD_unit_vector[1], BD_unit_vector[0]])

            # length of the edges of triangle
            a = self.BC
            b = self.CD
            c = BD_length

            #Height h is calculated using Heron's formula to find the area of the triangle, and then using the area formula.
            s = (a + b + c) / 2
            area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            h = 2 * area / c


            # Calculate the distance from point C to BD (the projection length along the direction of BD)
            projection_length = np.sqrt(self.BC ** 2 - h ** 2)

            # Two possible positions for point C
            C1 = self.B + projection_length * BD_unit_vector + h * normal_vector_toBD
            C2 = self.B + projection_length * BD_unit_vector - h * normal_vector_toBD

            """ Choose between C1 and C2 """
            ###

            # calculate vector BC1
            #BC1_vector = self.C1 - self.B

            # calculate cross product to choose C between C1 and C2
            #cross_product_1 = BD_vector[0] * BC1_vector[1] - BD_vector[1] * BC1_vector[0]

            # choose C according to cross product result
            #if cross_product_1 > 0:
            #    C_positive, C_negative = C1, C2
            #else:
            #    C_positive, C_negative = C2, C1

            # store results, ensure that cross product of C1 is always positive
            #self.C1 = C_positive
            #self.C2 = C_negative
            self.C1 = C1
            self.C2 = C2
            
            self.C = self.C2
            return



    # calculate position of point C (2 possible points)
    def calculate_P_Position(self):
        # calculate middle point of CD
        Middle_CD = (self.C + self.D) / 2

        # calculate vector DC
        DC_vector = self.C - self.D
        DC_length = np.linalg.norm(DC_vector)
        DC_unit_vector = DC_vector / DC_length

        # calculate position of Q (Q on CD and pq orthogonal to CD)
        Q = Middle_CD + (self.coupler_position / 2) * DC_vector

        # Calculate the normal vector perpendicular to CD
        normal_vector_toCD = np.array([-DC_unit_vector[1], DC_unit_vector[0]])

        # Calculate the offset distance for point P
        offset_distance = self.coupler_offset * DC_length

        # Two possible positions for point P
        #P1 = Q + offset_distance * normal_vector_toCD
        #P2 = Q - offset_distance * normal_vector_toCD

        # Use cross product to choose the correct position for point P
        #DQ_vector = Q - self.D  # Calculate vector DQ
        #DP1_vector = P1 - self.D  # Calculate vector DP1
        #cross_product_1 = DQ_vector[0] * DP1_vector[1] - DQ_vector[1] * DP1_vector[0]

        # Choose P point based on the cross product result
        #if cross_product_1 > 0:
        #    P_positive, P_negative = P1, P2
        #else:
        #    P_positive, P_negative = P2, P1

        #ensure that P1 is always with positive cross product
        #self.P1 = P_positive
        #self.P2 = P_negative

        # Add the condition to select self.P for GUI
        #if offset_distance >= 0:
        #    self.P = self.P1
        #else:
        #    self.P = self.P2
        self.P = Q + offset_distance * normal_vector_toCD

        return



    def update_trajectory(self):
        """Update the points' trajectory and add it to the DataFrame."""
        new_data = {
            'A_x': self.A[0], 'A_y': self.A[1],
            'B_x': self.B[0], 'B_y': self.B[1],
            'C_x': self.C[0], 'C_y': self.C[1],
            'D_x': self.D[0], 'D_y': self.D[1],
            'P_x': self.P[0], 'P_y': self.P[1],
        }
        self.trajectory_df = self.trajectory_df.append(new_data, ignore_index=True)
        return



    #calculate coordinates after iteration
    def Iteration_for_Animation(self, trace: bool):
        """
        Perform an iteration for the animation.

        Parameters:
        trace (bool): If True, enables tracking of the points' trajectory.
        """

        self.alpha = self.alpha + self.alpha_velocity * self.t
        self.run()

        if trace:
            # start tracing and record trajectory
            self.update_trajectory()

        return

    def Iteration_for_Animation_Mouse(self, trace: bool, alpha):
        """
        Perform an iteration for the animation.

        With Mouseclick! And alpha is direction of mouse, which will be input from GUI.

        Parameters:
        trace (bool): If True, enables tracking of the points' trajectory.
        """

        self.alpha = alpha
        self.run()

        if trace:
            # start tracing and record trajectory
            self.update_trajectory()

        return