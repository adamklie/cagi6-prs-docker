import sys 
import os
import pandas as pd
import pyarrow.feather as feather

import torch
from torch.utils import data
import numpy as np
from itertools import islice

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


class SNPDataset(data.Dataset):
    """Characterizes a dataset for PyTorch."""

    def __init__(self, id_file, geno_file, pheno_file, zscore=True, disease_col='PROSTATE_CANCER'):
        """Initialization.
        Args:
            ids_file
            geno_file 
            pheno_file
            zscore
            disease_col
        """
        
        # Get individual ids from list
        self.list_ids = pd.read_csv(id_file, header=None, dtype=str)[0].tolist()
        
        # Get individual phenotype information in form of dataframe
        pheno = pd.read_csv(pheno_file, sep='\t', dtype={"IID": str})
        
        # Pull disease diagnosis from this dataframe
        self.phenotypes = dict(zip(pheno["IID"], pheno[disease_col]))
        
        # Pull ethnicity information from this dataframe
        self.ethnic = dict(zip(pheno["IID"], pheno['ETH']))
        
        # Pull family history information from this dataframe
        self.fh = dict(zip(pheno["IID"], pheno['FH']))
        
        # Get genotype from hdf5
        if "intersection" in geno_file:
            self.geno = feather.read_feather(geno_file).set_index('1')
        else:
            self.geno = feather.read_feather(geno_file).set_index('0')
              
    def __len__(self):
        return len(self.list_ids)
   
    def __getitem__(self, index):
        """Returns one data pair (genotypes and label)."""
        
        ID = self.list_ids[index]
        
        # Load SNP data
        genotype = self.geno[ID].values
        X = torch.from_numpy(genotype).float()
        
        # Load cancer diagnosis
        cancer = torch.from_numpy(np.array([self.phenotypes[ID]]))
        
        # One hot encode the ethnic values
        categories = [x for x in set([x for x in self.ethnic.values()])]
        labelencoder = LabelEncoder()
        enc = OneHotEncoder(handle_unknown='ignore')
        mp_ethnic = dict(zip(categories, enc.fit_transform(labelencoder.fit_transform(categories).reshape(-1,1)).toarray()))
        z = torch.from_numpy(mp_ethnic[self.ethnic[ID]])
        anc = torch.Tensor([torch.argmax(z)])
        
        fh = torch.from_numpy(np.array([self.fh[ID]]))
        
        return X, cancer, anc, fh


def get_loader(ids_file, genotype_file, phenotype_file, disease_column, batch_size, shuffle, num_workers):
    """Returns torch.utils.data.DataLoader for geno dataset."""
    geno_dataset = SNPDataset(geno_file=genotype_file,id_file=ids_file, pheno_file=phenotype_file, disease_col=disease_column)
    params = {'batch_size': batch_size, 'shuffle': shuffle,'num_workers': num_workers}
    data_loader = torch.utils.data.DataLoader(dataset=geno_dataset, **params)
    return data_loader