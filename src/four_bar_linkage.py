import math
import numpy as np
class FourBarLinkage:
    # Parameter Check
    Linkage_Type = "Undefined"  # This will be either "Grashof" or "non-Grashof" after check_Parameter()
    geometric_Validity = True  # Bool: True or False (possible geometry)
    # Parameter to display in GUI
    Input_Link_Type = "Undefined" # Type of input linkage (e.g., 'crank', 'π-rocker', '0-rocker')
    Output_Link_Type = "Undefined" # Type of output linkage (e.g., 'rocker', 'π-rocker', 'crank', '0-rocker')

    # all parameters you need to calculate coordinates, default initializing
    # bars lengths
    AB = 0. # AB
    BC = 0. # BC
    CD = 0. # CD
    DA = 0.  # DA
    # input angle in degrees (vector AD to positive x achse)
    alpha = 0.
    # input angle in degrees (vector BC to negative x achse)
    beta = 0.
    # angle in degrees between ground bar and horizont
    theta = 0.
    # convert angle from degrees to radians
    alpha_rad = 0.
    theta_rad = 0.
    beta_rad  = 0.
    # limits for angle alpha
    alpha_lims = [0., 0.]
    alpha_rad_lims = [0., 0.]
    alpha_limited = True
    # limits for angle beta
    beta_lims = [0., 0.]
    beta_rad_lims = [0., 0.]
    # coupler positions
    coupler_position = 0. # 0% from DC midpoint towards C
    coupler_offset = 0. # 0% of DC length
    # all coordinates of conection points A,B,C,D,P
    A  = np.array([0.0, 0.0]) # coordinates of A are always (0,0)
    B  = np.array([0.0, 0.0])
    C = np.array([0.0, 0.0])  # C is chosen point for GUI
    C1 = np.array([0.0, 0.0]) # C1 is always with positive cross product
    C2 = np.array([0.0, 0.0]) # C2 is always with negative cross product
    C_last = np.array([0.0, 0.0]) # C before one iteration
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
        self.C_mode = 'C2'
        # initialize coordinates of connection points
        self.switch_C2_C1_180 = False
        self.switch_C2_C1_360 = False
        self.C2_C1_switched_last_time = False
        self.alpha_limited = True
        self.run()
        return



    # implement here geometry to calculate coordinates of all points from parameters (lengths, angles, ...)
    # this function will be called from GUI after updating some parameters to get coordinates for GUI animation
    def run(self):
        # calculate classification values
        self.calculate_Classification_Value()
        
        # check_Parameter
        self.check_Parameter()
        
        # update coordinates only if parameters are correct
        if not self.geometric_Validity:
            return

        # search Linkage Type
        self.find_Linkage_Type()

        # find_Linkage_Type
        self.find_Linkage_Type()

        # calculate limits
        self.calculate_alpha_lims()
        self.calculate_beta_lims()

        # calculate all coordinates A, B, C, D, P
        self.calculate_Point_Position()

        # calculate angle beta for the link BC with respect to the positive x-axis
        self.calculate_beta()

        self.C_last = self.C
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
        if V > 0:
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
        """
        Calculate the limit angles for the input link (alpha) of the four-bar linkage.
        Uses the law of cosines to determine the valid range of alpha, ensuring the linkage can form a closed quadrilateral.
        If the cosine value is out of the valid range ([-1, 1]), alpha limits are set to [0, 0].
        """

        # Calculate the effective lengths using the lengths of the linkage bars
        a_1 = self.BC + self.CD  # Combined length of BC and CD 
        a_2 = self.BC - self.CD  # Combined length of BC and CD 
        b = self.AB  # Length of input link AB
        c = self.DA  # Length of output link DA

        # Using the law of cosines to find cos(alpha limits)
        cos_alpha_lims_1 = (b ** 2 + c ** 2 - a_1 ** 2) / (2 * b * c)
        cos_alpha_lims_2 = (b ** 2 + c ** 2 - a_2 ** 2) / (2 * b * c)
        
        if abs(cos_alpha_lims_1) < 1.0:
            self.alpha_limited = True
            self.switch_C2_C1_180 = False
            self.switch_C2_C1_360 = False
            self.alpha_rad_lims = [-np.arccos(cos_alpha_lims_1) + self.theta_rad,
                                   np.arccos(cos_alpha_lims_1) + self.theta_rad]
            
            if abs(cos_alpha_lims_2) < 1.0:
                self.alpha_rad_lims[0] = np.arccos(cos_alpha_lims_2) + self.theta_rad
            else:
                if abs(abs(cos_alpha_lims_2) - 1.0) < 1e-12:
                    self.switch_C2_C1_360 = True
                
        else:
            self.switch_C2_C1_180 = False
            self.switch_C2_C1_360 = False
            if abs(abs(cos_alpha_lims_1) - 1.0) < 1e-12:
                self.switch_C2_C1_180 = True
            if abs(cos_alpha_lims_2) < 1.0:
                self.alpha_limited = True
                self.alpha_rad_lims = [np.arccos(cos_alpha_lims_2) + self.theta_rad,
                                       2*math.pi - np.arccos(cos_alpha_lims_2) + self.theta_rad]
            else:
                if abs(abs(cos_alpha_lims_2) - 1.0) < 1e-12:
                    self.switch_C2_C1_360 = True
                self.alpha_limited = False
                self.alpha_rad_lims = [0.0, 2*math.pi]
        self.alpha_lims = [math.degrees(self.alpha_rad_lims[0]), math.degrees(self.alpha_rad_lims[1])]
        return


    # calculate limits of angle beta
    def calculate_beta_lims(self):
        """
        Calculate the limit angles for the link BC with respect to the negative x-axis (beta).
        Uses the law of cosines to determine the valid range of beta, ensuring the linkage can form a closed quadrilateral.
        The sides of the triangle used are AD + DC, AB, and BC.
        """

        # Calculate the effective lengths of the sides of the triangle formed by the linkage bars
        a = self.DA + self.CD  # Combined length of AD and DC (link lengths between A->D and D->C)
        b = self.AB  # Length of input link AB
        c = self.BC  # Length of link BC

        # Using the law of cosines to find cos(beta limits)
        cos_beta_lims = (b**2 + c**2 - a**2) / (2 * b * c)

        # Check if the calculated cosine value is valid (cosine should be between -1 and 1)
        if np.abs(cos_beta_lims) >= 1:
            # If cosine value is out of bounds, there is no cos limits or configuration is invalid,
            # but we validate it another way
            self.beta_rad_lims = [-math.pi, math.pi]
            self.beta_lims = [-180.0, 180.0]
        else:
            # If cosine value is valid, calculate the angle limits in radians
            # Add or subtract arccos to get the limits based on the base angle theta_rad
            self.beta_rad_lims = [
                -np.arccos(cos_beta_lims) - self.theta_rad,  # Lower limit of beta in radians
                np.arccos(cos_beta_lims) - self.theta_rad    # Upper limit of beta in radians
            ]

            # Convert the radian limits to degrees and store in beta_lims
            self.beta_lims = [
                math.degrees(self.beta_rad_lims[0]),  # Lower limit in degrees
                math.degrees(self.beta_rad_lims[1])   # Upper limit in degrees
            ]
        return


    # calculate angle beta
    def calculate_beta(self):
        """
        Calculate the angle (beta) between the vector BC (from point B to point C) and the positive x-axis.
        """
        # Calculate the vector from point B to point C
        BC_vector = self.C - self.B
        # Calculate the magnitude (length) of the BC vector
        BC_length = np.linalg.norm(BC_vector)
        # Define the unit vector along the x-axis (1, 0)
        x_axis_vector = np.array([-1, 0])  # normalized vector of positive x-axis
        # Calculate the dot product between BC_vector and the x_axis_vector
        dot_product = np.dot(BC_vector, x_axis_vector)
        # Calculate the cosine of the angle using the dot product formula:
        # cos(beta) = (BC_vector • x_axis_vector) / (|BC_vector| * |x_axis_vector|)    ----- |x_axis_vector| = 1
        cos_beta = dot_product / BC_length
        # Check the cosine value is within the valid range [-1, 1]
        cos_beta = np.clip(cos_beta, -1, 1)
        # Calculate the angle in radians using arccos (inverse cosine)
        self.beta_rad = np.arccos(cos_beta)
        # Convert the angle from radians to degrees
        self.beta = math.degrees(self.beta_rad)
        return



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
        BD_unit_vector = (self.B - self.A)/self.AB
        if BD_length > 10**-12:
            BD_unit_vector = BD_vector / BD_length
        # calculate normal vector , which is orthogonal to BD
        normal_vector_toBD = np.array([-BD_unit_vector[1], BD_unit_vector[0]])

        # length of the edges of triangle
        a = self.BC
        b = self.CD
        c = BD_length

        #Height h is calculated using Heron's formula to find the area of the triangle, and then using the area formula.
        s = (a + b + c) / 2
        # clip area_2 to positiv values to solve some problems with floating point precision
        area_2 = max(s * (s - a) * (s - b) * (s - c), 0.0)
        area = np.sqrt(area_2)
        h = 0.0
        if c > 10**-12:
            h = 2 * area / c

        # Calculate the distance from point C to BD (the projection length along the direction of BD)
        projection_length = np.sqrt(self.BC ** 2 - h ** 2)
        
        # to choose sign of projection
        cos_CBD = (self.BC**2 + c**2 - self.CD**2)/(2*self.BC*c)
        if cos_CBD < 0:
            projection_length = -projection_length

        # Two possible positions for point C
        C1 = self.B + projection_length * BD_unit_vector + h * normal_vector_toBD
        C2 = self.B + projection_length * BD_unit_vector - h * normal_vector_toBD

        self.C1 = C1
        self.C2 = C2
        
        # choose C1 or C2
        if self.C_mode=='C2':
            self.C = self.C2
        else:
            self.C = self.C1
            
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
        Q = Middle_CD + self.coupler_position * DC_vector

        # Calculate the normal vector perpendicular to CD
        normal_vector_toCD = np.array([-DC_unit_vector[1], DC_unit_vector[0]])

        # Calculate the offset distance for point P
        offset_distance = self.coupler_offset * DC_length
        
        self.P = Q + offset_distance * normal_vector_toCD

        return





    # update alpha for animation
    def animation_alpha(self):
        """
        Update alpha for new iteration of the animation.

        The motion of alpha alternates direction when it hits the upper or lower limit of alpha_lims.
        """

        # Initialize iteration state (0 for increasing, 1 for decreasing)
        if not hasattr(self, 'direction'):  # Check if direction attribute exists
            self.direction = 0  # 0 means increasing alpha, 1 means decreasing alpha
            
        C2_C1_switched_pre_last_time = self.C2_C1_switched_last_time

        # Update alpha based on current direction
        if self.direction == 0:  # Increasing alpha
            self.alpha += self.alpha_velocity * self.t
            self.alpha_rad = math.radians(self.alpha)

            # Check if alpha exceeds the upper limit
            if self.alpha_limited and self.alpha >= self.alpha_lims[1]:
                # Set alpha to the upper limit
                self.alpha = self.alpha_lims[1]
                self.alpha_rad = self.alpha_rad_lims[1]
                # Switch direction to decreasing
                self.direction = 1
                # switch C1 and C2
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            if self.switch_C2_C1_360 and ((self.alpha - self.theta >= 0.0 and self.alpha - self.theta - self.alpha_velocity * self.t <= 0.0) or \
                                          (self.alpha - self.theta >= 360.0 and self.alpha - self.theta - self.alpha_velocity * self.t <= 360.0)):
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            if self.switch_C2_C1_180 and self.alpha - self.theta >= 180.0 and self.alpha - self.theta - self.alpha_velocity * self.t <= 180.0:
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            # alpha is not limited values have to stay from 0 to 360
            if not self.alpha_limited and self.alpha >= 360.0:
                self.alpha = self.alpha - 360.0
                self.alpha_rad = math.radians(self.alpha)
                

        elif self.direction == 1:  # Decreasing alpha
            self.alpha -= self.alpha_velocity * self.t
            self.alpha_rad = math.radians(self.alpha)

            # Check if alpha falls below the lower limit
            if self.alpha_limited and self.alpha <= self.alpha_lims[0]:
                # Set alpha to the lower limit
                self.alpha = self.alpha_lims[0]
                self.alpha_rad = self.alpha_rad_lims[0]
                # Switch direction to increasing
                self.direction = 0
                # switch C1 and C2
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
            
                
            if self.switch_C2_C1_180 and self.alpha - self.theta <= 180.0 and self.alpha - self.theta + self.alpha_velocity * self.t >= 180.0:
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            if self.switch_C2_C1_360 and self.alpha - self.theta <= 0.0 and self.alpha - self.theta + self.alpha_velocity * self.t >= 0.0:
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            # alpha is not limited values have to stay from 0 to 360
            if not self.alpha_limited and self.alpha <= 0.0:
                self.alpha = self.alpha + 360.0
                self.alpha_rad = math.radians(self.alpha)
                
        # if didn't switch this time
        if C2_C1_switched_pre_last_time:
            self.C2_C1_switched_last_time = False
        return
    
    # function to switch between C1 and C2, call only by alpha_lim
    def switch_C2_C1(self):
        if self.C_mode == 'C2':
            self.C_mode = 'C1'
        else:
            self.C_mode = 'C2'
        