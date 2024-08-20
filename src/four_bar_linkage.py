class FourBarLinkage:
    # all parameters you need to calculate coordinates, default initializing
    # for example 
    # AB = 0
    # ...
    # alpha = ...
    # ...
    # all coordinates of conection points A,B,C,D,P
    # A = (0.,0.)
    # ...
    # P = (0.,0.)
    
    # this is constructor that will be used from GUI to initialize all needed parameters,
    # lengths, angles, coordinated of fixed points and so one
    def __init__(self): #(self, AB, ..., alpha, ...):
        # initialize all parameters
        # for example
        # self.AB = AB
        # ...
        # self.alpha = alpha
        # initialize coordinates of connection points
        self.run()
    
    # implement here geometry to calculate coordinates of all points from parameters (lengths, angles, ...)
    # this function will be called from GUI after updating some parameters to get coordinates for GUI animation
    def run(self):
        # calculate and set all parameters
        # self.A = ...
        # ...
        pass # delete later   
        
    # add some functions, if you need it to implement run function. Keep it simple, 
    # split run() in subfunctions, that you will call from run().
    # The important thing is that GUI needs to call only run() to update coordinates! 