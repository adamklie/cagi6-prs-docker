# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:36:01 2021

@author: james

Inputs: 1) A trained pytorch model path 2) A config path for model instantiation 3) A boolean --age_only True is needed if only age is incorportated instead of both sex and age
4) An out path to a folder path where predictions will be written. 5) A disease header used in the column names (e.g., bca, T2D). If one is not provided lockhart attempts to pull 
one from the given config 

Docker Changes needed: 
1) Automate/change SNPLoader path to account for updated location of SNPLoader in Docker file
2) Automate/change the InSNPtion path? Can resolve this if this script is in the bin...
"""

import yaml 
import argparse 
import torch 
import os
import sys
import numpy as np
from torch.utils.data import DataLoader
#from DontGetSNPpyWithMe import * #The neural net
sys.path.append('/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/DeweyIsOutOfTheGAGI/bin') #path to optimizer, InSNPtion, etc...
from InSNPtionEverdeen import * #The neural net with Mish
import torch.optim as optim
#from optimizer import Lookahead
#from radam import RAdam
import torch.nn.functional as F
#from EarlyStop import * #Early Stopping object
#from dataloader4 import
#import matplotlib.pyplot as plt
#import seaborn as sns
from torch.autograd import Variable
#import joblib
#from collections import defaultdict
sys.path.append('/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/NeverArgueWithTheData') #path to the dataloader
from SNPAndClinicalLoader import * #replace with TestLoader if want the IDs and prediction? Or maybe can pull in an unshuffled manner from the files?
import pandas as pd


def load_config(path):
    """
    Load the configuration from Cosmo.yaml.
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)


'''
Inputs: 1) Pytorch model 2) Dataloader 3) Device (e.g., CUDA or cpu) 
        4) Boolean Variable -> Default True; If False includes only age
        information instead of both sex and age (example BCA)
        
Returns: None

This function generates a .tsv prediction file for a given model.
'''
def Persian(model, loader, pleaseBeGpu, allClinical = True):
    print("I'M JUST A GUY WITH A BOOMERANG. I DIDN'T ASK FOR ALL THIS FLYING AND MAGIC.")
    
    model.eval()
    predictedScores = list()
    #trueLabels = list()
    
    dtype = torch.FloatTensor
    
    if not allClinical: 
        #Want only Age here
        for i, (snpBatch, pcBatch, ethnBatch, fHBatch, sexBatch, ageBatch) in enumerate(loader):
            snpBatch = snpBatch.to(pleaseBeGpu)
            
            ageBatch = ageBatch.type(dtype) #Ensure correct type for concatenation
            ageBatch = ageBatch.to(pleaseBeGpu)

            output = model(snpBatch, ageBatch)

            #for el in pcBatch.numpy():
            #    trueLabels.append(el)

            for el in torch.sigmoid(output[0]).to('cpu').detach().numpy():
                predictedScores.append(el)
    
    else:
        for i, (snpBatch, pcBatch, ethnBatch, fHBatch, sexBatch, ageBatch) in enumerate(loader):
            snpBatch = snpBatch.to(pleaseBeGpu)
            
            #Inclusion of clinical factors: Ensure correct type for concatenation
            sexBatch = sexBatch.type(dtype) 
            ageBatch = ageBatch.type(dtype)

            #Concatenate clinical features 
            stackedOutput = torch.cat([sexBatch, ageBatch], dim = 1)
            stackedOutput = stackedOutput.to(pleaseBeGpu)    

            #Run it:
            output = model(snpBatch, stackedOutput)

            #for el in pcBatch.numpy():
            #    trueLabels.append(el)

            for el in torch.sigmoid(output[0]).to('cpu').detach().numpy():
                predictedScores.append(el)
    
    print("I KNEW IT WAS ONLY A MATTER OF TIME! APPA ATE MOMO!\n")
    
    return predictedScores

