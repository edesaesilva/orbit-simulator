import numpy as np

G = 6.67e-20

class Rock:
    '''
    Class holding info and methods for a massless rock in the system
    This object has no radius as they will be visually all the same size
    x: x coordinate on the simulation plane
    y: y coordinate on the simulation plane
    T: period of orbit of the planet
    circ: circumference of the planet's orbit
    axis: semimajor axis of the planet's orbit
    '''


    #System object MUST check validity of x and y values for all rocks
    def __init__(self,  initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y

    #return this object's coordinates in the form (x,y)
    def get_position(self):
        return self.x, self.y

    #set this object's coordinates, MUST be checked by the controlling System; cant do checking here
    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    #return the object in a json writable form
    def serialize(self):
        data = {}
        data['x'] = self.x
        data['y'] = self.y
        return data

    def find_period(self, system_mass):
        # kepler's third law
        self.T = np.sqrt(4 * np.pi ** 2 / G / system_mass * self.axis ** 3)

    #cog_x: x coordinate of the center of gravity of the system
    #cog_y: y coordinate of the center of gravity of the system
    #effective_mass: approximation of the "mass" at the center of gravity of the system
    #dt: the time period in seconds over which to simulate
    #returns a numpy array of position data
    def move(self, cog_x, cog_y, effective_mass, dt):
        # simulate 100 seconds per time step for now, may be increased for visuals
        nt = 2
        t = np.linspace(0,dt,nt)

        #track x,y over nt steps
        movement = np.zeros((nt,2))
        movement[0][0] = self.x
        movement[0][1] = self.y

        #semimajor axis calculation
        self.axis = np.sqrt((self.x-cog_x)**2 + (self.y-cog_y)**2)
        #finding period for future calculations
        self.find_period(effective_mass)
        #circumference calculation
        self.circ = 2 * np.pi * self.axis

        for time in range(1,nt):
            # special case for objects close to the cog, we wont bother to move them
            if self.T < 100:
                movement[time][0] = movement[time - 1][0]
                movement[time][1] = movement[time - 1][1]
                continue
            # find fraction of area covered in this time period (kepler's second law)
            percent_change_t = (t[time] - t[time - 1]) / self.T
            # this helps us find the fraction of the circumference covered
            this_step_distance = percent_change_t * self.circ

            # special cases for moving perpindicular to either axis
            if abs(movement[time - 1][1] - cog_y) < 1:
                # moving exactly vertically
                movement[time][0] = movement[time - 1][0]
                if movement[time][0] > cog_x:
                    # right of the center of gravity; we should move upwards
                    movement[time][1] = movement[time - 1][1] + this_step_distance
                else:
                    # left side, move negative y way
                    movement[time][1] = movement[time - 1][1] - this_step_distance
                continue

            if abs(movement[time - 1][0] - cog_x) < 1:
                # moving exactly horizontally
                movement[time][1] = movement[time - 1][1]
                if movement[time][1] > cog_y:
                    # above of the center of gravity; we should move lefts
                    movement[time][0] = movement[time - 1][0] - this_step_distance
                else:
                    # lower side, move right
                    movement[time][0] = movement[time - 1][0] + this_step_distance
                continue

            #slope of the planet to the center of gravity
            cog_rock_slope = (movement[time-1][1]-cog_y)/(movement[time-1][0]-cog_x)
            #approximate movement by a perpendicular line
            orbit_slope = -1 * (1/cog_rock_slope)

            #conditions for counterclockwise movement
            if movement[time-1][1] > 0:
                new_x = movement[time-1][0] - this_step_distance*np.sqrt(1/(1+orbit_slope**2))
            else:
                new_x = movement[time-1][0] + this_step_distance*np.sqrt(1/(1+orbit_slope**2))
            new_y = orbit_slope*(new_x-movement[time-1][0]) + movement[time-1][1]

            movement[time][0] = new_x
            movement[time][1] = new_y
        self.x = movement[-1][0]
        self.y = movement[-1][1]
        return movement