#        __________              __________
#       /          \            /          \
#      /____{()}____\          /____{()}____\
#     |----|    |----|        |----|    |----|
#     |{()}|    |{()}|   VS   |{()}|    |{()}|
#     \ ~~ / $$ \ ~~ /        \ ~~ / $$ \ ~~ /
#      \  /  $$  \  /          \  /  $$  \  /
#       \/  $$$$  \/            \/  $$$$  \/
#       ||        ||            ||        ||
#  @MVM@ \________/              \________/ @MVM@
#       \ \//____/                \____\\/ /
#       / //                            \\ \
#       \//                              \\/
#Date:2021/12/29
#Data exploration exercise from geeksforgeek.com
#I expanded upon their initial lesson by adding the user input
#and adding the freqs, times, and mean speeds of nico and sanne
#Keyword args: "long-lat", "map", "freqs", "times", "mean-speed or "gui"
#plots and compares three bird gps data
#long/lat of birds paths and then overlayed
#on a cartographic map. mean daily speed,
#the speed frequency and elapsed times are also analyzed
#added a gui... for fun

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import tkinter as tk

#general tracker of each birds longitude and latitude
def long_lat_track():

    #read data and find the unique bird names
    data = pd.read_csv("bird_tracking.csv")
    bird_names = pd.unique(data.bird_name)

    #interate through bird_names
    for name in bird_names:
        #store the unique bird name in indices
        indices = data.bird_name == name
        #store the logitude and latitude of that bird
        x, y = data.longitude[indices], data.latitude[indices]
        #plot data
        plt.plot(x, y, ",", label = name)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend(loc = "lower right")
    plt.show()

#function that plots the birds latitude and longitude 
#on a map
def b_map():

    #read data and grab unique bird names
    data = pd.read_csv("bird_tracking.csv")
    indices = pd.unique(data.bird_name)

    # define a porjector to use for plotting from ccrs
    proj = ccrs.Mercator()

    plt.figure(figsize = (10,10))

    #defining the projection plot using Mercator
    ax = plt.axes(projection = proj)
    #define all of the additions to the map
    ax.set_extent((-25.0, 20.0, 52.0, 10.0))
    ax.add_feature(cfeat.LAND)
    ax.add_feature(cfeat.OCEAN)
    ax.add_feature(cfeat.COASTLINE)
    ax.add_feature(cfeat.BORDERS, linestyle = ":")

    #loop through the names grab name and plot the long and lat 
    #using Geodetic from ccrs
    for name in indices:
        ind = data["bird_name"] == name
        x, y = data.longitude[ind], data.latitude[ind]
        ax.plot(x, y, ".", markersize = 2.0, transform = ccrs.Geodetic(), label = name)

    plt.legend(loc = "upper left")
    plt.show()

#function to plot the frequency of observations of each bird
def freqs():

    data = pd.read_csv("bird_tracking.csv")

    #grabbing the unique birds
    e_indices = data.bird_name == "Eric"
    n_indices = data.bird_name == "Nico"
    s_indices = data.bird_name == "Sanne"

    #getting each of their speeds
    e_speed = data.speed_2d[e_indices]
    n_speed = data.speed_2d[n_indices]
    s_speed = data.speed_2d[s_indices]

    #tests if the value is nan then returns the boolean array
    e_ind = np.isnan(e_speed)
    n_ind = np.isnan(n_speed)
    s_ind = np.isnan(s_speed)

    #define the figure
    fig, ax = plt.subplots(1, 3, figsize = (12, 4), 
                           gridspec_kw = {"wspace" : 0.5})

    #plot the histograms ~e_ind plots the speed if the value is true
    ax[0].hist(e_speed[~e_ind], bins = np.linspace(0, 30, 20), color = 'r')
    ax[1].hist(n_speed[~n_ind], bins = np.linspace(0, 30, 20), color = 'g')
    ax[2].hist(s_speed[~s_ind], bins = np.linspace(0, 30, 20), color = 'b')
    
    ax[0].set(title = 'Eric')
    ax[1].set(title = 'Nico')
    ax[2].set(title = 'Sanne')

    fig.supxlabel('Speed 2d (m/s)')
    fig.supylabel('Frequency')
    plt.show()

def times():

    data = pd.read_csv("bird_tracking.csv")

    #array for holding time stamp variables
    stamps = []
    #print(data.head())
    #loop for stripping datetime 
    for i in range(len(data)):
        stamps.append(datetime.datetime.strptime(data.date_time.iloc[i][:-3],
        "%Y-%m-%d %H:%M:%S"))
    #print(stamps)

    #add a new column to the data fram and make it a series 
    #of the parsed time stamps
    data["timestamp"] = pd.Series(stamps, index = data.index)

    #getting all of the bird times, need to reset index for Nico and
    #Sanne because their indexes dont start at 0
    e_times = data.timestamp[data.bird_name == "Eric"]

    n_times = data.timestamp[data.bird_name == "Nico"]
    n_times = n_times.reset_index(drop = True)

    s_times = data.timestamp[data.bird_name == "Sanne"]
    s_times = s_times.reset_index(drop = True)
    #print(times)

    #getting the elapsed time
    e_elap_time = [time - e_times[0] for time in e_times]
    n_elap_time = [time - n_times[0] for time in n_times]
    s_elap_time = [time - s_times[0] for time in s_times]

    #define the figure same as all of the others
    fig, ax = plt.subplots(1, 3, figsize = (12, 4), 
                           gridspec_kw = {"wspace" : 0.5})

    ax[0].plot(np.array(e_elap_time) / datetime.timedelta(days = 1), color = 'r')
    ax[1].plot(np.array(n_elap_time) / datetime.timedelta(days = 1), color = 'g')
    ax[2].plot(np.array(s_elap_time) / datetime.timedelta(days = 1), color = 'b')

    ax[0].set(title = 'Eric')
    ax[1].set(title = 'Nico')
    ax[2].set(title = 'Sanne')

    fig.supxlabel('Observation')
    fig.supylabel('Elapsed Time (days)')

    plt.show()

