import numpy as np
import random
import pprint

from numpy.core.defchararray import array
###
filePath="/Users/veliakdeniz/Desktop/Genetic_Algorithms_TSP/CityCoordinates.tsp"
###

class Location:
    def __init__(self,arr) -> None:
        self.location_no,self.lat,self.long=arr;

    def relativeDistance(self,location):
        return np.sqrt((self.lat - location.lat)**2 + (self.long - location.long)**2)

#Calcultes the distance between two diferrent Location object
def calculateDistance(location1:Location,location2:Location)->int:
    return np.sqrt((location1.lat - location2.lat)**2 + (location1.long - location2.long)**2)



#Reads population coordinates from file
def getLocationCoordinates(filePath:str) -> array:
    with open(filePath,"r") as file:
        location_coordinates=list(list(map(int,x.replace('\n',"").split(" "))) for x in file.readlines()[3:-1])
        return location_coordinates

#Returns an array populated with Location objects 
def initLocations(location_coordinates:array) -> array:
    location_array=[]
    location_array.extend(list(Location(x) for x in location_coordinates))
    return(location_array)

#Creates random route from Location objects
def createRandomRoute(location_list:array)->array:
    random_route=random.sample(location_list,len(location_list))
    return random_route

#Creates population from Location objects in given size
def createPopulation(population_size:int,location_list:array)->array:
    population=[]
    for i in range (0,population_size):
        population.append(createRandomRoute(location_list))
    return population

#Ranks 1 route's fitness based on fitness algorithm.
def rankRoute(route_array:array)->int:
    fitness_point=0
    start_location=route_array[0]
    current_location=start_location
    for i in route_array[2:]:
        fitness_point+=calculateDistance(current_location,i)
        current_location=i
    fitness_point+=calculateDistance(current_location,start_location)
    return fitness_point





#Ranks routes in a population and puts them in a dictionary
"""def rankPopulation(population:array)->dict:
    ranking={}"""


loc_list=initLocations(getLocationCoordinates(filePath))
population=createPopulation(10,loc_list)
print(rankRoute(population[0]))
#pprint.pprint(list(list((x.location_no) for x in population[i]) for i in range(0,len(population))))