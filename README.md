# CAGI6-PRS CLAIM-InSNPtion Instructions
 
## 1. Pull the Docker image down for use
 
 ```bash
 docker pull docker.synapse.org/syn26247239/cagi6-prs-docker
 ```
 
## 2. Add the MGB files
Place the following files inside the `/input` directory

```bash
MGB.bim
MGB.fam
MGB.bed
MGB.covariates.txt
```

## 3. Run the Docker

 ```bash
 docker run --name cagi6-prs-docker-test8.1 -v $(pwd)/input/:/input/:rw -v $(pwd)/output/:/output/:rw cagi6-prs-docker:test8
 ```
 
## 4. Check the outputs
Outputs can be found in thef file `/output/CLAIM-InSNPtion_modelnumber_1.tsv`

This is a tab-separated file. The first column contain the **IIDs** for the individuals from the `/input/MGB.fam` file. Each subsequent column is the raw PRS scores output by are model for each of the 4 real phenotypes. The columns are labeled by the phenotypes **BCA, CAD, IBD, T2D**.