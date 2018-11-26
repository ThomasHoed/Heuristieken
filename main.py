import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    i = 3
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)

    # grid.draw_grid()
    # grid.greedy()
    # grid.random_move_greedy_hillclimber(10)
    # grid.move_batteries_random()
    grid.greedy()
    # grid.draw_grid()
    grid.hillclimber()
    # grid.draw_grid()
    cost = grid.calculate_total_cost()
    print(cost)
    # grid.hillclimber()
    # grid.draw_routes()
    # info = {}
    # for i in range(2):
    #     grid.move_batteries_random()
    #     grid.greedy()
    #     grid.hillclimber()
    #     cost = grid.calculate_total_cost()
    #     info[i+1] = {'Cost':cost, 'Location': [battery.location for battery in grid.batteries]}
    #     grid.disconnect_all()
    #
    # print(info)
    #
    # grid.draw_all()
    # plt.show()





    # grid.greedy()
    # grid.hillclimber()
    # print(grid.calculate_total_cost())

    # for house in grid.houses:
    #     print(house.max_output)
    # grid.simple()
    # print(grid.range_connected(grid.batteries[0]))
    # grid.greedy()
    # print(grid.calculate_total_cost())
    # wijk_naam = "wijk3"
    # cost_bound = 46258
    # repeats = 1500
    # grid.random_hillclimber(cost_bound, repeats)

    # grid.greedy_alt()







    # grid.greedy()
    # grid.simple()
    # x = grid.calculate_total_cost() + 25000
    # grid.hillclimber()
    # # print(x)
    # print(grid.calculate_total_cost() + 25000)
    print(len(grid.unconnected_houses))
    # grid = Grid("wijk2")
    # print(sum(grid.shortest_paths()))
    # print(sum(grid.longest_paths()))
    #
    # grid = Grid("wijk3")
    # print(sum(grid.shortest_paths()))
    # print(sum(grid.longest_paths()))

    # print(grid.range_connected())





    # grid.find_best_option(grid.unconnected_houses, grid.batteries[0], 0, 0)

    # grid.simple()
    # grid.greedy()
    # for i in range(5):
    #     x= grid.batteries[i].calculate_routes_cost()
    #     print(x/9)
    # x = grid.calculate_total_cost()
    # print(x)
    # #
    # for i in grid.unconnected_houses:
    #     print(i)
    # sum_output = sum([i.max_output for i in grid.unconnected_houses])
    #
    # for i in grid.batteries:
    #     print(i.current_capacity)
    # print(sum_output)
    # #
    # #
    # for i in grid.batteries[0].routes:
    #     print(i.house.max_output)
    # closest_house = grid.batteries[0].find_closest_house([])
    # print(closest_house)
    # grid = Grid("wijk1")
    # grid.greedy()
    # first = grid.calculate_total_cost()
    # grid.hillclimber()
    # second = grid.calculate_total_cost()
    # difference = first - second
    # print(difference)
    # print(grid.unconnected_houses)
    #
    # grid.draw_grid([10, 28], [9, 3])
