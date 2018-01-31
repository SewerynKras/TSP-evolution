from random import randrange
import time
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg

fig = plt.figure()
canvas = fig.canvas
class Display(App):
	def build(self):
		box = BoxLayout()
		box.add_widget(canvas)
		canvas.draw()
		return box

#Create the first population
def _firstPopulation(populationSize,target,genes):
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
def _breed(population,mc,gen):
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
			evolvedPopulation.append(_mutate(baby,mc,gen))
		evolvedPopulation.append(first)
		evolvedPopulation.append(second)
	return evolvedPopulation

#Randmly change genes to increase gene diversity
def _mutate(individual,mutationChance,genes):
	newbaby = ''
	for i in range(len(individual)):
		luck = randrange(0,100)
		if luck < mutationChance:
			newbaby += genes[randrange(0,len(genes))]
		else:
			newbaby += individual[i]
	return newbaby

#Display the results in a nice graph 
def _displayGraph (best,average,worse,save,gen):
	axes = fig.add_axes([0.1,0.1,0.9,0.9])
	axes.set_xlabel("Generation")
	axes.set_ylabel("Points")
	axes.plot(range(gen),worse, label = "Worst", color = "#E24D4D",lw=5) 
	axes.plot(range(gen),average, label = "Average",color = "#E7E72E",lw=5)
	axes.plot(range(gen),best,label = "Best",color = "#48F127",lw=5)
	axes.legend()
	if save == True : 
		lc = time.localtime(time.time())
		fig.savefig("{}_{:02}_{:02}_{:02}_{:02}.png".format(lc.tm_year,lc.tm_mon,lc.tm_mday,lc.tm_hour,lc.tm_min),dpi=300)
	Display().run()

#The function you actually call :P
def evolutionSimulator(Target,
		PopulationSize=1000,
		MutationChance=10,
		Genes="qwertyuiopasdfghjklzxcvbnm?!'.,QWERTYUIOPASDFGHJKLZXCVBNM 1234567890",
		GradientChance=5,
		DisplayResults=False,
		TimeLimit=600,
		SaveGraph=False):

	startTime = float(time.time()) #use it later to measure time
	population = _firstPopulation(PopulationSize,Target,Genes)
	population = _ratePopulation(population,Target)
	score = len(Target)
	print ("Starting the experiment now. {} random individuals have been created.".format(PopulationSize))
	generation = 0
	best = [] #collect data about the best individuals
	mid = [] #collect data about average individuals
	worst = [] #collect data about the worst individuals    
	found = False
	while(not found) :
		generation += 1
		population = _naturalSelection(population,GradientChance)
		population = _breed(population,MutationChance,Genes)
		population = _ratePopulation(population,Target)
		if DisplayResults == True : 
			print("Best gen {:03}:\t{}\t score:{:02}/{:02}\t time elapsed: {}s".format(generation,population[0][0],population[0][1],score,
	                                                                   "%.2f"% (time.time()-startTime)))
		best.append(population[0][1])
		mid.append(population[int(PopulationSize/2)][1])
		worst.append(population[PopulationSize-1][1])

		#if we got it
		if population[0][1] == score :
			found = True
			print ('It took {} generations and {} seconds for the experiment to end successfully!'.format
				(generation,"%.2f"% (time.time()-startTime)))
			_displayGraph(best,mid,worst,SaveGraph,generation)

		#if time ran out
		elif time.time() - startTime > TimeLimit :
			found = True
			print ("Perfection too hard to achieve in the given time.The experiment has been stopped")
			_displayGraph(best,mid,worst,SaveGraph,generation)