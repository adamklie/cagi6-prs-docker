cd /app/

echo 'CAGI6-PRS Docker Script'

# Main pipeline for taking individual level gentypes in plink bfile format and outputting predictions

### Step 1 - Generate raw files for for MGB ###

# Usage: 
# $path_to_plink --bfile $path_to_bfiles --export A --out  MGB

# Test
#./plink --bfile data/test/MGB_100_1000/MGB_100_1000 --export A --out data/test/MGB_100_1000/MGB_100_1000
./plink --bfile data/test/MGB_10_all/MGB_10_all --extract data/test/MGB_10_all/ibd.age.old.extract.txt --export A --out data/test/MGB_10_all/MGB_10_all

# Actual
# ./plink --bfile data/val/MGB--export A --out data/val/MGB

###

### Step 2 - Generate z-scored feather files for each pheno ###

# Usage:
# python3 make-feather.py --raw $path_to_raw --stats $path_to_snp_statistics (maybe make this a mapping that can correct for things)

# Test
#python3 make-feather-for-loader.py --raw data/test/MGB_100_1000.raw --stats data/test/MGB_100_1000.stats.tsv --out data/test/MGB_100_1000\
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_all

# Actual
# python3 make-feather-for-loader.py --raw data/val/MGB.raw --stats data/val/bca.stats.tsv --out data/val/bca
# python3 make-feather-for-loader.py --raw data/val/MGB.raw --stats data/val/cad.stats.tsv --out data/val/cad
# python3 make-feather-for-loader.py --raw data/val/MGB.raw --stats data/val/ibd.stats.tsv --out data/val/ibd
# python3 make-feather-for-loader.py --raw data/val/MGB.raw --stats data/val/t2d.stats.tsv --out data/val/t2d

###

### Step 3 - Generate IDs and phenotype file  ###

# Usage:
# python3 make-pheno-for-loader.py --fam $path_to_fam --out

# Test:
#python3 make-pheno-for-loader.py --fam data/test/MGB_100_1000.fam --out data/test/MGB_100_1000
python3 make-pheno-for-loader.py --fam data/test/MGB_10_all/MGB_10_all.fam --out data/test/MGB_10_all/MGB_10_all

# Actual
# python3 make-pheno-for-loader.py --fam data/val/MGB.fam

###

### Step 4 - Dataload and make predictions using InSNPtion models ###

# Usage
# python3 --geno data/test --pheno data/val/MGB.fam --ids $path_to_ids

# Test
#python3 YoureNotVeryBrightAreYou.py --config_path data/test/MGB_100_1000.yaml --out_path output/test
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test

# Actual
# python3 ReleaseYourCAGIdFury.py --model_path PATH_TO_TRAINED_MODEL --config_path PATH_TO_CONFIG_THAT_MATCHES_TRAINED_MODEL_SPECS --out_path FOLDER_WHERE_WANT_THE_PREDICTIONS_WRITTENx4

###