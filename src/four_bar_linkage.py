import math
import numpy as np
import pandas as pd
class FourBarLinkage:
    # Record Trajectories for Animation ==== function is update_trajectory
    trajectory_df = pd.DataFrame(columns=[
        'A_x', 'A_y', 'B_x', 'B_y', 'C1_x', 'C1_y', 'C2_x', 'C2_y',
        'D_x', 'D_y', 'P1_x', 'P1_y', 'P2_x', 'P2_y'
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
    # coupler positions
    coupler_position = 0. # 0% from DC midpoint towards C
    coupler_offset = 0. # 0% of DC length
    # all coordinates of conection points A,B,C,D,P
    A  = np.array([0.0, 0.0]) # coordinates of A are always (0,0)
    B  = np.array([0.0, 0.0])
    C1 = np.array([0.0, 0.0]) # C1 is always with positive cross product
    C2 = np.array([0.0, 0.0]) # C2 is always with negative cross product
    D  = np.array([0.0, 0.0])
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
        self.calculate_Classification_Values()

        # calculate all coordinates A, B, C, D, P
        self.calculate_Point_Position()
        return


        
    # add some functions, if you need it to implement run function. Keep it simple, 
    # split run() in subfunctions, that you will call from run().
    # The important thing is that GUI needs to call only run() to update coordinates! 

    # calculate classification values
    def calculate_Classification_Values(self):
        self.T1 = self.AB + self.CD - self.BC - self.DA
        self.T2 = self.BC + self.AB - self.CD - self.DA
        self.T3 = self.CD + self.BC - self.AB - self.DA
        self.L =  self.AB + self.BC + self.CD + self.DA
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
        self.calculate_C_Position

        # calculate P
        self.calculate_P_Position

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
            BC1_vector = self.C1 - self.B

            # calculate cross product to choose C between C1 and C2
            cross_product_1 = BD_vector[0] * BC1_vector[1] - BD_vector[1] * BC1_vector[0]

            # choose C according to cross product result
            if cross_product_1 > 0:
                C_positive, C_negative = C1, C2
            else:
                C_positive, C_negative = C2, C1

            # store results, ensure that cross product of C1 is always positive
            self.C1 = C_positive
            self.C2 = C_negative

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
        P1 = Q + offset_distance * normal_vector_toCD
        P2 = Q - offset_distance * normal_vector_toCD

        # Use cross product to choose the correct position for point P
        DQ_vector = Q - self.D  # Calculate vector DQ
        DP1_vector = P1 - self.D  # Calculate vector DP1
        cross_product_1 = DQ_vector[0] * DP1_vector[1] - DQ_vector[1] * DP1_vector[0]

        # Choose P point based on the cross product result
        if cross_product_1 > 0:
            P_positive, P_negative = P1, P2
        else:
            P_positive, P_negative = P2, P1

        #ensure that P1 is always with positive cross product
        self.P1 = P_positive
        self.P2 = P_negative

        return



    def update_trajectory(self):
        """Update the points' trajectory and add it to the DataFrame."""
        new_data = {
            'A_x': self.A[0], 'A_y': self.A[1],
            'B_x': self.B[0], 'B_y': self.B[1],
            'C1_x': self.C1[0], 'C1_y': self.C1[1],
            'C2_x': self.C2[0], 'C2_y': self.C2[1],
            'D_x': self.D[0], 'D_y': self.D[1],
            'P1_x': self.P1[0], 'P1_y': self.P1[1],
            'P2_x': self.P2[0], 'P2_y': self.P2[1]
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