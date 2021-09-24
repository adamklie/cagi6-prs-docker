# Adam Klie, Meghana Pagadala, James Talwar InSNPtion project
# 07/07/2021

# PyTorch dataloader for a SNPDataset amenable to multi-task learning. A SNP dataset consists of three aspects: 
# Genotypic data that should come in the feather format with the first column being SNP IDs
# Phenotypic data that should come in the tsv format with the first column being sample IDs
# (optional) SNP mapping or metadata files that should also be in the tsv format with the first column being SNP IDs


# Import necessary packages
import pandas as pd
import numpy as np
import pyarrow.feather as feather

import torch
from torch.utils import data

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


# Define the dataset class
class SNPDataset(torch.utils.data.Dataset):
    """Characterizes a dataset for PyTorch."""

    def __init__(self, id_file, geno_file, pheno_file, zscore=True, disease_col='PROSTATE_CANCER'):
        """Initialization of SNPDataset class.
        Args:
            id_file: List of ids that will be pulled from the genotype file
            geno_file: Feather file with the genotypes (z-scored or raw) that are inputs to model 
            pheno_file: Tab-separated file with phenotype information
            zscore: boolean indicating whether the genotypes have been z-scored
            disease_col: The column of the metadata file that contains the phenotype of interest
        """
        
        # Get individual ids from list
        self.list_ids = pd.read_csv(id_file, header=None, dtype=str)[0].tolist()
        
        # Get individual phenotype information in form of dataframe
        pheno = pd.read_csv(pheno_file, sep='\t', dtype={'IID': str})
        
        # Pull disease diagnosis from this dataframe
        if set(pheno[disease_col]) != {0,1}:
            newPheno = pheno[disease_col] - min(pheno[disease_col])
            if set(newPheno) == {0,1}:
                self.phenotypes = dict(zip(pheno['IID'].astype(str), newPheno))
            else:
                raise ValueError("STATUS Values are not 0/1 and cannot be corrected by substraction of max to this representation. Fix phenotype representation.")                         
        else:
            self.phenotypes = dict(zip(pheno['IID'].astype(str), pheno[disease_col]))

        # Pull ethnicity information from this dataframe
        self.ethnic = dict(zip(pheno['IID'], pheno['ETH']))
        
        # Pull family history information from this dataframe
        self.fh = dict(zip(pheno['IID'], pheno['FH']))
        
        # Get genotype from feather; pulled in NeuralNet script and passed here for memory efficiency 
        self.geno = geno_file
              
    def __len__(self):
        """Returns the number of samples in the dataset.
        """
        return len(self.list_ids)
   
    def __getitem__(self, index):
        """Returns one sample of inputs and labels.
        Args:
            index: an index from 0 to len(dataset)-1
        """
        
        # Get the id from list
        ID = self.list_ids[index]
        
        # Load SNP data and format
        genotype = self.geno[ID].values
        X = torch.from_numpy(genotype).float()
        
        # Load phenotype labels (NEED TO MAKE MORE GENERAL)
        cancer = torch.from_numpy(np.array([self.phenotypes[ID]]))
        
        # One hot encode the ethnicity values (NEED TO MAKE MORE GENERAL FOR ANY CATEGORICAL VARIABLE)
        categories = [x for x in set([x for x in self.ethnic.values()])]
        labelencoder = LabelEncoder()
        enc = OneHotEncoder(handle_unknown='ignore')
        mp_ethnic = dict(zip(categories, enc.fit_transform(labelencoder.fit_transform(categories).reshape(-1,1)).toarray()))
        z = torch.from_numpy(mp_ethnic[self.ethnic[ID]])
        anc = torch.Tensor([torch.argmax(z)])
        
        # Load FH (NEED TO MAKE MORE GENERAL FOR ANY BINARY)
        fh = torch.from_numpy(np.array([self.fh[ID]]))
        
        # Return these as a tuple (GENERALIZE)
        return X, cancer, anc, fh


def get_loader(ids_file, genotype_file, phenotype_file, disease_column, batch_size, shuffle, num_workers):
    """Returns torch.utils.data.DataLoader for SNPDataset.
    Args:
            ids_file: List of ids that will be pulled from the genotype file
            genotype_file: Feather file with the genotypes (z-scored or raw) that are inputs to model 
            phenotype_file: Tab-separated file with phenotype information
            disease_column: The column of the metadata file that contains the phenotype of interest
            batch_size: Int that defines the batch-size
            shuffle: Boolean defining whether to shuffle the samples
            num_workers: Int defnining the number of parallel workers used for dataloading
    """
    geno_dataset = SNPDataset(id_file=ids_file,
                              geno_file=genotype_file,
                              pheno_file=phenotype_file, 
                              disease_col=disease_column)
    params = {'batch_size': batch_size, 'shuffle': shuffle,'num_workers': num_workers}
    data_loader = torch.utils.data.DataLoader(dataset=geno_dataset, **params)
    return data_loader
