# -*- coding: utf-8 -*-
"""
Created on Thu Sept 22 23:41:15 2021

@author: james

Inputs: 1) An input file directory of all intermediate CAGI prediction files 2) An output path where concatenated file will be written 
Outputs: A concatenated .tsv file containing all predictions for all IDs

Usage: python PENGUINS.py --inter_milan --out_path

"""

import argparse 
import os
import pandas as pd

if __name__ == "__main__":
    #Add Path to Config - default path will be set to current directory with a config.yaml file
    parser = argparse.ArgumentParser()
    path_args = parser.add_argument_group("Input/output options:")
    path_args.add_argument("--inter_milan", type = str, default = "/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/DeweyIsOutOfTheGAGI/OtherStuff/temp_files", help = "Path to intermediate prediction files for all conditions")
    path_args.add_argument("--out_path", type = str, default = "/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/DeweyIsOutOfTheGAGI/OtherStuff/CastTheKnucklebonesAngela", help = "Folder path where final prediction file will be written.")
    args = parser.parse_args()
    
    #handle issues where user forgets to add a backslash in the path
    tempFilePath = args.inter_milan
    if tempFilePath[-1] != "/": 
        tempFilePath += "/"
        
    byeSpaceSword = args.out_path
    if byeSpaceSword[-1] != "/":
        byeSpaceSword += "/"
    
    penguins = os.listdir(tempFilePath)
    #print(sorted(penguins))
    
    print("Concatenating files ... in the meantime maybe go penguin sledding?!?")

    blizzard = pd.DataFrame() #empty DF which predictions will get concatenated with 
    
    for ice in sorted(penguins):
        if ice.split(".")[-1] != "tsv":
            continue
        print(ice)
        lapras = pd.read_csv(tempFilePath + ice, sep = "\t", index_col = 0)
        lapras = lapras.applymap(lambda x: x[1:-1]) #remove the annoying [] around each prediction probability
        lapras = lapras.astype(float) #convert to float from string
        blizzard = pd.concat([blizzard, lapras], axis = 1)
        
    blizzard.to_csv(byeSpaceSword + "Predictions.tsv", sep = "\t")
    
    print("Everything changed the day the fire nation attacked - but hey at least you have a prediction file generated by Empoleon!")