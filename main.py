from typing import final
import genetic_algorithm as ga_util
import json
import os
from matplotlib import pyplot as plt, animation
import networkx as nx
import threading
import time

constants_file = open("constants.json")
constants=json.load(constants_file)["main_constants"]
constants_file.close()

#######
print_best_ranking_rate=constants["print_best_ranking_rate"]
generation_count=constants["generation_count"]
figure_size=constants["figure_size"]
drawing_rate=constants["drawing_rate"]
#######

plt.rcParams["figure.figsize"] = figure_size
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
G = nx.DiGraph()
best_route=[]
fixed_positions={}

class terminal_styles:
    PURPLE = '\033[ 95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    STANDART = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

purple=terminal_styles.PURPLE
bold=terminal_styles.BOLD
red=terminal_styles.RED
yellow=terminal_styles.YELLOW
standart=terminal_styles.STANDART
cyan=terminal_styles.CYAN
green=terminal_styles.GREEN
blue=terminal_styles.BLUE

def printConstants()->None:
    print(bold+red+"******** Genetic Algorithm Constants **********"+standart)
    ga_util.printConstants(bold,cyan,green)
    print(bold+red+"******** Main Application Constants ***********"+standart)
    print(bold+cyan+f"Generation Count : {green}{generation_count}"+standart)
    print(bold+cyan+f"Printing Rate : {green}{print_best_ranking_rate}"+standart)

def printInfo(generation_count:int,population:list,ranking:list)->None:
    os.system('printf \'\33c\e[3J\'')
    printConstants()
    print("----------------------------------------------")
    print(yellow+bold+"Generation : "+standart+green+str(generation_count))
    print(yellow+bold+"Best route ranking : "+standart+green+str(ranking[0][1]))
    print(yellow+bold+"Best Distance : "+standart+green+str(1/(ga_util.rankRoute(population[ranking[0][0]]))))
    print(standart+"----------------------------------------------")

    
def setBestRoute(chromosome:list):
    global best_route
    best_route=chromosome

def loop()->None:
    time.sleep(1)
    printConstants()
    global population
    global ranking
    for i in range(0,generation_count):
        mating_pool=ga_util.createMatingPool(population,ranking)
        offsprings=ga_util.breedMatingPool(mating_pool)
        mutated_offsprings=ga_util.mutateOffsprings(offsprings)
        population,ranking=ga_util.insertToPopulation(population,ranking,mutated_offsprings)
        setBestRoute(population[ranking[0][0]]) 
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
    print(f"{green} -> {standart}{final_route[0]}")


def animate(event)->list:
    global best_route
    global fixed_positions
    route_crd=list(x.location_no for x in best_route)
    fig.clear()
    G.clear()
    edges=[]
    edges_list=list((route_crd[x],route_crd[x+1]) for x in range(0,len(route_crd)-1))
    edges_list.extend([(route_crd[len(route_crd)-1],route_crd[0])])
    edges.extend(edges_list)
    G.add_edges_from(edges)
    fixed_nodes = fixed_positions.keys()
    color_map=[]
    for node in G:
        if node == best_route[0].location_no:
            color_map.append('red')
        else:
            color_map.append('blue')
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
    nx.draw_networkx(G,pos, with_labels=True,node_color=color_map,font_color="yellow")



loc_list=ga_util.initLocations(ga_util.getLocationCoordinates())
population=ga_util.createPopulation(loc_list)
ranking=ga_util.rankPopulation(population)
def init()->None:
    global fixed_positions
    global best_route
    best_route=population[ranking[0][0]]
    fixed_positions={x[0]:(x[1],x[2]) for x in ga_util.getLocationCoordinates()}
    loop_thread=threading.Thread(target=loop)
    loop_thread.start()
    ani = animation.FuncAnimation(fig, animate, frames=6, interval=drawing_rate,repeat=True)
    plt.show()
