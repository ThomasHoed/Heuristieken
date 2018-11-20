import csv
from house import House
from battery import Battery
from route import Route
from distance import distance
from operator import attrgetter
import copy

class Grid(object):
    """
    Representation of a grid in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    counter = 0
    def __init__(self, wijk_N):
        """
        Initialize a grid"""
        # id
        self.id = Grid.id
        Grid.id += 1
        # load houses and batteries
        self.houses = self.load_houses(f"Huizen_Batterijen/{wijk_N}_huizen.csv")
        self.unconnected_houses = self.houses
        self.batteries = self.load_batteries(f"Huizen_Batterijen/{wijk_N}_batterijen.csv")
        # size of grid
        self.size = (50, 50)

    def __str__(self):
        """
        Print description
        """
        return f" GridID: {self.id} Grid size: {self.size}"

    def load_houses(self, filename):
        """
        Load houses from .csv
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
            batteries = [Battery(row[0], row[1], "Normal", row[2], 5000) for row in csv.reader(csvfile) if row[0].isdigit()]
        return batteries

    def connect(self, house_id,  battery_id):
        """
        Connect a house to a battery and change information in system accordingly
        """
        # get house
        H = [house for house in self.unconnected_houses if house.id == house_id]
        # error check
        if not H:
            print("House not found, try disconnecting it first")
            return
        if len(H) > 1:
            print("Mutiple houses found, please reload grid")
            return
        # unlist
        H = H[0]

        # get battery
        B = [battery for battery in self.batteries if battery.id == battery_id]
        # error check
        if not B:
            print("Battery not found, please enter the id not the index number")
            return
        if len(B) > 1:
            print("Mutiple batteries found, please reload grid")
            return
        # unlist
        B = B[0]

        # if house max_output exceeds battery capacity return and print error message
        if B.current_capacity < H.max_output:
            print(f"Battery capacity ({round(B.current_capacity, 2)}) is not sufficient")
            return

        # remove house from unconnected list
        self.unconnected_houses.remove(H)

        # get battery index in battery list of grid
        B_index = self.batteries.index(B)

        # Make a route and append it to the route list in the corresponding battery
        route = Route(H, B.id, B.location)
        self.batteries[B_index].routes.append(route)

        # print connection made
        print(f"connected house {H.id} with battery {B.id}")

        # recalculate battery current capacity
        self.batteries[B_index].current_capacity -= H.max_output

        # print leftover capacity
        print(f"capcity left on battery: {round(self.batteries[B_index].current_capacity, 2)}")

    def disconnect(self, house_id):
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
                    print(f"house {house_id} disconnected")
                    return
        # if house id not found print error message
        print("House not found, please check if house exists in grid.houses or excel file \nif it does exist please check grid.unconnected_houses \nif not present there, reload grid")
        return

    def calculate_total_cost(self):
        total_cost = sum([battery.calculate_routes_cost() for battery in self.batteries])
        return total_cost


    def greedy(self):
        # find min and max output value
        min = float('inf')
        max = 0
        for house in self.houses:
            if house.max_output > max:
                max = house.max_output
            if house.max_output < min:
                min = house.max_output

        # loop over batteries
        for battery in self.batteries:
            # repeat for amount of unconnected_houses
            for counter in range(len(self.unconnected_houses)):
                # find closest house
                house_id = battery.find_closest_house(self.unconnected_houses)

                # check if closest house is found
                if not house_id == None:
                    # find current house as object
                    for house in self.unconnected_houses:
                        if house_id == house.id:
                            H = house
                    # get difference between current capacity and house max_output
                    difference_best = battery.current_capacity - H.max_output
                    # find better option if difference is in range 5 to max_max_ouput
                    if difference_best > 5 and difference_best < max:
                        # loop over unconnected_houses
                        for house in self.unconnected_houses:
                            # difference of current loop house
                            difference_current = battery.current_capacity - house.max_output
                            # see if current house is a better fit
                            if difference_current < difference_best and difference_current > 0:
                                # set H object house_id and difference to new option
                                H = house
                                house_id = house.id
                                difference_best = battery.current_capacity - H.max_output

                    # find difference is still over 5 find if a combination of 2 house is better
                    current_best =  1000000000
                    house_id1, house_id2 =  -1, -1
                    if difference_best > 10:
                        for house1 in self.unconnected_houses:
                            for house2 in self.unconnected_houses:
                                if  0 < house1.max_output + house2.max_output - battery.current_capacity < 5 and house1.max_output + house2.max_output - battery.current_capacity < current_best:
                                    current_best = house1.max_output + house2.max_output - battery.current_capacity
                                    house_id = house1.id
                                    house_id2 = house2.id

                    self.connect(house_id, battery.id)
                else:
                    print("No houses to connect")

    def simple(self):
        for battery in self.batteries:
            for numb in range(150, 0, -1):
                self.connect(numb, battery.id)

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
            if capacity_taken + house.max_output < battery.max_capacity:
                capacity_taken += house.max_output
                max_connected_houses += 1
        # sort houses from largest to smallest max output
        self.unconnected_houses.sort(reverse=True, key=max_output_func)
        # get max amount of houses able to connect
        capacity_taken = 0
        min_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.max_capacity:
                capacity_taken += house.max_output
                min_connected_houses += 1

        range = (min_connected_houses, max_connected_houses)
        return range


    def find_best_option(self, houses, battery, sum_houses_capacity, sum_houses_distance):
        # alle combinaties/kinderen genereren voor een batterij
        #
        # als de kosten boven self.simple kosten oplossing komen dan afkappen
        # Dubbele combinaties?
        # volgorde maakt niet uit, dus het gaat om combinaties --> uitrekene min en max aantal huizen per batterij,
        # dus eerst sorteren en dan kijken hoeveel van de kleinste er in passen en hoeveel van de grootse er in passen
        # of kosten van een oplossing opslaan en zodra je er onder komt afkappen
        # als capaciteit is bereikt afpakken
        if sum_houses_capacity > battery.max_capacity:
            print("cap reached")
            return
        if sum_houses_distance > 500:
            print("longer route")
            return
        Grid.counter += 1

        new_houses = copy.deepcopy(houses)
        for house in new_houses:
            print(house)
            new_houses.remove(house)
            self.find_best_option(new_houses, battery, sum_houses_capacity, sum_houses_distance)

        # for house in houses:
        #     new_houses = copy.deepcopy(houses)
        #     print(house)
        #     for i in new_houses:
        #         print(i)
        #         if i.id == house.id:
        #             sum_houses_capacity += i.max_output
        #             dist =  distance(i.location, battery.location)
        #             sum_houses_distance += dist
        #         new_houses.remove(i)
        #     print(Grid.counter)
        #     self.find_best_option(new_houses, battery, sum_houses_capacity, sum_houses_distance)
        #     for i in new_houses:
        #         print(i)
        return
