# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

# Objects
from Objects.house import House
from Objects.battery import Battery
from Objects.route import Route
from Objects.distance import distance


# Libraries
import csv
import random
import copy
import matplotlib.pyplot as plt
import numpy as np

GRID_LENGTH = 50
GRID_WIDTH = 50

class Grid(object):
    """
    Representation of a grid in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    counter = 0


    def __init__(self, wijk_N):
        """
        Initialize a grid based on given csv files
        """
        # id
        self.id = Grid.id
        Grid.id += 1
        self.name = wijk_N
        # load houses and batteries
        self.houses = self.load_houses(f"Huizen_Batterijen/{wijk_N}_huizen.csv")
        self.unconnected_houses = copy.deepcopy(self.houses)
        self.batteries = self.load_batteries(f"Huizen_Batterijen/{wijk_N}_batterijen.csv")
        random.shuffle(self.batteries)
        # size of grid
        self.size = (GRID_WIDTH, GRID_LENGTH)


    def __str__(self):
        """
        Print grid description
        """
        return f"Wijk: {self.name[-1]} GridID: {self.id} Grid size: {self.size}"


    def load_houses(self, filename):
        """
        Load houses from csv file
        """
        # Open file
        with open(filename, "r") as csvfile:

            # loop over rows of csv file, make house based on content and add house to house list of grid
            houses = [House(row[0], row[1], row[2]) for row in csv.reader(csvfile) if row[0].isdigit()]
        return houses


    def load_batteries(self, filename):
        """
        Load batteries from .csv
        """
        # open file
        with open(filename, "r") as csvfile:
            # loop over rows of csv file make battery based on data and add to battery list
            batteries = [Battery(row[0], row[1], "Normal", row[2], int(row[3])) for row in csv.reader(csvfile) if row[0].isdigit()]

        return batteries


    def connect(self, house_id,  battery_id):
        """
        Connect a house to a battery and change information in system accordingly
        """
        # get house
        H = [house for house in self.unconnected_houses if house.id == house_id]

        # error check
        if not H:
            return False
        if len(H) > 1:
            print("Mutiple houses found, please reload grid")
            return False

        # unlist
        H = H[0]

        # get battery
        B = [battery for battery in self.batteries if battery.id == battery_id]

        # error check
        if not B:
            return False
        if len(B) > 1:
            return False

        # unlist
        B = B[0]

        # if house max_output exceeds battery capacity return and print error message
        if B.current_capacity < H.max_output:
            # print(f"Battery capacity ({round(B.current_capacity, 2)}) is not sufficient")
            return False

        # remove house from unconnected list
        self.unconnected_houses.remove(H)

        # get battery index in battery list of grid
        B_index = self.batteries.index(B)

        # Make a route and append it to the route list in the corresponding battery
        route = Route(H, B.id, B.location)
        self.batteries[B_index].routes.append(route)

        # recalculate battery current capacity
        self.batteries[B_index].current_capacity -= H.max_output

        return True


    def disconnect(self, house_id):
        """
        Disconnects house based on id
        """
        # loop over routes in each battery untill we find the correct house
        for battery in self.batteries:
            for route in battery.routes:
                if route.house.id == house_id:
                    # find battery index
                    battery_idx = self.batteries.index(battery)
                    # update battery capacity
                    self.batteries[battery_idx].current_capacity += route.house.max_output
                    # place house back to unconnected_houses
                    self.unconnected_houses.append(route.house)
                    # remove route
                    self.batteries[battery_idx].routes.remove(route)
                    return True
        # if house id not found print error message
        return False


    def disconnect_all(self):
        """
        Disconnects all houses from batteries
        """
        for battery in self.batteries:
            while battery.routes != []:
                self.disconnect(battery.routes[0].house.id)


    def swap(self, h1, h2, h3 = False, h4 = False):
        """
        Swaps 2 or 4 houses
        """
        swap = False
        if h3 == False or h4 == False:
            # disconnect houses
            self.disconnect(h1.house.id)
            self.disconnect(h2.house.id)
            # reconnected houses swapped
            self.connect(h1.house.id, h2.battery_id)
            self.connect(h2.house.id, h1.battery_id)
            swap = True
        else:
            # disconnect houses
            self.disconnect(h1.house.id)
            self.disconnect(h2.house.id)
            self.disconnect(h3.house.id)
            self.disconnect(h4.house.id)
            # reconnected swap
            self.connect(h1.house.id, h3.battery_id)
            self.connect(h2.house.id, h3.battery_id)
            self.connect(h3.house.id, h1.battery_id)
            self.connect(h4.house.id, h1.battery_id)
            swap = True
        return swap


    def calculate_total_cost(self):
        """
        Calculates the total cost of the current grid
        """
        total_cost_routes = sum([battery.calculate_routes_cost() for battery in self.batteries])
        total_cost_batteries = sum([battery.cost for battery in self.batteries])
        total_cost = total_cost_routes + total_cost_batteries
        return total_cost


    def lower_bound(self):
        """
        Calculates the lower_bound based on the  manhattan distance for the shortest path
        for each house.
        Returns the total grid cost of the lower_bound
        """
        all_shortest = []
        # loop over houses for each house loop over batteries
        # find the shortest distance to a battery and append to output list
        for house in self.houses:
            current_house_shortest = float('inf')
            for battery in self.batteries:
                dist = distance(house.location, battery.location)
                if dist < current_house_shortest:
                    current_house_shortest = dist
            all_shortest.append(current_house_shortest)

        # calculate lower bound costs
        lower_bound = 0
        for battery in self.batteries:
            lower_bound += battery.cost
        lower_bound += sum(all_shortest) * 9

        return lower_bound


    def upper_bound(self):
        """
        Calculates the upper_bound based on the manhattan distance for the longest path
        for each house.
        Returns the total grid cost of the upper_bound
        """
        all_longest = []
        # loop over houses for each house loop over batteries
        # find the longest distance to a battery and append to output list
        for house in self.houses:
            current_house_longest = float('-inf')
            for battery in self.batteries:
                dist = distance(house.location, battery.location)
                if dist > current_house_longest:
                    current_house_longest = dist
            all_longest.append(current_house_longest)

        # calculate lower bound costs
        upper_bound = 0
        for battery in self.batteries:
            upper_bound += battery.cost
        upper_bound += sum(all_longest) * 9

        return upper_bound


    def draw_grid(self, info = ""):
        """
        Draw routes using the grid_route property of the routes
        """
        plt.figure()

        # draw grid
        size = [x for x in range(51)]
        for x in range(51):
            current = [x for i in range(51)]
            plt.plot(size, current, 'k', linewidth=0.2)
            plt.plot(current, size, 'k', linewidth=0.2)

        # set potential colors for batteries
        colors = ['b', 'g', 'r', 'm', 'c', 'y']

        # plot all houses and batteries, house has color of battery it is connected to
        # for each route in each battery plot the grid_routes in the same color as the battery
        for idx, battery in enumerate(self.batteries):
            color = colors[idx % 6]
            # plot battery
            plt.plot(battery.location[0], battery.location[1], color + '8', markersize = 12)

            for route in battery.routes:

                # get x and y
                x = [loc[0] for loc in route.grid_route]
                y = [loc[1] for loc in route.grid_route]

                # plot route
                plt.plot(x, y, color)

                # plot house
                plt.plot(route.house.location[0], route.house.location[1], color + '8', markersize = 5)

        # plot all unconnected houses in black
        for house in self.unconnected_houses:
            plt.plot(house.location[0], house.location[1], 'k8', markersize = 5)

        # get lowerbound
        lower_bound = self.lower_bound()

        # costs and wijk name in title
        cost = self.calculate_total_cost()
        plt.title(f"{self.name} costs: {cost} {info}, lower bound: {lower_bound}")

        plt.show()


    def range_connected(self, battery):
        """
        Returns absolute minimum and maximum of house that can be connected to input battery
        """
        # function that returns max output
        def max_output_func(house):
            return house.max_output
        # sort houses from smallest max output to largest
        self.unconnected_houses.sort(key=max_output_func)
        # get min amount of houses able to connect
        capacity_taken = 0
        max_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.current_capacity:
                capacity_taken += house.max_output
                max_connected_houses += 1
        # sort houses from largest to smallest max output
        self.unconnected_houses.sort(reverse=True, key=max_output_func)
        # get max amount of houses able to connect
        capacity_taken = 0
        min_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.current_capacity:
                capacity_taken += house.max_output
                min_connected_houses += 1

        range = (min_connected_houses, max_connected_houses)
        return range


    def move_batteries_random(self):
        """
        Moves each battery to a random new location
        """
        # for each battery
        for battery in self.batteries:

            location_taken = True

            # keep generating random locations untill location is not taken by a house or battery (including current battery)
            while location_taken == True:
                location = (random.randint(0,51), random.randint(0,51))

                for house in self.houses:
                    if house.location == location:
                        location_taken = True
                        continue
                    else:
                        location_taken = False

                for bat in self.batteries:
                    if bat.location ==  location:
                        location_taken = True
                        continue
                    else:
                        location_taken = False

            # move battery
            battery.move(location)
