# -*- coding: utf-8 -*-

"""
Python script for formatting input .fam file for SNBLoader
TODO: 
    1. 
    2. 
    3. 
"""

# Built-in/Generic Imports
import glob
import os
import argparse


# Libs
import pandas as pd
import numpy as np


# Tags
__author__ = "Adam Klie"
__data__ = "MM/DD/YYYY"


def main(args):
    
    print("Phenotype Loading\n" + "-"*len("Phenotype Loading"))
    
    #Step X: Load data
    print("Loading fam file from {}...".format(args.out))
    fam = pd.read_csv(args.fam, delim_whitespace=True, header=None)
    
    #Step X: Do stuff to data
    print("Formatting tsv and ids.txt files...")
    fam.columns = ["FID", "IID", "PAT", "MAT", "SEX", "PHENOTYPE"]
    fam["AGE"] = -9
    fam["FH"] = -9
    fam["ETH"] = "EUR"
    ids = fam["IID"].values
    
    #Step X: Save new data
    print("Saving tsv and ids.txt file to {}...".format(args.out))
    fam.to_csv("{}.tsv".format(args.out), sep="\t", index=False)
    np.savetxt("{}.ids.txt".format(args.out), ids, fmt="%s")
    
    print("-"*len("Phenotype Loading"))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fam", type=str, help="Input .fam file")
    parser.add_argument("--out", type=str, default='./test', help="Output prefix for .tsv and .ids.txt files")
    args = parser.parse_args()
    main(args) 