from random import randrange
import time
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

def firstPopulation(size,target,genes):
    pop=[]
    for i in range(size):
        current = ""
        for idx in range(len(target)):
            current += genes[randrange(0,len(genes))]
        pop.append(current)
    return pop

def ratePopulation(population,target):
    newPopulation = []
    for i in range(len(population)):
        current = population[i]
        score = 0
        for idx in range(len(current)):
            if (current[idx]==target[idx]): score+=1
        newPopulation.append([current,score])
    return sorted(newPopulation,key = lambda newPopulation: newPopulation[1],reverse = True)

def breed(population,mutationChance,genes,target):
    evolvedPopulation = []
    size=int((len(population))/2)
    for i in range(size):
        first = population[i][0]
        second = population[i+1][0]
        baby1 = ""
        for idx in range(len(first)):
            luck = randrange(1,3)
            if luck%2==0: baby1 += first[idx]
            else: baby1 += second[idx]
        evolvedPopulation.append(mutate(baby1,mutationChance,genes))
        evolvedPopulation.append(population[i][0])
    #newBaby = ''
    #for idx in range(len(target)):
    #    newBaby += genes[randrange(0,len(genes))]
    #evolvedPopulation.append(mutate(newBaby,mutationChance,genes))
    return evolvedPopulation

def mutate(individual,chance,genes):
    newbaby = ''
    for i in range(len(individual)):
        luck = randrange(0,100)
        if luck<chance:
            newbaby+=genes[randrange(0,len(genes))]
        else:newbaby += individual[i]
    return individual

def evolutionSimulator(populationSize,mutationChance,genes,target):
    startTime = float(time.time())
    population = firstPopulation(populationSize,target,genes)
    population = ratePopulation(population,target)
    score = len(target)
    print ("Starting the experiment now. {} random individuals have been created.\n".format(populationSize))
    theone = population[0][0]
    found = False
    gen=0
    best = []
    mid = []
    worse = []     
    fig = plt.figure()
    axes = fig.add_axes([0,0,1,1])
    while(not found):
        gen+=1
        population = breed(population,mutationChance,genes,target)
        population = ratePopulation(population,target)

        print("Best gen {}:\t{}\t score:{}/{}\t time elapsed: {}s".format(gen,population[0][0],population[0][1],score,
                                                                       "%.2f"% (time.time()-startTime)))
        
        best.append(population[0][1])
        mid.append(population[int(populationSize/2)][1])
        worse.append(population[populationSize-1][1])

        
        if population[0][1]==score:
            found = True
            print ('\nIt took {} generations and {} seconds for the experiment to end successfully!'.format
                   (gen,"%.2f"% (time.time()-startTime)))
            axes.plot(range(gen),best,label = "Best",color = "#00CC66",lw=2)
            axes.plot(range(gen),mid, label = "Average",color = "#CCCC00",lw=2)
            axes.plot(range(gen),worse, label = "Worse", color = "#FF66B2",lw=2)
            axes.set_xlabel("Generation")
            axes.set_ylabel("Points")
            axes.legend()
            fig.savefig("Example.png",dpi=300)
            
        elif time.time()-startTime >90:
            found = True
            print ("\nPerfection too hard to achieve in a resonable time... Experiment has been stopped")
            axes.plot(range(gen),best,label = "Best",color = "#00CC66",lw=2)
            axes.plot(range(gen),mid, label = "Average",color = "#CCCC00",lw=2)
            axes.plot(range(gen),worse, label = "Worse", color = "#FF66B2",lw=2)
            axes.set_xlabel("Generation")
            axes.set_ylabel("Points")
            axes.legend()
           #fig.savefig("Example.png",dpi=300)

evolutionSimulator(1000,60,"qwertyuiopasdfghjklzxcvbnm?!'.,QWERTYUIOPASDFGHJKLZXCVBNM 1234567890","what does this even do lets be honest")

