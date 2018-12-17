# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes
import time

def repeat_hillclimber_greedy(grid, cost_bound, repeats):
    """
    Repeat hillclimber takes a certain cost bound and an amount of repeats as input
    The algorithm first finds a random solution for connecting all houses
    Then it runs a hillclimber to find the local mamximum
    It will repeat untill a solution is found under the cost bound
    Or untill amount of repeats is reached
    House combinations for best solution will be saved in .json
    Cost results for random and hillclimbers are saved aswell
    """


    # initiate
    counter = 0
    costs_random = [999999, 999998]
    times_random =  []
    costs_hillclimber = [999999, 999998]
    times_hillclimber = []
    current_lowest_cost =  float('inf')
    combination = {}

    # loop untill repeats is reached or untill combination under lower bound is found
    while min(costs_hillclimber) > cost_bound and counter < repeats:


        # get random solution save time and costs
        random_start = time.time()
        grid = Algoritmes.random_connect(grid)
        random_stop = time.time()

        times_random.append(random_stop - random_start)

        cost_r = grid.calculate_total_cost()
        costs_random.append(cost_r)


        # run hillclimber save time and costs
        hill_start = time.time()
        grid = Algoritmes.hillclimber_greedy(grid)
        hill_stop = time.time()

        times_hillclimber.append(hill_stop - hill_start)

        cost_h = grid.calculate_total_cost()
        costs_hillclimber.append(cost_h)



        # if cost of hillclimber is best solution save data for .json export
        if cost_h < current_lowest_cost:
            current_lowest_cost = cost_h
            current_combi = {}
            for battery in grid.batteries:
                house_ids = []
                for route in battery.routes:
                    house_id = route.house.id
                    house_ids.append(house_id)
                current_combi[f'{battery.id}'] = house_ids
            current_combi["Costs best solution"] = cost_h
            combination = current_combi

        # disconnect for new iteration
        grid.disconnect_all()
        counter += 1
        print(counter)

    # save all results in dict aswell
    combination["All random results"] = costs_random
    combination["All hillclimber results"] = costs_hillclimber
    combination["Random times"] = times_random
    combination["Hillclimber times "] = times_hillclimber

    # get current datetime in string
    dt = datetime.now()
    stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

    # dump data of best found solution to .json file
    with open(f'Results/RandomHillclimber/{grid.name}_Best_solution_{combination["Costs best solution"]}_{stdt}_random_optimized_with_hillclimber_{counter}_repeats_bound_{cost_bound}.json', 'w') as f:
        json.dump(combination, f,indent=4)
