# -*- coding: utf-8 -*-

"""
Python script for...
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
from pyarrow import feather


# Tags
__author__ = "Adam Klie"
__data__ = "MM/DD/YYYY"


def main(args):
    
    print("Making a feather file\n" + "-"*len("Making a feather file"))
    
    #Step X: Load data
    print("Loading raw file from {}...".format(args.raw))
    raw = pd.read_csv(args.raw, delim_whitespace=True)
    IIDs = raw["IID"]
    raw = raw.iloc[:, 6:].T
    raw.columns = IIDs
    raw.index.name = "0"
    stats = pd.read_csv(args.stats, sep="\t")
    
    #Step X: Do stuff to data
    print("Z-scoring genotypes...")
    zraw = raw.subtract(stats["mean"].values, axis="index")
    zraw = zraw.div(stats["std"].values, axis="index")
    
    #Step X: Save new data
    print("Saving zscored feather file to {}.zscored.feather...".format(args.out))
    feather.write_feather(zraw.reset_index(), "{}.zscored.feather".format(args.out))
    print("-"*len("Making a feather file\n"))
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=str, help="Input raw file")
    parser.add_argument("--stats", type=str, help="Input SNP stats file")
    parser.add_argument("--out", type=str, default='./test', help="Output prefix for .zscored.feather file")
    args = parser.parse_args()
    main(args) 