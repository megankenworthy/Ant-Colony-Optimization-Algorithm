# Megan Kenworthy
# December 12, 2017
# Ant colony optimization for supply chain data

import random
import numpy as np
import csv
import itertools as tool #imports itertools library
import time
import matplotlib.pyplot as plotter


with open('european_cities.csv','rb') as f:
    
    reader = csv.reader(line.replace(';',',') for line in f) 
    data = list(reader)
    Cities = data[0]
    data = data[1:]     #pop off first line 

    Data = [] 			#getting the distances in int
    for line in data:
    	newline = [float(i) for i in line]
    	Data.append(newline)

def antcolony(Alpha,Beta,TRIALS,Ants):

	#we can have the number of ants equal the number of cities 

	#Tij - amount of pheromone on edge ij
	#Nij - desireablility of edge ij (i/length of edge)
	# alpha controls the influence of Tij (the amount of pheromone on edge ij)
	# beta controls the influence of Nij aka how much weight you want to put on the dist
	alpha = Alpha 	#influence of pheromone
	beta = Beta   #influence of distance


	#desireability, is just 1/dist for each of the values in distances
	#this is just the data for the distances from each city 
	Distances = Data 		#just setting it to data 

	#Tij graph
	Pheromones = [1]*len(Distances)
	for i in range(len(Distances)):
		Pheromones[i] = [1]*len(Distances)


##############
#EVERYTHING HAS BEEN SET UP NOW 


	#now we want to do x number of trials placing our A number 
	#ants and having them find the best trails
	Pathlengths = []
	Pathlenavg = []
	for trial in range(TRIALS):
		#setting up 30 ants at a starting city
		numberofants = Ants
		antpath = [0]*numberofants
		for i in range(numberofants): 
			antpath[i] = [0]*len(Distances)
			antpath[i][0] = random.randint(0,23)

		#print('antpath',antpath)

		for ant in range(len(antpath)):
			Ant = antpath[ant]
			#Ant[0] = random.randint(0,23)
			
		
			pathposition = 0 
		
			#set up prob matrix for each ant 
			Probability = [0]*len(Distances)
			for i in range(len(Distances)):
				Probability[i] = [0]*len(Distances)

	
			pathlength = 0 

			visitablelist = [i for i in range(0,24)]
			visitablelist.remove(Ant[0]) #removes by value 

			while pathposition<23:
			
				Antcity = Ant[pathposition]

				#we can get the bottom of the probability eq here bec its based on the visit list
				Bottomofprobeq = 0
				for city in visitablelist:  
						P1 = (Pheromones[Antcity][city])*alpha
						D1 = (1/Distances[Antcity][city])*beta
						Bottomofprobeq = Bottomofprobeq + P1*D1
			
				#now doing the full calculation
				for city in visitablelist: 
					Topofprobeq1 = (Pheromones[Antcity][city])*alpha
					Topofprobeq2 = (1/(Distances[Antcity][city]))*beta
					Topofprobeq = Topofprobeq1*Topofprobeq2

					if Bottomofprobeq != 0:
						Probability[Antcity][city] = Topofprobeq/Bottomofprobeq
					else: 
						Probability[Antcity][city] = 0


				maxprob = Probability[Antcity].index(max(Probability[Antcity]))
				if maxprob not in visitablelist: 
					maxprob = random.choice(visitablelist)
				
				prevcity = Ant[pathposition]
				visitablelist.remove(maxprob)
				Ant[pathposition+1] = maxprob
				pathlength = pathlength + Distances[prevcity][maxprob]

				pathposition = pathposition+1
		
			#print('starting city', Ant[0],'ending city',Ant[23])

			Startingcity = Ant[0]
			gettinghome = Ant[23]
			distancehome = Distances[gettinghome][Startingcity]
			

			#print('distancehome',distancehome)
			pathlength = pathlength+distancehome 	
			
			##save pathlengths
			Pathlengths.append(pathlength)

			#updating the pheromone trail
			#Q is a constant pheromone value something like 60k lets say
			Q = 60000

			#phereomone decay variable 
			pdecay = .1

			#we have to go through the ant path and update the pheromones 
			updatepath = Ant
			
			for location in range(len(updatepath)):
				#total pheromone deposit variable
				
				if location == len(updatepath)-1:
					lastdeposit = Distances[gettinghome][Startingcity] 
					Pheromones[gettinghome][Startingcity] = (1-pdecay)*lastdeposit + Q/pathlength

				else: 
					city1 = updatepath[location]
					city2 = updatepath[location+1]
					pdeposit = Distances[city1][city2] 	
					Pheromones[city1][city2] = (1-pdecay)*pdeposit + Q/pathlength
		
			#print('the ant paths',antpath)
			#print('pathlengths',Pathlengths)
			#print('pathlengths',Pathlengths)
		pathlenaverage = sum(Pathlengths)/len(Pathlengths) #numberofants
		Pathlenavg.append(pathlenaverage)
	
	return(Pathlenavg)


def main():

	trialgraph = []
	ultimateval = []
	for i in range(1,101): 
		newgraph = antcolony(.65,.35,60,30)
		ultimateval.append(sum(newgraph)/len(newgraph))
	
	print(sum(ultimateval)/len(ultimateval))
	#print(newgraph)
	#	trialtest = sum(newgraph)/len(newgraph)
	#	trialgraph.append(trialtest)
	#print(trialgraph)

	#plotter.plot(range(1,101),trialgraph)
	#plotter.show()

	#betaval = []
	#alphabetagraph = []
	#for i in range(1,21):
	#	beta = .05*i 		#pheromone
	#	alpha = 1-beta 		#distance 
	
	#	betaval.append(beta)

	#	trials = 25 
	#	graphtoplot = antcolony(alpha,beta,trials)
	#	alphabetaAdd = sum(graphtoplot)/len(graphtoplot)
	#	alphabetagraph.append(alphabetaAdd)


	#print('alpha g',alphabetagraph)

	#findmin = min(alphabetagraph)
	#findminindex = alphabetagraph.index(findmin)

	
	#plotter.plot(betaval,alphabetagraph,betaval[findminindex],alphabetagraph[findminindex],'bo')
	#plotter.title('Average Tour Lengths for Different Influence on Distance Between Cities')
	#plotter.xlabel('Influence of Distance on Choosing Next City')
	#plotter.ylabel('Tour Length')
	#plotter.show()

	#print('totalavg',sum(Pathlenavg)/len(Pathlenavg))

main() 
