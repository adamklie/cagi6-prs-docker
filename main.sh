cd /app/

<<<<<<< HEAD
# Main pipeline for taking individual level genotypes in plink bfile format and outputting predictions
echo -e 'Running CAGI6-PRS Docker Script\n'

### Step 1 - Generate raw files for for MGB
./plink --bfile data/test/MGB_10_all/MGB_10_all --extract data/test/MGB_10_all/ibd.age.old.extract.txt --export A --out data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 2 - Generate z-scored feather files
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_all
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_all
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_all
python3 make-feather-for-loader.py --raw data/test/MGB_10_all/MGB_10_all.raw --summary data/test/MGB_10_all/ibd.age.old.summary.tsv --out data/test/MGB_10_all/MGB_10_alls
echo -e "\n"

### Step 3 - Generate IDs and phenotype file
python3 make-pheno-for-loader.py --fam data/test/MGB_10_all/MGB_10_all.fam --out data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 4 - Dataload and make predictions
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path output/test/MGB_10_all/

echo -e 'Script completed'
=======
echo 'Testing Docker'

# Main pipeline for taking individual level genotypes in plink bfile format and outputting predictions

### Step 1 - Generate raw files for for MGB - Tell plink which is minor ###

# Usage:
# $path_to_plink --bfile $path_to_bfiles --export A --out  MGB

# Test
./plink --bfile data/sample/MGB_100_1000 --export A --out output/test/MGB_100_1000

# Actual
# ./plink --bfile data/val/MGB_100_1000 --export A --out data/val/MGB_100_1000

###

### Step 2 - Generate z-scored feather files for each pheno ###

# Usage:
# python3 make-feather.py --raw $path_to_raw --stats $path_to_snp_statistics (maybe make this a mapping that can correct for things)

# Test
python3 make-feather-for-loader.py --raw data/test/MGB_100_1000.raw --stats data/sample/MGB_100_1000.stats.tsv --out output/test/MGB_100_1000

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
python3 make-pheno-for-loader.py --fam data/sample/MGB_100_1000.fam --out output/test/MGB_100_1000

# Actual
# python3 make-pheno-for-loader.py --fam data/val/MGB.fam

###

### Step 4 - Dataload and make predictions using InSNPtion models ###

# Usage
# python3 --geno data/sample --config $path_to_config

# Test

# Actual
# python3 --geno data/val/bca --config $path_to_config
# python3 --geno data/val/cad --config $path_to_config
# python3 --geno data/val/ibd --config $path_to_config
# python3 --geno data/val/t2d --config $path_to_config

###
>>>>>>> aa16d27adc0b9f7d636580d97e8bd33fa0f414fa
