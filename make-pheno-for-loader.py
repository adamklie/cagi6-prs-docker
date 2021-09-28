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
    
    # Step 1: Load fam file
    print("Loading fam file from {}...".format(args.out))
    fam = pd.read_csv(args.fam, delim_whitespace=True, header=None)
    
    # Step 2: Load covariates file
    print("Loading the covariates file from {}...".format(args.covar))
    covar = pd.read_csv(args.covar, delim_whitespace=True)
    
    # Step 3: Load means and stds
    print("Loading age summary file file from {}...".format(args.summary))
    summary = pd.read_csv(args.summary, sep="\t", index_col=0)
    
    # Step 4: Z-score age
    print("Z-scoring age")
    mean = summary.loc[args.phenotype]["MEAN"]
    std = summary.loc[args.phenotype]["STD"]
    print("\tMean age:", mean)
    print("\tStd age:", std)
    zage = (covar["AGE"]-mean)/std
    
    # Step 5: Format
    print("Formatting tsv and ids.txt files...")
    fam.columns = ["FID", "IID", "PAT", "MAT", "SEX", "PHENOTYPE"]
    fam["AGE"] = covar["AGE"]
    fam["Z_AGE"] = zage
    fam["FH"] = -9
    fam["ETH"] = "EUR"
    ids = fam["IID"].values
    
    #Step 6: Save new data
    print("Saving tsv and ids.txt file to {}...".format(args.out))
    fam.to_csv("{}.{}.tsv".format(args.out, args.phenotype.lower()), sep="\t", index=False)
    np.savetxt("{}.ids.txt".format(args.out), ids, fmt="%s")
    
    print("-"*len("Phenotype Loading"))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fam", type=str, help="Input .fam file")
    parser.add_argument("--covar", type=str, help="Input .covariates.txt file")
    parser.add_argument("--summary", type=str, help="Input .summary.tsv file")
    parser.add_argument("--phenotype", type=str, help="{BCA, CAD, IBD, T2D}")
    parser.add_argument("--out", type=str, default='./test', help="Output prefix for .tsv and .ids.txt files")
    args = parser.parse_args()
    main(args) 