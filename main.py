#import genetic_algorithm as util
import json

constants_file = open("constants.json")
constants=json.load(constants_file)["main_constants"]
constants_file.close()