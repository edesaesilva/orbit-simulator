import PySimpleGUI as sg
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

#set up the path of the gif writer
mpl.rcParams['animation.convert_path'] = 'C:\Program Files\ImageMagick-7.0.9-Q16\magick.exe'

import matplotlib.animation as animation
from AstroLibrary.System import System

#the program's system
system = System()



global main_window, vis
#the image on the screen i will be updating with animations
vis = sg.Image('animation.gif')
#layout of the main window
main_layout = [ [vis],
                [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                [sg.Button('Add Star', key= 'star'), sg.Button('Add Planet', key='planet'), sg.Button('Add Rocks', key='rocks')],
                [sg.Button('Read JSON', key= 'read'), sg.Button('Write JSON', key= 'load'), sg.Button('Write CSV', key= 'csv')]]

#show a new window for inputting parameters for a new star
def show_star_window():

    star_layout = [[sg.Text('Star Mass (Solar Masses)'), sg.InputText(key='mass')],
                   [sg.Text('Star Radius (Solar Radii)'), sg.InputText(key='radius')],
                   [sg.Text('Initial X (kilometers)'), sg.InputText(key='x')],
                   [sg.Text('Initial Y (kilometers)'), sg.InputText(key='y')],
                   [sg.OK()]]
    star_window = sg.Window('New Star').Layout(star_layout)

    #track if the user gave us good numbers
    valid_input = False
    while not valid_input:
        event, values = star_window.Read()
        if event in (None, 'Exit'):
            break
        try:
            mass = float(values['mass'])
        except:
            sg.Popup('invalid mass was given!')
            continue
        try:
            radius = float(values['radius'])
        except:
            sg.Popup('invalid radius was given!')
            continue
        try:
            x = float(values['x'])
            y = float(values['y'])
            valid_input = True
        except:
            sg.Popup('invalid coordinates were given!')
            continue
    if valid_input:
        #radius and mass are in solar units so i'll convert them to km and kg
        system.add_star(radius*7e5, mass*2e30, x, y)
    star_window.close()

#show a new window for getting planet parameters
def show_planet_window():

    planet_layout = [[sg.Text('Planet Mass (Earth Masses)'), sg.InputText(key='mass')],
                     [sg.Text('Planet Radius (Earth Radii)'), sg.InputText(key='radius')],
                     [sg.Text('Initial X (kilometers)'), sg.InputText(key='x')],
                     [sg.Text('Initial Y (kilometers)'), sg.InputText(key='y')],
                     [sg.OK()]]
    planet_window = sg.Window('New Planet').Layout(planet_layout)

    #track if the user gave good input
    valid_input = False
    while not valid_input:
        event, values = planet_window.Read()
        if event in (None, 'Exit'):
            break
        try:
            mass = float(values['mass'])
        except:
            sg.Popup('invalid mass was given!')
            continue
        try:
            radius = float(values['radius'])
        except:
            sg.Popup('invalid radius was given!')
            continue
        try:
            x = float(values['x'])
            y = float(values['y'])
            valid_input = True
        except:
            sg.Popup('invalid coordinates were given!')
            continue
    if valid_input:
        #mass and radius were given in earth units so i'll convert it to km and kg
        system.add_planet(radius*6e3, mass*6e24, x, y)
    planet_window.close()

#show a new window to get parameters for new rocks from the user
def show_rock_window():

    rock_layout = [[sg.Text('Number of Rocks'), sg.InputText(key='n')],
                   [sg.Text('Initial X (kilometers)'), sg.InputText(key='x')],
                   [sg.Text('Initial Y (kilometers)'), sg.InputText(key='y')],
                   [sg.OK()]]
    rock_window = sg.Window('New Rocks').Layout((rock_layout))

    #track if we got valid input
    valid_input = False
    while not valid_input:
        event, values = rock_window.Read()
        if event in (None, 'Exit'):
            break
        try:
            n = int(values['n'])
        except:
            sg.Popup('invalid number of rocks!')
            continue
        try:
            x = float(values['x'])
            y = float(values['y'])
            valid_input = True
        except:
            sg.Popup('invalid coordinates were given!')
            continue
    if valid_input:
        for i in range(n):
            #seperate the rocks by a little bit so they have a chance to follow different orbits
            system.add_rocks(x+i*1000, y-i*1000)
    rock_window.close()

#read a system from the specified json file
def read_json():
    read_layout = [[sg.Text('File name (.json)'), sg.InputText(key='file')],
                   [sg.OK()]]
    read_window = sg.Window('Read JSON').Layout((read_layout))
    # track if we got valid input
    valid_input = False
    while not valid_input:
        event, values = read_window.Read()
        if event in (None, 'Exit'):
            break
        #check file type is correct
        if not values['file'][-5:] == '.json':
            sg.Popup('Invalid file name')
            continue
        try:
            json_file = open(values['file'], 'r')
            data = json.load(json_file)
            json_file.close()
            system.from_json(data)
            valid_input = True
        except:
            sg.Popup('There was a problem')
    read_window.close()

def load_json():
    load_layout = [[sg.Text('File name (.json)'), sg.InputText(key='file')],
                   [sg.OK()]]
    load_window = sg.Window('Load JSON').Layout((load_layout))
    # track if we got valid input
    valid_input = False
    while not valid_input:
        event, values = load_window.read()
        if event in (None, 'Exit'):
            break
        # check file type is correct
        if not values['file'][-5:] == '.json':
            sg.Popup('Invalid file name')
            continue
        try:
            system.to_json(values['file'])
            valid_input = True
        except:
            sg.Popup('Invalid file name')
    load_window.close()

def write_csv():
    write_layout = [[sg.Text('File name (.csv)'), sg.InputText(key='file')],
                   [sg.OK()]]
    write_window = sg.Window('write CSV').Layout((write_layout))
    # track if we got valid input
    valid_input = False
    while not valid_input:
        event, values = write_window.read()
        if event in (None, 'Exit'):
            break
        # check file type is correct
        if not values['file'][-4:] == '.csv':
            sg.Popup('Invalid file name')
            continue
        try:
            system.to_csv(values['file'])
            valid_input = True
        except:
            sg.Popup('Invalid file name')
    write_window.close()

#init function for mpl animation
def init_animation():
    #get the positions of every type of object and place them on the plot
    system_stars = system.get_stars()
    star_data = items_to_positions(system_stars)
    stars.set_data(star_data[0], star_data[1])

    system_planets = system.get_planets()
    planet_data = items_to_positions(system_planets)
    planets.set_data(planet_data[0], planet_data[1])

    system_rocks = system.get_rocks()
    rock_data = items_to_positions(system_rocks)
    rocks.set_data(rock_data[0], rock_data[1])

    return stars, planets, rocks

#animation function for mpl animation
#calculates the ith frame of the gif
def animate(i):
    #simulate one time step
    system.simulate_time()

    #get the positions of every type of object and place them on the plot
    system_stars = system.get_stars()
    star_data = items_to_positions(system_stars)
    stars.set_data(star_data[0], star_data[1])

    system_planets = system.get_planets()
    planet_data = items_to_positions(system_planets)
    planets.set_data(planet_data[0], planet_data[1])

    system_rocks = system.get_rocks()
    rock_data = items_to_positions(system_rocks)
    rocks.set_data(rock_data[0], rock_data[1])

    return stars, planets, rocks

#a helper function that takes a list of objects and returns two lists of x and y values
def items_to_positions(items):
    x,y = [],[]
    for item in items:
        position = item.get_position()
        x.append(position[0])
        y.append(position[1])
    return x,y

#generate animation.gif
def generate_gif(time):
    #meaningful value i'm using when i need a still image
    if time == 0:
        anim = animation.FuncAnimation(fig, animate, frames=1, blit=True, init_func=init_animation)
        anim.save('animation.gif', writer='imagemagick', extra_args="convert", fps=60)
        return
    #set the time step of the system for 300 frames
    system.set_dt(time)
    #animate the gif
    anim = animation.FuncAnimation(fig, animate, frames=300, blit=True, init_func=init_animation)
    #save to animation.gif
    print("saving animation")
    anim.save('animation.gif', writer='imagemagick', extra_args="convert", fps=60)
    print("refreshing main window")


main_window = sg.Window('Orbit Simulator').Layout(main_layout)

#initializing the figure used in the animation
fig = plt.figure(facecolor='black')
axis = fig.add_subplot(111,autoscale_on=False, xlim=(-1e9,1e9), ylim= (-1e9,1e9), facecolor= 'black')
stars, = axis.plot([], [], 'oy')
planets, = axis.plot([], [], '.b')
rocks, = axis.plot([], [], ',w')
#generate the still image of the initial state of the system
generate_gif(0)

#event loop
while True:
    #timeout on 50 ms to animate the gif
    event, values = main_window.Read(timeout=50)

    if event in (None, 'Exit'):
        break

    if event == 'star':
        #the user has asked to add a new star
        show_star_window()
        #display the new initial state
        generate_gif(0)

        #regenerate the main window with the new picture
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'), sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key= 'read'), sg.Button('Write JSON', key= 'load'), sg.Button('Write CSV', key= 'csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)

    if event == 'planet':
        #the user has asked to add a new planet
        show_planet_window()
        #update the image
        generate_gif(0)
        #refresh the main window with the new image
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                        sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                        sg.Button('Write CSV', key='csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)

    if event == 'rocks':
        #the user has asked to add rocks
        show_rock_window()
        #update image
        generate_gif(0)
        #refresh main window
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                        sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                        sg.Button('Write CSV', key='csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)

    if event == 'sim':
        #user has asked to run the simulation
        try:
            #get specified time
            t = int(values['time'])

            generate_gif(t)
            #refresh page with new image
            vis = sg.Image('animation.gif')
            main_layout = [[vis],
                           [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                           [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                            sg.Button('Add Rocks', key='rocks')],
                           [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                            sg.Button('Write CSV', key='csv')]]
            main_window = sg.Window('Orbit Simulator').Layout(main_layout)
        except:
            sg.Popup(f"{values['time']} is an invalid time!")

    if event == 'read':
        #show the read json window
        read_json()
        # update image
        generate_gif(0)
        # refresh main window
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                        sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                        sg.Button('Write CSV', key='csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)
        
    if event == 'load':
        #show the load json window
        load_json()
        # update image
        generate_gif(0)
        # refresh main window
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                        sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                        sg.Button('Write CSV', key='csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)

    if event == 'csv':
        #show the csv window
        write_csv()
        # update image
        generate_gif(0)
        # refresh main window
        vis = sg.Image('animation.gif')

        main_layout = [[vis],
                       [sg.Text('Time (seconds)'), sg.InputText(key='time'), sg.Button('Go', key='sim')],
                       [sg.Button('Add Star', key='star'), sg.Button('Add Planet', key='planet'),
                        sg.Button('Add Rocks', key='rocks')],
                       [sg.Button('Read JSON', key='read'), sg.Button('Write JSON', key='load'),
                        sg.Button('Write CSV', key='csv')]]
        main_window = sg.Window('Orbit Simulator').Layout(main_layout)

    #for animating the gif in the window
    if event == "__TIMEOUT__":
        vis.update_animation('animation.gif', time_between_frames=50)


        #TODO: add import/export buttons or dialogues, test export filename for json extendo, open import file on your own and pull all the data