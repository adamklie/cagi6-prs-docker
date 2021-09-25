#cd /app/

# Main pipeline for taking individual level genotypes in plink bfile format and outputting predictions
echo -e 'Running CAGI6-PRS Docker Script\n'

### Step 1 - Generate IDs and phenotype file
python3 make-pheno-for-loader.py --fam ./data/test/MGB_10_all/MGB_10_all.fam --out ./data/test/MGB_10_all/MGB_10_all
echo -e "\n"

### Step 2 - Generate raw files for for MGB for each disease
./plink --bfile ./data/test/MGB_10_all/MGB_10_all --extract ./data/test/MGB_10_all/bca.age.old.extract.txt --export A --out ./data/test/MGB_10_all/MGB_10_all.bca
./plink --bfile ./data/test/MGB_10_all/MGB_10_all --extract ./data/test/MGB_10_all/cad.age.old.extract.txt --export A --out ./data/test/MGB_10_all/MGB_10_all.cad
./plink --bfile ./data/test/MGB_10_all/MGB_10_all --extract ./data/test/MGB_10_all/ibd.age.old.extract.txt --export A --out ./data/test/MGB_10_all/MGB_10_all.ibd
./plink --bfile ./data/test/MGB_10_all/MGB_10_all --extract ./data/test/MGB_10_all/t2d.age.old.extract.txt --export A --out ./data/test/MGB_10_all/MGB_10_all.t2d
echo -e "\n"

### Step 3 - Generate z-scored feather files
python3 make-feather-for-loader.py --raw ./data/test/MGB_10_all/MGB_10_all.bca.raw --summary ./data/test/MGB_10_all/bca.age.old.summary.tsv --out ./data/test/MGB_10_all/MGB_10_all.bca
python3 make-feather-for-loader.py --raw ./data/test/MGB_10_all/MGB_10_all.cad.raw --summary ./data/test/MGB_10_all/cad.age.old.summary.tsv --out ./data/test/MGB_10_all/MGB_10_all.cad
python3 make-feather-for-loader.py --raw ./data/test/MGB_10_all/MGB_10_all.ibd.raw --summary ./data/test/MGB_10_all/ibd.age.old.summary.tsv --out ./data/test/MGB_10_all/MGB_10_all.ibd
python3 make-feather-for-loader.py --raw ./data/test/MGB_10_all/MGB_10_all.t2d.raw --summary ./data/test/MGB_10_all/t2d.age.old.summary.tsv --out ./data/test/MGB_10_all/MGB_10_all.t2d
echo -e "\n"

### Step 4 - Dataload and make predictions
python3 ReleaseYourCAGIdFury.py --model_path ./data/test/MGB_10_all/Optuna_Study_Trial_11_Epoch_38.pt --config_path ./data/test/MGB_10_all/BCA_5e-4_Old_Test.yaml --out_path ./output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path ./data/test/MGB_10_all/Optuna_Study_Trial_45_Epoch_24.pt --config_path ./data/test/MGB_10_all/CAD_5e-4_Old_Test.yaml --out_path ./output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path ./data/test/MGB_10_all/Optuna_Study_Trial_20_Epoch_49.pt --config_path ./data/test/MGB_10_all/IBD_5e-4_Old_Test.yaml --out_path ./output/test/MGB_10_all/
python3 ReleaseYourCAGIdFury.py --model_path ./data/test/MGB_10_all/Optuna_Study_Trial_15_Epoch_21.pt --config_path ./data/test/MGB_10_all/T2D_5e-4_Old_Test.yaml --out_path ./output/test/MGB_10_all/
python PENGUINS.py --inter_milan ./output/test/MGB_10_all/ --out_path ./output/test/MGB_10_all/

echo -e 'Script completed'