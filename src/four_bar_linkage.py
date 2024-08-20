class FourBarLinkage:
    # all parameters you need to calculate coordinates, default initializing
    
    # GIVEN
    # Parameters should be
    # bars lengths
    a = 0. # DA
    b = 0. # BC
    g = 0. # AB
    f = 0. # CD
    # input angle in degrees
    alpha = 0.
    # angle in degrees between ground bar and horizont
    theta = 0.
    # coupler positions
    coupler_position = 0. # distance between coupler P and D along DC
    coupler_offset = 0. # distance between coupler P and DC
    # all coordinates of conection points A,B,C,D,P
    A = (0.,0.) # coordinates of A are always (0,0)
    
    # TO CALCULATE
    # coordinates of B, C, D and P are to be calculated
    B = (0.,0.)
    C = (0.,0.)
    D = (0.,0.)
    P = (0.,0.)
    # you can classify motions using following values
    T1 = 0. # g+h-a-b
    T2 = 0. # b+g-a-h
    T3 = 0. # b+h-a-g
    # consult https://en.wikipedia.org/wiki/Four-bar_linkage
    
    
    # this is constructor that will be used from GUI to initialize all needed parameters,
    # lengths, angles, coordinated of fixed points and so one
    def __init__(self, a, b, g, f, alpha, theta, coupler_position, coupler_offset): 
        # initialize all parameters
        self.a = a
        self.b = b
        self.g = g
        self.f = f
        self.theta
        self.coupler_position = coupler_position
        self.coupler_offset = coupler_offset
        # initialize coordinates of connection points
        self.run()
    
    # implement here geometry to calculate coordinates of all points from parameters (lengths, angles, ...)
    # this function will be called from GUI after updating some parameters to get coordinates for GUI animation
    def run(self):
        # calculate classification values
        self.T1 = self.g + self.h - self.a - self.b
        self.T2 = self.b + self.g - self.a - self.h
        self.T3 = self.b + self.h - self.a - self.g
        # calculate all coordinates B, C, D, P
        # ...
        
    # add some functions, if you need it to implement run function. Keep it simple, 
    # split run() in subfunctions, that you will call from run().
    # The important thing is that GUI needs to call only run() to update coordinates! 