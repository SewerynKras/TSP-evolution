# Genetic approach to the ['Traveling salesman problem'](https://simple.wikipedia.org/wiki/Travelling_salesman_problem)

## Usage example

```python
cities = {'Sacramento': (-121.468926, 38.555605),
          'Boston': (-71.0275, 42.2352),
          'Albany': (-73.781339, 42.659829),
          'Nashville': (-86.784, 36.165),
          'Madison': (-89.384444, 43.074722)}

size = 100

pop = Population(target=cities,
                 population_size=size,
                 method='planet')

pop.evolve(generations=500,
           mutation_chance=10,
           survival_chance=1,
           autosave_every=100,
           print_progress_bar=True)

print(pop[0].path)
print(pop[0].score)
```

You can also do each iteration 'by hand'

```python
    pop = Population(cities,size)
    pop.create_population()
    for i in range(500):
        pop.one_step(mutation_chance=10, survival_chance=1)
        print(f'Best score:{pop[0].score}, Iteration: {i+1}')
```

## Unit conversion

 To convert between different units of length or planet sizes you can change the EARTH_RADIUS variable

```python
pop = Population(cities,size)
pop.EARTH_RADIUS = 3959.0 # miles
pop.EARTH_RADIUS = 6371.0 # kilometers
```

## Loading and saving

To save the current population for future use you can use the save_population() function

```python
pop = Population(cities,size)
pop.evolve(500)
pop.save_population('population 500')
```

To load a previously saved population use the load_population() function (make sure that the target and population_size are the same)

```python
pop = Population(cities,size) 
pop.load_population('population 500')
```