def DoTheThing(modelPath, config, fileOutputPath, ageOnly, condition):
    generalSpecs = config["General"]
    mtlParams = config["Multitask-FFN"]
    dataLoaderParams = config["Dataloader"]
    pleaseBeGpu = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    #Check if user provided a valid condition name 
    if condition == "":
        print("Hey moron you forgot to input a disease header... well your leaving it up to Gilderoy then. Brachiarm armendo.\n")
        condition = generalSpecs.get("singleModelName").split("_")[1].upper()
    
    #instantiate and load the trained model
    if ageOnly: 
        #Single feature need to pass an additional flag since default add-ons is 2
        shallWeBegin = DoubleDash([generalSpecs["batchSize"],mtlParams["inputDimension"]],mtlParams["numLayers"], mtlParams["layerWidths"], mtlParams["dropout"], mtlParams["multiTaskOutputs"], generalSpecs["activationFunction"], numberAddOns = 1)
        
    else:
        shallWeBegin = DoubleDash([generalSpecs["batchSize"],mtlParams["inputDimension"]],mtlParams["numLayers"], mtlParams["layerWidths"], mtlParams["dropout"], mtlParams["multiTaskOutputs"], generalSpecs["activationFunction"])
    
    shallWeBegin.load_state_dict(torch.load(modelPath, map_location=torch.device('cpu')))
    shallWeBegin.to(pleaseBeGpu)
    
    geno_file = dataLoaderParams.get("SNP_Path")
    if "intersection" in geno_file:
        genotypeFile = feather.read_feather(geno_file).set_index('1')
    else:
        genotypeFile = feather.read_feather(geno_file).set_index('0')
        
    #Go through the test set in order!!! Make sure unshuffled/ shuffle = False
    testLoader = get_loader(ids_file = dataLoaderParams.get("TestIDs"), genotype_file = genotypeFile, phenotype_file = dataLoaderParams.get("PhenotypeFile"), disease_column = dataLoaderParams.get("Disease"), batch_size=generalSpecs["batchSize"],shuffle=False,num_workers=generalSpecs.get("numWorkers"))
    
    #generate predictions; AUC
    print("\nStarting predicitons: \n")
    if ageOnly:
        whatAreMyScores = Persian(shallWeBegin, testLoader, pleaseBeGpu, allClinical = False)
    else:
        whatAreMyScores = Persian(shallWeBegin, testLoader, pleaseBeGpu)
    
    
    #write output to a test file
    testPredictions = pd.DataFrame([whatAreMyScores], index=[condition + "_Predictions"]).T
    namesBePowerfulThingsButYouMayKnowMeAsMaud = pd.read_csv(dataLoaderParams.get("TestIDs"), header = None) #Get labels and then index
    testSetIndexes = list(namesBePowerfulThingsButYouMayKnowMeAsMaud[0]) 
    
    if len(testSetIndexes) != testPredictions.shape[0]:
        print("PANIC! The Bear is on the loose!")
        print(len(testSetIndexes))
        print(testPredictions.shape[0])
        raise ValueError("Test set index length does not match the number of predictions. Exiting...")


    testPredictions.index = testSetIndexes
    testPredictions.to_csv(fileOutputPath, sep = "\t") #write file
    print("This is just like magic - there are now predictions.")
    return None


if __name__ == "__main__":
    #Add Path to Config - default path will be set to current directory with a config.yaml file
    print("\nProfessor we found the entrance to the chamber of secrets... are you going somewhere? \nWell, yes. Urgent call. Unavoidable. Got to go.\nWhat about my sister?\nWell... As to that, most unfortunate - no one regrets more than I.\nYou're the Defense Against the Dark Arts teacher. You can't go now.\nI must say, when I took the job, there was nothing in the description about...\nYou're running away? After all of your predictions?\nPredictions can be misleading.\nYou made them.\nMy dear boy, use your common sense. My predictions wouldn't have done half as well if people knew I released Dewey from his CAGI.\nYou're not making any sense at all mate... my peanut!\nAND HERE WE GO\n\n\n")
    
    parser = argparse.ArgumentParser()
    path_args = parser.add_argument_group("Input/output options:")
    path_args.add_argument("--model_path", type =str, help = "Path to the trained InSNPtion model")
    path_args.add_argument("--config_path", type=str, default="./config.yaml", help='Path to config .yaml file to instantiate the trained InSNPtion model')
    path_args.add_argument("--age_only", type = bool, default = False, help = "A boolean flag that shuts of sex inclusion in preinitialization. If model used age only instead of sex and age use this flag as --age_only True")
    path_args.add_argument("--out_path", type = str, default = "/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/DeweyIsOutOfTheGAGI/OtherStuff/temp_files", help = "Folder path where predictions will be written.")
    path_args.add_argument("--disease", type = str, default = "", help = "A name for the intermediate prediction file column (e.g. BCA or t2d) so clear what each prediction corresponds to come concatenation time")
    
    args = parser.parse_args()
    
    #Pull model specs from the config:
    config = load_config(args.config_path)
    
    basePath = args.out_path 
    if basePath[-1] != "/": #handle issues where user forgets to add a backslash in the path
        basePath += "/"
        
    nameNames = args.config_path.split("/")[-1].split(".")[0]
    #Load the model, dataloader, and generate prediction file and AUC
    if args.age_only:
        print("Model loaded in uses a single clinical factor. Accounting for this here. \n")
    
    condition = args.disease
    aucward = DoTheThing(modelPath = args.model_path, config = config, fileOutputPath = basePath + nameNames + ".tsv", ageOnly = args.age_only, condition = condition.upper()) 
    