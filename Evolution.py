import math
import os
import pickle
import random
import sys
from datetime import datetime, timedelta


class City:

    def __init__(self, name, coords):
        self.name = str(name)
        self.x = coords[0]
        self.y = coords[1]


class Creature:

    def __init__(self, genes, method, radius):
        self.genes = genes
        self.size = len(genes)
        self.method = method
        self.radius = radius
        self.score = 0

        for idx in range(len(genes) - 1):
            if method == 'plane':
                self.score += self.calculate_distance_plane(
                    genes[idx], genes[idx + 1])

            elif method == 'planet':
                self.score += self.calculate_distance_planet(
                    genes[idx], genes[idx + 1])

        self.path = [self.genes[i].name for i in range(len(self.genes))]

    def breed(self, parent2, mutation_chance):
        new_genes = [-1 for i in range(self.size)]
        genes_list = []

        # parent 1
        parent1_num = random.randint(0, self.size)
        parent1_genes = random.sample(range(self.size), k=parent1_num)
        for idx in parent1_genes:
            new_genes[idx] = self.genes[idx]
            genes_list.append(self.genes[idx])

        # parent 2
        parent2_genes = []
        for gene in parent2.genes:
            if gene not in genes_list:
                parent2_genes.append(gene)

        # combination
        idx = 0
        for i in range(len(new_genes)):
            if new_genes[i] == -1:
                new_genes[i] = parent2_genes[idx]
                idx += 1

        # mutation
        for gene in new_genes:
            roll = random.randint(1, 100)
            if roll <= mutation_chance:
                idx1 = random.randint(0, self.size - 1)
                idx2 = random.randint(0, self.size - 1)
                # swap
                new_genes[idx1], new_genes[idx2] = new_genes[idx2], new_genes[idx1]

        return Creature(
            genes=new_genes,
            method=self.method,
            radius=self.radius)

    def calculate_distance_plane(self, city1, city2):
        """Calculates the distance between two cities using
        the Pythagorean Theorem
        https://en.wikipedia.org/wiki/Pythagorean_theorem"""

        score = 0
        score += math.hypot(city2.x - city1.x, city2.y - city1.y)
        return score

    def calculate_distance_planet(self, city1, city2):
        """Calculates the distance between two cities
        using the haversine formula
        https://en.wikipedia.org/wiki/Haversine_formula"""

        score = 0
        lat1 = math.radians(city1.x)
        lon1 = math.radians(city1.y)
        lat2 = math.radians(city2.x)
        lon2 = math.radians(city2.y)
        lon = lon2 - lon1
        lat = lat2 - lat1
        hav = math.sin(lat / 2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(lon / 2) ** 2
        score += self.radius * \
            (2 * math.atan2(math.sqrt(hav), math.sqrt(1 - hav)))
        return score

    def __gt__(self, creature2):
        # this allows us to sort them
        return self.score > creature2.score


class Population:

    def __init__(
            self,
            target,
            population_size,
            method='planet'):
        """Genetic approach to the 'Travelling salesman problem'

        Arguments:
            target {dict} -- python dictionary: {'city_name':(x,y)}
            population_size {int} -- number of individuals, this number should
                be divisible by 4 (and will be rounded down in case its not)

        Keyword Arguments:
            method {str} -- aviable: 'plane' or 'planet', use 'planet' if
                you're considering real cities for increased accuracy
                (it takes the earths curvature into account during calculations)
                (default: {'planet'})
        """
        if method.lower() not in ['plane', 'planet']:
            raise ValueError(
                "Invalid argument: 'method', use 'plane' or 'planet'")
        self.method = method.lower()

        self.population_size = population_size - population_size % 4

        city_names = list(target.keys())
        city_coords = list(target.values())
        self.cities = []
        for idx in range(len(city_names)):
            city = City(city_names[idx],
                        city_coords[idx])
            self.cities.append(city)

        self.EARTH_RADIUS = 6373.0
        self.population = []

    def create_population(self):
        for i in range(self.population_size):
            genes = random.sample(self.cities, len(self.cities))
            creature = Creature(
                genes=genes,
                method=self.method,
                radius=self.EARTH_RADIUS)
            self.population.append(creature)
        self.population.sort()

    def natural_selection(self, survival_chance=1):

        new_population = []
        new_size = int(len(self.population) / 2)  # round down
        for idx in range(len(self.population[:new_size])):
            roll = random.randint(1, 100)
            if roll <= survival_chance:
                new_population.append(self.population[idx + new_size])
            else:
                new_population.append(self.population[idx])
        self.population = new_population

    def breed_all(self, mutation_chance=15):
        new_population = []
        for idx in range(0, len(self.population), 2):
            parent1 = self.population[idx]
            parent2 = self.population[idx + 1]
            baby1 = parent1.breed(parent2, mutation_chance)
            baby2 = parent2.breed(parent1, mutation_chance)
            new_population.extend([parent1, parent2, baby1, baby2])
        self.population = new_population
        self.population.sort()

    def one_step(self, mutation_chance=10, survival_chance=1):
        if not self.population:
            print("Creating new population")
            self.create_population()
        self.natural_selection(survival_chance)
        self.breed_all(mutation_chance)

    def save_population(self, file_path):
        with open(f'{file_path}', 'wb') as save:
            pickle.dump(self.population, save)

    def load_population(self, file_path):
        with open(f'{file_path}', 'rb') as pop:
            self.population = pickle.load(pop)

    def evolve(
            self,
            generations,
            mutation_chance=10,
            survival_chance=1,
            autosave_every=100,
            print_progress_bar=True):
        """Performs one_step() selected number of times, displays
        a progress bar and autosaves the population for later use

        Arguments:
            generations {int} -- number of iterations

        Keyword Arguments:
            mutation_chance {int} -- each new creature has a chance to have
                some of its genes swapped (default: {10})
            survival_chance {int} -- during natural selection some good
                creatures may die allowing lucky worse ones to survive
                increasing diversity (default: {1})
            autosave_every {int} -- creates a pickle file every x iterations,
                it can be later loaded using the load_population() function
                set to 0 to disable autosave (default: {100})
            print_progress_bar {bool} -- if True it'll print a progress bar
                containing current iteration, estimated time left and
                the best current score (default: {True})
        """

        if not self.population:
            print("Creating new population")
            self.create_population()

        start_time = datetime.now()

        if autosave_every > 0:
            name = f"Population {start_time:%d-%m-%Y %H-%M}"
            os.makedirs(f'{name}')

        for iteration in range(generations):
            self.one_step(mutation_chance, survival_chance)

            # autosave
            if autosave_every > 0 and (iteration + 1) % autosave_every == 0:
                self.save_population(f'{name}/generation {iteration + 1}')

            # progress bar
            if print_progress_bar is True:
                progress = (iteration + 1) / generations
                time_elapsed = (datetime.now() - start_time).seconds
                time_left = int(((time_elapsed / progress) * (1 - progress)))
                bar = f"[ {'#'*int(progress*20)}{'-'*(20-int((progress*20)))} ]"
                done = f"{iteration+1}/{generations}  {progress*100:.2f}%"
                timer = f"Estimated time left: {timedelta(seconds=time_left)}"
                best = f"Best score: {(self.population[0].score)}"
                progress_bar = f"{bar}  {done}  {timer}  {best}\r"
                sys.stdout.write(progress_bar)
                sys.stdout.flush()

    def __getitem__(self, key):
        return self.population[key]


if __name__ == '__main__':

    cities = {
        'Alabama': (-86.279118, -32.361538),
        'Arizona': (-112.073844, 33.448457),
        'Arkansas': (-92.331122, 34.736009),
        'California': (-121.468926, 38.555605),
        'Colorado': (-104.984167, 39.7391667),
        'Connecticut': (-72.677, 41.767),
        'Delaware': (-75.526755, 39.161921),
        'Florida': (-84.27277, 30.4518),
        'Georgia': (-84.39, 33.76),
        'Idaho': (-116.237651, 43.613739),
        'Illinois': (-89.650373, 39.783250),
        'Indiana': (-86.147685, 39.790942),
        'Iowa': (-93.620866, 41.590939),
        'Kansas': (-95.69, 39.04),
        'Kentucky': (-84.86311, 38.197274),
        'Louisiana': (-91.140229, 30.45809),
        'Maine': (-69.765261, 44.323535),
        'Maryland': (-76.501157, 38.972945),
        'Massachusetts': (-71.0275, 42.2352),
        'Michigan': (-84.5467, 42.7335),
        'Minnesota': (44.95, -93.094),
        'Mississippi': (-90.207, 32.320),
        'Missouri': (-92.189283, 38.572954),
        'Montana': (-112.027031, 46.595805),
        'Nebraska': (-96.675345, 40.809868),
        'Nevada': (-119.753877, 39.160949),
        'New Hampshire': (-71.549127, 43.220093),
        'New Jersey': (-74.756138, 40.221741),
        'New Mexico': (-105.964575, 35.667231),
        'New York': (-73.781339, 42.659829),
        'North Carolina': (-78.638, 35.771),
        'North Dakota': (-100.779004, 48.813343),
        'Ohio': (-83.000647, 39.962245),
        'Oklahoma': (-97.534994, 35.482309),
        'Oregon': (-123.029159, 44.931109),
        'Pennsylvania': (-76.875613, 40.269789),
        'Rhode Island': (-71.422132, 41.82355),
        'South Carolina': (-81.035, 34.000),
        'South Dakota': (-100.336378, 44.367966),
        'Tennessee': (-86.784, 36.165),
        'Texas': (-97.75, 30.266667),
        'Utah': (-111.892622, 40.7547),
        'Vermont': (-72.57194, 44.26639),
        'Virginia': (-77.46, 37.54),
        'Washington': (-122.893077, 47.042418),
        'West Virginia': (-81.633294, 38.349497),
        'Wisconsin': (-89.384444, 43.074722),
        'Wyoming': (-104.802042, -41.145548)
    }
    pop = Population(cities, 2000, method='planet')
    pop.evolve(1000, autosave_every=1000)