#plots the daily mean speed of each bird
def speeds():

    data = pd.read_csv("bird_tracking.csv")

    stamps = []
    e_next = 1
    e_inds = []
    e_day_mean_speed = []
    n_next = 1
    n_inds = []
    n_day_mean_speed = []
    s_next = 1
    s_inds = []
    s_day_mean_speed = []

    #parse time and store it in stamps
    for i in range(len(data)):
        stamps.append(datetime.datetime.strptime(data.date_time.iloc[i][:-3],
        "%Y-%m-%d %H:%M:%S"))

    #create a new column in data called timestamp which is the parsed times
    data["timestamp"] = pd.Series(stamps, index = data.index)

    #grabbing specific bird data
    e_new_data = data[data.bird_name == "Eric"]
    #grabbing just the time stamp data
    e_times = e_new_data.timestamp

    #same as previously but need to reset index because 
    #index doesnt start at 1
    n_new_data = data[data.bird_name == "Nico"]
    n_new_data = n_new_data.reset_index(drop = True)
    n_times = n_new_data.timestamp

    #same as for nico
    s_new_data = data[data.bird_name == "Sanne"]
    s_new_data = s_new_data.reset_index(drop = True)
    s_times = s_new_data.timestamp

    #print(times.head())

    #same for every bird, grab the elapsed time and the elapsed days
    e_elap_time = [time - e_times[0] for time in e_times]
    e_elap_days = np.array(e_elap_time) / datetime.timedelta(days = 1)

    #loop through elapsed days, we enumerate so that we can track j
    #which is the iteration we are on
    for (i, j) in enumerate(e_elap_days):
        #when j is less than e_next which we set to 1 earlier
        if j < e_next:
            #we append i to e_inds where i is the elapsed days
            e_inds.append(i)
        else:
            #then we append to the day_mean_speed the mean of the speed
            #2d data in relation to e_inds which was appeneded earlier
            e_day_mean_speed.append(np.mean(e_new_data.speed_2d[e_inds]))
            #add one to e_next
            e_next += 1
            #remove everything from e_inds
            e_inds = []

    n_elap_time = [time - n_times[0] for time in n_times]
    n_elap_days = np.array(n_elap_time) / datetime.timedelta(days = 1)

    for (i, j) in enumerate(n_elap_days):
        if j < n_next:
            n_inds.append(i)
        else:
            n_day_mean_speed.append(np.mean(n_new_data.speed_2d[n_inds]))
            n_next += 1
            n_inds = []

    s_elap_time = [time - s_times[0] for time in s_times]
    s_elap_days = np.array(s_elap_time) / datetime.timedelta(days = 1)

    for (i, j) in enumerate(s_elap_days):
        if j < s_next:
            s_inds.append(i)
        else:
            s_day_mean_speed.append(np.mean(s_new_data.speed_2d[s_inds]))
            s_next += 1
            s_inds = []

    fig, ax = plt.subplots(1, 3, figsize = (15, 4), 
                           gridspec_kw = {"wspace" : 0.5})

    ax[0].plot(e_day_mean_speed, "rs-")
    ax[1].plot(n_day_mean_speed, "gs-")
    ax[2].plot(s_day_mean_speed, "bs-")

    ax[0].set(title = 'Eric')
    ax[1].set(title = 'Nico')
    ax[2].set(title = 'Sanne')

    fig.supxlabel('Day')
    fig.supylabel('Mean Speed (m/s)')
    
    plt.show()

#gui... for fun
def tk_gui():

    #defines the window
    wind = tk.Tk()
    #sets the frame and the master to wind
    fr = tk.Frame(master = wind)

    #define all buttons and the command invoked
    btn_1 = tk.Button(master = fr, text = "Longitude/Latitude Plot",
                      command = long_lat_track)
    btn_2 = tk.Button(master = fr, text = "Flight Map", command = b_map)
    btn_3 = tk.Button(master = fr, text = "Speed Frequencies", command = freqs)
    btn_4 = tk.Button(master = fr, text = "Elapsed Time", command = times)
    btn_5 = tk.Button(master = fr, text = "Mean Speed", command = speeds)

    #defines the grid, where the buttons are and their spacing
    fr.grid(row = 0, column = 0, pady = 10)
    btn_1.grid(row = 1, column = 0, pady = 10)
    btn_2.grid(row = 2, column = 0, pady = 10)
    btn_3.grid(row = 3, column = 0, pady = 10)
    btn_4.grid(row = 4, column = 0, pady = 10)
    btn_5.grid(row = 5, column = 0, pady = 10)

    #starts the gui!
    wind.mainloop()

#main... obviously
def main():

    #takes the args and stores them in a list
    #not including the script itself
    args = sys.argv[1:]

    #if no args, then print and exit
    if len(args) < 1:
        print("Incorrect usage: Input Keyword args... 'long-lat',\
              'map', 'freqs', 'times', 'mean-speed', or 'gui'")
        sys.exit(1)

    #loop through the args and check then call the 
    #specific function b
    for arg in args:
        if "long-lat" in arg:
            long_lat_track()

        elif "map" in arg:
            b_map()

        elif "freqs" in arg:
            freqs()

        elif "times" in arg:
            times()

        elif "mean-speed" in arg:
            speeds()

        elif "gui" in arg:
            tk_gui()

if __name__ in "__main__":
    main()