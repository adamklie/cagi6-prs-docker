cd /app/

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