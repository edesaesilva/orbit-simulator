import numpy as np
import json
import csv

from AstroLibrary.Planet import Planet
from AstroLibrary.Rock import Rock
from AstroLibrary.Star import Star


class System:
    '''
    Class holding info and methods for the whole system of bodies
    stars: a list of Star objects in the system
    planets: a list of Planet objects in the system
    rocks: a list of Rock objects in the system
    cog_x: x coordinate of the center of gravity of the system
    cog_y: y coordinate of the center of gravity of the system
    effective_mass: the "mass" at the center of gravity
    dt: timestep to use for animation
    '''

    def __init__(self):

        self.stars = []
        self.planets = []
        self.rocks = []
        self.cog_x = 0
        self.cog_y = 0
        self.effective_mass = 0
        self.dt = 10000

    def get_stars(self):
        return self.stars

    def get_planets(self):
        return self.planets

    def get_rocks(self):
        return self.rocks

    def get_center_of_grav(self):
        return self.cog_x, self.cog_y

    def get_mass(self):
        return self.effective_mass

    def valid_position(self, x, y):
        #checking if we are trying to place an object on top of another object
        for star in self.stars:
            star_x,star_y = star.get_position()
            star_r = star.get_radius()
            #if the x,y is inside the star
            if np.sqrt((x - star_x)**2 + (y-star_y)**2) < star_r:
                return False
        #same code but for planets
        for planet in self.planets:
            planet_x, planet_y = planet.get_position()
            planet_r = planet.get_radius()
            if np.sqrt((x - planet_x) ** 2 + (y - planet_y) ** 2) < planet_r:
                return False
        return True

    def calc_center_of_gravity(self):
        #finding the center of gravity between all massive objects of the system
        sum_mass = 0
        sum_y = 0
        sum_x = 0

        for star in self.stars:
            star_mass = star.get_mass()
            star_x, star_y = star.get_position()
            sum_mass += star_mass
            sum_x += star_mass * star_x
            sum_y += star_mass*star_y

        for planet in self.planets:
            planet_mass = planet.get_mass()
            planet_x, planet_y = planet.get_position()
            sum_mass += planet_mass
            sum_x += planet_mass*planet_x
            sum_y += planet_mass*planet_y
        #update system variables
        #d = sum(mass_i * d_i)/sum(mass_i)
        if sum_mass == 0:
            return
        self.cog_x = sum_x/sum_mass
        self.cog_y = sum_y/sum_mass
        self.effective_mass = sum_mass

    def add_star(self, radius, mass, initial_x, initial_y):
        #make sure we're not putting a star inside something else
        if not self.valid_position(initial_x, initial_y):
            return

        #binary systems only
        if len(self.stars) >= 2:
            return

        new_star = Star(radius, mass, initial_x, initial_y)
        self.stars.append(new_star)
        self.calc_center_of_gravity()

    def add_planet(self, radius, mass, initial_x, initial_y):
        #make sure we're not placing a planet inside anything else
        if not self.valid_position(initial_x, initial_y):
            return

        new_planet = Planet(radius, mass, initial_x, initial_y)
        self.planets.append(new_planet)
        self.calc_center_of_gravity()

    def add_rocks(self, initial_x, initial_y):
        #rocks are very naive and dont care about anything
        new_rock = Rock(initial_x, initial_y)
        self.rocks.append(new_rock)

    def simulate_time(self):
        #simulate one time step
        self.calc_center_of_gravity()
        for star in self.stars:
            star.move(self.cog_x, self.cog_y, self.effective_mass, self.dt)
        for planet in self.planets:
            planet.move(self.cog_x, self.cog_y, self.effective_mass, self.dt)
        for rock in self.rocks:
            rock.move(self.cog_x, self.cog_y, self.effective_mass, self.dt)
        self.calc_center_of_gravity()

    def set_dt(self,time):
        self.dt = time//300

    #send a json representation of the system to a file called file_name
    def to_json(self, file_name):
        file = open(file_name, 'w')
        
        star_data = []
        for star in self.get_stars():
            star_data.append(star.serialize())
        planet_data = []
        for planet in self.get_planets():
            planet_data.append(planet.serialize())
        rock_data = []
        for rock in self.get_rocks():
            rock_data.append(rock.serialize())

        all_data = {'stars': star_data, 'planets': planet_data, 'rocks': rock_data}

        json.dump(all_data, file)
        file.close()


    #read a system configuration from a json file
    def from_json(self, data):

        self.reset_space()
        for star in data['stars']:
            self.add_star(star['radius'], star['mass'], star['x'], star['y'])
        for planet in data['planets']:
            self.add_planet(planet['radius'], planet['mass'], planet['x'], planet['y'])
        for rock in data['rocks']:
            self.add_rocks(rock['x'], rock['y'])

    def to_csv(self, file_name):
        file = open(file_name, 'w')

        writer = csv.writer(file, delimiter=',')

        writer.writerow(['Name', 'Mass (kg)', 'Radius(km)', 'Position (km,km)'])

        stars = self.get_stars()
        for i in range(len(stars)):
            writer.writerow([f'Star{i}', stars[i].get_mass(),stars[i].get_radius(),stars[i].get_position()])
        planets = self.get_planets()
        for i in range(len(planets)):
            writer.writerow([f'Planet{i}', planets[i].get_mass(), planets[i].get_radius(), planets[i].get_position()])
        rocks = self.get_rocks()
        for i in range(len(rocks)):
            writer.writerow([f'Rock{i}', 0, 0, rocks[i].get_position()])

        file.close()

    def reset_space(self):
        #destroy everything
        self.stars = []
        self.planets = []
        self.rocks = []