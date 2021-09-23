# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 13:36:01 2021

@author: james

Inputs: 1) A trained pytorch model path 2) a config path for model instantiation 3) An out-file path
Outputs: A TSV for an individual's probability of disease risk

Challenge time to do: 
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
from InSNPtion import * #The neural net with Mish
sys.path.append('/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/NeverArgueWithTheData') #path to the dataloader
from SNPLoader import * #replace with TestLoader if want the IDs and prediction? Or maybe can pull in an unshuffled manner from the files?
import pandas as pd

#import torch.optim as optim
#from optimizer import Lookahead
#from radam import RAdam
#import torch.nn.functional as F
#from EarlyStop import * #Early Stopping object
#from dataloader4 import *
#from PrepareForTrouble import * #for auc have to call Meowth then ROCkPaperScissors functions
#import matplotlib.pyplot as plt
#import seaborn as sns
#from torch.autograd import Variable
#import joblib
#from collections import defaultdict




def Meowth(model, loader, pleaseBeGpu):
    print("Team Rockets Rockets ---> Giovanni awaits \n")
    model.eval()
    predictedScores = list()
    #trueLabels = list()
    
    for i, (snpBatch, pcBatch, ethnBatch, fHBatch) in enumerate(loader):
        #print(*phenotypeBatch.tolist())
        snpBatch = snpBatch.to(pleaseBeGpu)
        #phenotypeBatch = phenotypeBatch.to(pleaseBeGpu)
        output = model(snpBatch)
        
        #for el in pcBatch.numpy():
        #    trueLabels.append(el)
        
        for el in torch.sigmoid(output[0]).to('cpu').detach().numpy():
            predictedScores.append(el)
     
    return predictedScores


def load_config(path):
    """
    Load the configuration from Cosmo.yaml.
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)


def DoTheThing(modelPath, config, fileOutputPath = "./TestSetPredictions"):
    generalSpecs = config["General"]
    mtlParams = config["Multitask-FFN"]
    dataLoaderParams = config["Dataloader"]
    pleaseBeGpu = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #print(pleaseBeGpu)
    
    #instantiate and load the trained model
    shallWeBegin = DiddyKongRacing([generalSpecs["batchSize"],mtlParams["inputDimension"]],mtlParams["numLayers"], mtlParams["layerWidths"], mtlParams["dropout"], mtlParams["multiTaskOutputs"], generalSpecs["activationFunction"])
    shallWeBegin.load_state_dict(torch.load(modelPath, map_location=pleaseBeGpu)) #, map_location=torch.device('cpu')))
    shallWeBegin.to(pleaseBeGpu)

    
    geno_file = dataLoaderParams.get("SNP_Path")
    if "intersection" in geno_file:
        genotypeFile = feather.read_feather(geno_file).set_index('1')
    else:
        genotypeFile = feather.read_feather(geno_file).set_index('0')
        
    testLoader = get_loader(ids_file = dataLoaderParams.get("TestIDs"), genotype_file = genotypeFile, phenotype_file = dataLoaderParams.get("PhenotypeFile"), disease_column = dataLoaderParams.get("Disease"), batch_size=generalSpecs["batchSize"],shuffle=False,num_workers=generalSpecs.get("numWorkers"))
    
    #generate predictions; AUC
    print("Starting predicitons: \n")
    whatAreMyScores = Meowth(shallWeBegin, testLoader, pleaseBeGpu)
    
    #auc = ROCkPaperScissors(whatAreMyScores, phenotypeLabels)
    
    #write output to a test file
    condition = generalSpecs.get("singleModelName").split("_")[1].upper()
    testPredictions = pd.DataFrame([whatAreMyScores], index=[condition + "_Predictions"]).T #generate predictions
    namesBePowerfulThingsButYouMayKnowMeAsMaud = pd.read_csv(dataLoaderParams.get("TestIDs"), header = None) #Get labels and then index
    testSetIndexes = list(namesBePowerfulThingsButYouMayKnowMeAsMaud[0]) 
    
    if len(testSetIndexes) != testPredictions.shape[0]:
        print("PANIC! The Bear is on the loose!")
        print(len(testSetIndexes))
        print(testPredictions.shape[0])
        raise ValueError("Test set index length does not match the number of predictions. Exiting...")
    #

    testPredictions.index = testSetIndexes
    testPredictions.to_csv(fileOutputPath, sep = "\t") #write file
    
    return None


if __name__ == "__main__":
    #Add Path to Config - default path will be set to current directory with a config.yaml file
    parser = argparse.ArgumentParser()
    path_args = parser.add_argument_group("Input/output options:")
    path_args.add_argument("--model_path", type = str, help = "Path to the trained InSNPtion model")
    path_args.add_argument('--config_path', type=str, default="./config.yaml", help='Path to config .yaml file to instantiate the trained InSNPtion model')
    path_args.add_argument("--out_path", type = str, default = "/cellar/users/jtalwar/projects/BetterRiskScores/InSNPtion/Galbatorix/DeweyIsOutOfTheGAGI/OtherStuff/temp_files", help = "Folder path where predictions will be written.")
    args = parser.parse_args()
    
    #Pull model specs from the config:
    config = load_config(args.config_path)
    
    basePath = args.out_path #Where the individual output .tsv file path is going
    if basePath[-1] != "/": #handle issues where user forgets to add a backslash in the path
        basePath += "/"
    nameNames = args.config_path.split("/")[-1].split(".")[0]
    #Load the model, dataloader, and generate a prediction file
    print("Generating predictions now - please stay on the line and numbers will be with you shortly... \n")
    DoTheThing(args.model_path, config, fileOutputPath = basePath + nameNames + ".tsv" ) 
    
    print("Congratulations ... there are now numbers. Have a pleasant day. Huzzah!")
