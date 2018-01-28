from random import randrange
import time
import matplotlib.pyplot as plt

#Create the first population
def firstPopulation(populationSize,target,genes):
    pop=[]
    for i in range(populationSize):
        current = ""
        for idx in range(len(target)):
            current += genes[randrange(0,len(genes))]
        pop.append(current)
    return pop

#Give every individual a rating and sort the population
def ratePopulation(population,target):
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
def naturalSelection(population,gradientChance):
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
def breed(population,mc,gen):
	evolvedPopulation = []
	for i in range(0,len(population),2):
		first = population[i][0]
		second = population[i+1][0]
		for offspring in range (2) :
			baby = ""
			for idx in range(len(first)):
				luck = randrange(0,2)
				if luck == 0 : 
					baby += first[idx]
				else :
					baby += second[idx]
			evolvedPopulation.append(mutate(baby,mc,gen))
		evolvedPopulation.append(first)
		evolvedPopulation.append(second)
	return evolvedPopulation

#Randmly change genes to increase gene diversity
def mutate(individual,mutationChance,genes):
    newbaby = ''
    for i in range(len(individual)):
        luck = randrange(0,100)
        if luck < mutationChance:
            newbaby += genes[randrange(0,len(genes))]
        else:
        	newbaby += individual[i]
    return newbaby


def displayGraph (best,average,worse,save,gen):
	fig = plt.figure()
	axes = fig.add_axes([0,0,1,1])
	axes.set_xlabel("Generation")
	axes.set_ylabel("Points")
	axes.plot(range(gen),worse, label = "Worst", color = "#FF66B2",lw=2) 
	axes.plot(range(gen),average, label = "Average",color = "#CCCC00",lw=2)
	axes.plot(range(gen),best,label = "Best",color = "#00CC66",lw=2)
	axes.legend()
	plt.show()
	if save == True : 
		lc = time.localtime(time.time())
		fig.savefig("{}_{}_{}_{}_{}.png".format(lc.tm_year,lc.tm_mon,lc.tm_day,lc.tm_hour,lc.tm_min),dpi=300)

#The function you actually call :P
def evolutionSimulator( Target,
						PopulationSize=1000,
						MutationChance=10,
						Genes="qwertyuiopasdfghjklzxcvbnm?!'.,QWERTYUIOPASDFGHJKLZXCVBNM 1234567890",
						GradientChance=5,
						DisplayResults=False,
						TimeLimit=600,
						SaveGraph=False):
	
	startTime = float(time.time()) #use it later to measure time
	population = firstPopulation(PopulationSize,Target,Genes)
	population = ratePopulation(population,Target)
	score = len(Target)
	print ("Starting the experiment now. {} random individuals have been created.\n".format(PopulationSize))
	generation=0
	best = [] #collect data about the best individuals
	mid = [] #collect data about average individuals
	worst = [] #collect data about the worst individuals    
	found = False
	while(not found):
		generation += 1
		population = naturalSelection(population,GradientChance)
		population = breed(population,MutationChance,Genes)
		population = ratePopulation(population,Target)
		if DisplayResults == True : 
			print("Best gen {}:\t{}\t score:{}/{}\t time elapsed: {}s".format(generation,population[0][0],population[0][1],score,
	                                                                   "%.2f"% (time.time()-startTime)))
		best.append(population[0][1])
		mid.append(population[int(PopulationSize/2)][1])
		worst.append(population[PopulationSize-1][1])

		#if we got it
		if population[0][1]==score:
			found = True
			print ('\nIt took {} generations and {} seconds for the experiment to end successfully!'.format
				(generation,"%.2f"% (time.time()-startTime)))
			displayGraph(best,mid,worst,SaveGraph,generation)
        
        #if time ran out
		elif time.time()-startTime >TimeLimit:
			found = True
			print ("\nPerfection too hard to achieve in the given time.The experiment has been stopped")
			displayGraph(best,mid,worst,SaveGraph,generation)
#Test
#evolutionSimulator("Lets make this one a bit harder hehe",DisplayResults=True)
