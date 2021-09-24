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
    
    #Step 1: Load raw and save intermediate data structures
    print("Loading raw file from {}...".format(args.raw))
    raw = pd.read_csv(args.raw, delim_whitespace=True)
    IIDs = raw["IID"]
    raw = raw.iloc[:, 6:].T
    raw.columns = IIDs
    raw.index.name = "0"
    snps = ["_".join(var.split("_")[:-1]) for var in raw.index]
    alleles = [var[-1] for var in raw.index]
    raw_summary = pd.DataFrame({"INDEX":raw.index, "MGB_ID":snps, "ACTUAL_ALLELE":alleles})
    
    #Step 2: Load summary file for SNPs
    print("Loading SNP summary file from {}...".format(args.summary))
    summary = pd.read_csv(args.summary, sep="\t")
    
    #Step 3: Combine these files
    print("Merging raw with SNP summary file...")
    merged_summary = pd.merge(raw_summary, summary, on="MGB_ID").set_index("INDEX")
    ordered_merged_summary = merged_summary.loc[raw.index]
    
    #Step 4: Correcting mismatched alleles, TODO: put number corrected
    print("Correcting mismatched alleles...")
    mismatched_pos = np.where(ordered_merged_summary["ACTUAL_ALLELE"] != ordered_merged_summary["EXPECTED_ALLELE"])[0]
    raw.iloc[mismatched_pos, :] = 2 - raw.iloc[mismatched_pos, :]
    
    #Step5 Z-score
    print("Z-scoring genotypes...")
    zraw = raw.subtract(ordered_merged_summary["MEAN"].values, axis="index")
    zraw = zraw.div(ordered_merged_summary["STD"].values, axis="index")
    
    #Step 6: Save new zscored feather
    print("Saving zscored feather file to {}.zscored.feather...".format(args.out))
    feather.write_feather(zraw.reset_index(), "{}.zscored.feather".format(args.out))
    print("-"*len("Making a feather file\n"))
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=str, help="Input raw file")
    parser.add_argument("--summary", type=str, help="Input SNP summary file containing IDs, effect alleles and training statistics")
    parser.add_argument("--out", type=str, default='./test', help="Output prefix for .zscored.feather file")
    args = parser.parse_args()
    main(args) 