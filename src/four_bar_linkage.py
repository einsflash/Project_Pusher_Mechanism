import math
import numpy as np
class FourBarLinkage:
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
        self.init_default_values()
        # calculate all positions
        self.run()
        return

    # default values initialization
    def init_default_values(self):
        # values for animation (when to switch C2 and C1)
        self.switch_C2_C1_180 = False
        self.switch_C2_C1_360 = False
        self.C2_C1_switched_last_time = False
        self.direction = 0
        
        # Parameter Check
        self.Linkage_Type = "Undefined"  # This will be either "Grashof" or "non-Grashof" after check_Parameter()
        self.geometric_Validity = True  # Bool: True or False (possible geometry)
        # Parameter to display in GUI
        self.Input_Link_Type = "Undefined" # Type of input linkage (e.g., 'crank', 'π-rocker', '0-rocker')
        self.Output_Link_Type = "Undefined" # Type of output linkage (e.g., 'rocker', 'π-rocker', 'crank', '0-rocker')
        
        # limits for angle alpha
        self.alpha_lims = [0., 0.]
        self.alpha_rad_lims = [0., 0.]
        self.alpha_limited = True
        
        # all coordinates of conection points A,B,C,D,P
        self.A  = np.array([0.0, 0.0]) # coordinates of A are always (0,0)
        self.B  = np.array([0.0, 0.0])
        self.C = np.array([0.0, 0.0])  # C is chosen point for GUI
        self.C1 = np.array([0.0, 0.0])
        self.C2 = np.array([0.0, 0.0])
        self.D  = np.array([0.0, 0.0])
        self.P = np.array([0.0, 0.0])
    
        # classification values consult https://en.wikipedia.org/wiki/Four-bar_linkage
        self.T1 = 0. # AB + CD - BC - DA
        self.T2 = 0. # BC + AB - CD - DA
        self.T3 = 0. # CD + BC - AB - DA
        self.L =  0. # AB + BC + CD + DA

    # implement geometry to calculate coordinates of all points from parameters
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

        # calculate alpha limits
        self.calculate_alpha_lims()

        # calculate all coordinates A, B, C, D, P
        self.calculate_Point_Position()
        
        return

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

    def find_Linkage_Type(self):
        """
        Determines the types of input and output linkages based on the values of T1, T2, and T3.
        Sets the input linkage type in self.Input_Link_Type 
        and the output linkage type in self.Output_Link_Type.
        """
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

    def calculate_Classification_Value(self):
        """ calculate classification values according to given 4 edges"""
        self.T1 = self.AB + self.CD - self.BC - self.DA
        self.T2 = self.BC + self.AB - self.CD - self.DA
        self.T3 = self.CD + self.BC - self.AB - self.DA
        self.L =  self.AB + self.BC + self.CD + self.DA
        return

    def calculate_Edge_Value(self):
        """ calculate 4 edges according to given classification values """
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
        # upper limit
        cos_alpha_lims_1 = (b ** 2 + c ** 2 - a_1 ** 2) / (2 * b * c)
        # lower limit
        cos_alpha_lims_2 = (b ** 2 + c ** 2 - a_2 ** 2) / (2 * b * c)
        
        # compare cos with one with some precision of 1e-10
        if abs(cos_alpha_lims_1) < 1.0 - 1e-10:
            self.alpha_limited = True
            # do not switch additionally by 180 and 360 degrees
            self.switch_C2_C1_180 = False
            self.switch_C2_C1_360 = False
            self.alpha_rad_lims = [-np.arccos(cos_alpha_lims_1) + self.theta_rad,
                                   np.arccos(cos_alpha_lims_1) + self.theta_rad]
            
            if abs(cos_alpha_lims_2) < 1.0 - 1e-10:
                self.alpha_rad_lims[0] = np.arccos(cos_alpha_lims_2) + self.theta_rad
            else:
                if abs(abs(cos_alpha_lims_2) - 1.0) < 1e-10:
                    # switch additionally by 360 degrees
                    self.switch_C2_C1_360 = True
                
        else:
            # do not switch additionally by 180 and 360 degrees
            self.switch_C2_C1_180 = False
            self.switch_C2_C1_360 = False
            if abs(abs(cos_alpha_lims_1) - 1.0) < 1e-10:
                # switch additionally by 180 degrees
                self.switch_C2_C1_180 = True
            if abs(cos_alpha_lims_2) < 1.0 - 1e-10:
                self.alpha_limited = True
                self.alpha_rad_lims = [np.arccos(cos_alpha_lims_2) + self.theta_rad,
                                       2*math.pi - np.arccos(cos_alpha_lims_2) + self.theta_rad]
            else:
                if abs(abs(cos_alpha_lims_2) - 1.0) < 1e-10:
                    # switch additionally by 360 degrees
                    self.switch_C2_C1_360 = True
                self.alpha_limited = False
                self.alpha_rad_lims = [0.0, 2*math.pi]
        self.alpha_lims = [math.degrees(self.alpha_rad_lims[0]), math.degrees(self.alpha_rad_lims[1])]
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

        # calculate C
        self.calculate_C_Position()

        # calculate P
        self.calculate_P_Position()

        return
    
    # calculate position of point C (2 possible points)
    def calculate_C_Position(self):
        # calculate vectors BD, BA, BC
        BD_vector = self.D - self.B
        BD_length = np.linalg.norm(BD_vector)
        BA_vector = self.A - self.B
        BC_vector = self.C - self.B
        # if BD_length is zero, unit vector is also zero
        BD_unit_vector = np.array([0.0, 0.0])
        if BD_length > 10**-12:
            BD_unit_vector = BD_vector / BD_length
        # calculate normal vector , which is orthogonal to BD
        normal_vector_toBD = np.array([-BD_unit_vector[1], BD_unit_vector[0]])
        # if BD vector is zero one, normal is along BA with sign depending on previous C
        if BD_length < 10**-12:
            normal_vector_toBD = np.sign(np.dot(BA_vector, BC_vector))*BA_vector/self.AB
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
        # if BD vector is zero, h is equal to BC
        if c <= 10**-12:
            h = self.BC
        # Calculate the distance from point C to BD (the projection length along the direction of BD)
        projection_length = np.sqrt(self.BC ** 2 - h ** 2)
        
        # to choose sign of projection find angle between AB and BD
        cos_CBD = 1.0
        if c > 10**-12:
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
            
        # if BD vector is zero C=C1 independing on C1 and C2 to not observe any jumps
        if BD_length < 10**-12:
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
                # switch C1 and C2 if didnt switch last time
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                
            # switch by 0 and 360 degrees if needed
            if self.switch_C2_C1_360 and ((self.alpha - self.theta >= -10**-12 and \
                                           self.alpha - self.theta - self.alpha_velocity * self.t <= 10**-12) or \
                                          (self.alpha - self.theta >= 360.0 and \
                                           self.alpha - self.theta - self.alpha_velocity * self.t <= 360.0)):
                # switch C1 and C2 if didnt switch last time
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
            
            # switch by 180 degrees if needed
            if self.switch_C2_C1_180 and self.alpha - self.theta >= 180.0 and \
               self.alpha - self.theta - self.alpha_velocity * self.t <= 180.0:
                # switch C1 and C2 if didnt switch last time
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
                # switch C1 and C2 if didnt switch last time
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
            
            # switch by 180 degrees if needed
            if self.switch_C2_C1_180 and self.alpha - self.theta <= 180.0 and \
               self.alpha - self.theta + self.alpha_velocity * self.t >= 180.0:
                # switch C1 and C2 if didnt switch last time
                if not self.C2_C1_switched_last_time: 
                    self.switch_C2_C1()
                    self.C2_C1_switched_last_time = True
                    
            # switch by 360 degrees if needed  
            if self.switch_C2_C1_360 and self.alpha - self.theta <= 10**-12 and \
               self.alpha - self.theta + self.alpha_velocity * self.t >= -10**-12:
                # switch C1 and C2 if didnt switch last time
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
        