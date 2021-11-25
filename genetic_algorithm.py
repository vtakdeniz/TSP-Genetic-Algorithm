from typing import List
import numpy as np
import random
import pprint
from itertools import islice

###
filePath="/Users/veliakdeniz/Desktop/Genetic_Algorithms_TSP/CityCoordinates.tsp"
population_size=50
mutation_chance=0.50
parent_selection_count=20
elitisim_count=int(parent_selection_count/2)
crossover_chance=1
chromosome_length=0
###

class Location:
    def __init__(self,arr) -> None:
        self.location_no,self.lat,self.long=arr;

    def relativeDistance(self,location):
        return np.sqrt((self.lat - location.lat)**2 + (self.long - location.long)**2)

    def info(self):
        return f"location no : {self.location_no} , latitute : {self.lat} , longitute : {self.long} "


#Calcultes the distance between two diferrent Location object
def calculateDistance(location1:Location,location2:Location)->int:
    return np.sqrt((location1.lat - location2.lat)**2 + (location1.long - location2.long)**2)

#Reads population coordinates from file
def getLocationCoordinates(filePath:str) -> list:
    with open(filePath,"r") as file:
        location_coordinates=list(list(map(int,x.replace('\n',"").split(" "))) for x in file.readlines()[3:-1])
    global chromosome_length
    chromosome_length=len(location_coordinates)
    return location_coordinates

#Returns an array populated with Location objects 
def initLocations(location_coordinates:list) -> list:
    location_array=[]
    location_array.extend(list(Location(x) for x in location_coordinates))
    return(location_array)

#Creates random route from Location objects
def createRandomRoute(location_list:list)->list:
    random_route=random.sample(location_list,len(location_list))
    return random_route

#Creates population from Location objects in given size
def createPopulation(population_size:int,location_list:list)->list:
    population=[]
    for i in range (0,population_size):
        population.append(createRandomRoute(location_list))
    return population

#Ranks one route's fitness based on fitness criteria.
def rankRoute(route_array:list)->int:
    fitness_point=0
    start_location=route_array[0]
    current_location=start_location
    for i in route_array[1:]:
        fitness_point+=calculateDistance(current_location,i)
        current_location=i
    fitness_point+=calculateDistance(current_location,start_location)
    fitness_point=1/fitness_point
    return fitness_point

#Ranks routes in a population and returns a list of tuples containint rankings and their corresponding index in the population list
def rankPopulation(population:list)->dict:
    ranking={}
    for i in range(len(population)):
        ranking[i]=rankRoute(population[i])
    return sorted(ranking.items(),key=lambda x: x[1],reverse=True)

#Returns list of routes chromosomes for breeding 
def createMatingPool(population:list,ranking:list)->list:
    index=[]
    chromosomes=[]
    for rank in ranking[:parent_selection_count]:
        index.append(rank[0])
    for i in index:
        chromosomes.append(population[i])
    return random.sample(chromosomes,len(chromosomes)) #list((location for location in population[i]) for i in index)

#Splits given list to given numebr
def chunks(l:list, n:int)->list:
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

#Crossovers two differentmtypes of chromosomes
def breed(chromosome1:list,chromosome2:list)->list:
    #TODO: Implement different crossover
    if(random.random()<(1-crossover_chance)):
        return [chromosome1,chromosome2][random.randint(0,1)]
    child=[]
    subchild1=[]
    subchild2=[]
    subchild3=[]

    index1=int(random.random()*len(chromosome1))
    index2=int(random.random()*len(chromosome2))    
    startIndex=min(index1,index2)
    endIndex=max(index1,index2)
    half_chromosome2_len=int(len(chromosome2)/2)

    for i in range(startIndex,endIndex):
        subchild1.append(chromosome1[i])
    for i in range(0,half_chromosome2_len):
        if chromosome2[i] not in subchild1:
            subchild2.append(chromosome2[i])
    for i in range(half_chromosome2_len,len(chromosome2)):
         if chromosome2[i] not in subchild1 and chromosome2[i] not in subchild2:
            subchild3.append(chromosome2[i])

    subchild_collection=[subchild1,subchild2,subchild3]
    subchild_sample=random.sample(subchild_collection,len(subchild_collection)) 
    for subchild in subchild_sample:
        child += subchild
    return child

#Returns collection of offsprings
def breedMatingPool(mating_pool:list)->list: 
    children=[]
    splitted_elemenets=list(chunks(mating_pool,2))

    for i in splitted_elemenets:
        ch=breed(i[0],i[1])     
        children.append(ch)

        ###Assertion###
        list_of_breed_location_no=list(l.location_no for l in ch)
        assert(len(list_of_breed_location_no) == len(set(list_of_breed_location_no)))
        assert(len(list_of_breed_location_no) == chromosome_length)
        ###Assertion###

    return children


loc_list=initLocations(getLocationCoordinates(filePath))
population=createPopulation(population_size,loc_list)
list_of_locations=list(list((p.location_no for p in population[i])) for i in range(len(population)))
rank=rankPopulation(population)
pool=createMatingPool(population,rank)
children=breedMatingPool(pool)
