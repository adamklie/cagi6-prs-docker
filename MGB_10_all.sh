cd /app/

# Testing pipeline for taking individual level gentypes in plink bfile format and outputting predictions
echo -e 'Running CAGI6-PRS Docker Script on MGB_10_all\n'

### Step 0 - Run commands in data/test/MGB_10_all/MGB_10_all-make-bed.test to make data/test/MGB_10_all/MGB_10_all.bed

### Step 1 - Generate raw files for for MGB

# Usage: 
# $path_to_plink --bfile $path_to_bfiles --export A --out  MGB
./plink --bfile data/test/MGB_10_all/MGB_10_all --extract data/test/MGB_10_all/ibd.age.old.extract.txt --export A --out data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 2 - Generate z-scored feather files for data/test/MGB_10_all/MGB_10_all.raw

# Usage:
# python3 make-feather.py --raw $path_to_raw --stats $path_to_snp_statistics (maybe make this a mapping that can correct for things)
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 3 - Generate IDs and phenotype file

# Usage:
# python3 make-pheno-for-loader.py --fam $path_to_fam --out
python3 make-pheno-for-loader.py --fam data/test/MGB_10_all/MGB_10_all.fam --out data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 4 - Dataload and make predictions using InSNPtion models

# Usage
# python3 --geno data/test --pheno data/val/MGB.fam --ids $path_to_ids
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test/MGB_10_all/

echo -e 'Script completed'