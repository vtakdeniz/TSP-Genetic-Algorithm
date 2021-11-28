from typing import final
import genetic_algorithm as ga_util
import json
import os
import sys

constants_file = open("constants.json")
constants=json.load(constants_file)["main_constants"]
constants_file.close()

#######
print_best_ranking_rate=constants["print_best_ranking_rate"]
generation_count=constants["generation_count"]
#######

class terminal_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    STANDART = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

purple=terminal_colors.HEADER
bold=terminal_colors.BOLD
red=terminal_colors.RED
yellow=terminal_colors.YELLOW
standart=terminal_colors.STANDART
cyan=terminal_colors.OKCYAN
green=terminal_colors.OKGREEN
blue=terminal_colors.OKBLUE

def printConstants()->None:
    print(bold+red+"******** Genetic Algorithm Constans **********"+standart)
    ga_util.printConstants(bold,cyan,green)
    print(bold+red+"******** Main Application Constans ***********"+standart)
    print(bold+cyan+f"Generation Count : {green}{generation_count}"+standart)
    print(bold+cyan+f"Printing Rate : {green}{print_best_ranking_rate}"+standart)

def printInfo(generation_count,population,ranking):
    os.system('clear')
    printConstants()
    print("----------------------------------------------")
    print(yellow+bold+"Generation : "+standart+green+str(generation_count))
    print(yellow+bold+"Best route ranking : "+standart+green+str(ranking[0][1]))
    print(yellow+bold+"Best Distance : "+standart+green+str(1/(ga_util.rankRoute(population[ranking[0][0]]))))
    print(standart+"----------------------------------------------")

def init()->None:
    loc_list=ga_util.initLocations(ga_util.getLocationCoordinates())
    population=ga_util.createPopulation(loc_list)
    ranking=ga_util.rankPopulation(population)
    printConstants()

    for i in range(0,generation_count):
        mating_pool=ga_util.createMatingPool(population,ranking)
        offsprings=ga_util.breedMatingPool(mating_pool)
        mutated_offsprings=ga_util.mutateOffsprings(offsprings)
        population,ranking=ga_util.insertToPopulation(population,ranking,mutated_offsprings)
        printInfo(i,population,ranking) if(i%print_best_ranking_rate==0) else None

    final_route=list(loc.location_no for loc in population[ranking[0][0]])

    print(red+"\n\n[+]DONE")
    print(red+"END RESULTS : \n")
    print(f"{bold}{yellow}Total generation count : {red}{generation_count}")
    print(f"{bold}{yellow}Best ranking : {red}{str(ranking[0][1])}")
    print(f"{bold}{yellow}Best distance : {red}{str(1/(ga_util.rankRoute(population[ranking[0][0]])))}")
    print(f"{bold}{yellow}Route : {standart}")
    print(final_route[0],end="")
    for loc in final_route[1:]:
        print(f"{green} -> {standart}",end="")
        print(loc,end="")
    print()
    
init()

