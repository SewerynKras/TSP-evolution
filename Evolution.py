from random import randrange
import time
#import matplotlib.pyplot as plt
#Create the first population
genes="aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPrRsStTuUvVwWxXyYzZ12345678!?,.'=+-/()*# "
def _firstPopulation(populationSize,target):
	population=[]
	for i in range(populationSize):
		current = ""
		for idx in range(len(target)):
			current += genes[randrange(0,len(genes))]
		population.append(current)
	return population
#Give every individual a rating and sort the population
def _ratePopulation(population,target):
	newPopulation = []
	for i in range(len(population)):
		current = population[i]
		score = 0
		for idx in range(len(current)):
			if (current[idx]==target[idx]):
				score+=1
		newPopulation.append([current,score])
	return sorted(newPopulation,key = lambda newPopulation: newPopulation[1],reverse = True) #sort by the second argument
#Kill half the population with a slight gradient (to increase gene diversity)
def _naturalSelection(population,gradientChance):
	half = int(len(population)/2)
	newPopulation = []
	for idx in range(half):
		luck = randrange(0,100)
		if luck < gradientChance :
			newPopulation.append(population[half + idx])
		else :
			newPopulation.append(population[idx])
	return newPopulation
#Let the remaining individuals breed and create the next generation
def _breed(population,mc,):
	evolvedPopulation = []
	for i in range(0,len(population),2):
		first = population[i][0]
		second = population[i+1][0]
		for offspring in range (2) :
			baby = ""
			for idx in range(len(second)):
				luck = randrange(0,2)
				if luck == 0 : 
					baby += first[idx]
				else :
					baby += second[idx]
			evolvedPopulation.append(_mutate(baby,mc))
		evolvedPopulation.append(first)
		evolvedPopulation.append(second)
	return evolvedPopulation
#Randmly change genes to increase gene diversity
def _mutate(individual,mutationChance):
	newbaby = ''
	for i in range(len(individual)):
		luck = randrange(0,100)
		if luck < mutationChance:
			newbaby += genes[randrange(0,len(genes))]
		else:
			newbaby += individual[i]
	return newbaby
#The function you actually call :P
def evolutionSimulator(Target,
		PopulationSize=1000,
		MutationChance=10,
		GradientChance=5,
		TimeLimit=600,
		DisplayResults=True,
		SaveGraph=False):
	startTime = float(time.time()) #use it later to measure time
	population = _firstPopulation(PopulationSize,Target)
	population = _ratePopulation(population,Target)
	score = len(Target)
	best=[]
	mid=[]
	worst=[]
	generation=0
	print ("Starting the experiment now. {} random individuals have been created.".format(PopulationSize))   
	found = False
	while(not found) :
		generation += 1
		population = _naturalSelection(population,GradientChance)
		population = _breed(population,MutationChance)
		population = _ratePopulation(population,Target)
		if DisplayResults == True : 
			print("Best gen {:03}:\t{}\t score:{:02}/{:02}\t time elapsed: {}s".format(generation,population[0][0],population[0][1],score,
	                                                                   "%.2f"% (time.time()-startTime)))
		best.append(population[0][1])
		mid.append(population[int(PopulationSize/2)][1])
		worst.append(population[PopulationSize-1][1])
		#EvolutionSimulator().refresh(best,mid,worst,generation)
		#if we got it
		if population[0][1] == score :
			found = True
			print ('It took {} generations and {} seconds for the experiment to end successfully!'.format
				(generation,"%.2f"% (time.time()-startTime)))
		#	_displayGraph(best,mid,worst,SaveGraph,generation)
		#if time ran out
		elif time.time() - startTime > TimeLimit :
			found = True
			print ("Perfection too hard to achieve in the given time.The experiment has been stopped")
		#	_displayGraph(best,mid,worst,SaveGraph,generation)
#evolutionSimulator(Target="This is just a test 123",DisplayResults=True,PopulationSize=200)
def evolvePopulation(population=[],Target="",MutationChance=10,GradientChance=5):
	population = _naturalSelection(population,GradientChance)
	population = _breed(population,MutationChance)
	population = _ratePopulation(population,Target)
	return population