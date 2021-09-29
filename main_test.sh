cd /app/

# Main pipeline for taking individual level genotypes in plink bfile format and outputting predictions
echo -e 'Running CAGI6-PRS Docker Script\n'

### Step 1 - Generate IDs and phenotype file for each disease
python3 make-pheno-for-loader.py --fam /input/test/MGB_10.fam --covar /input/test/MGB_10.covariates.txt --summary /input/test/age.summary.tsv --phenotype BCA --out /input/test/MGB_10
python3 make-pheno-for-loader.py --fam /input/test/MGB_10.fam --covar /input/test/MGB_10.covariates.txt --summary /input/test/age.summary.tsv --phenotype CAD --out /input/test/MGB_10
python3 make-pheno-for-loader.py --fam /input/test/MGB_10.fam --covar /input/test/MGB_10.covariates.txt --summary /input/test/age.summary.tsv --phenotype IBD --out /input/test/MGB_10
python3 make-pheno-for-loader.py --fam /input/test/MGB_10.fam --covar /input/test/MGB_10.covariates.txt --summary /input/test/age.summary.tsv --phenotype T2D --out /input/test/MGB_10
echo -e "\n"

### Step 2 - Generate raw files for for MGB for each disease
echo -e "Generating raw files\n------------"
./plink --bfile /input/test/MGB_10 --extract /input/test/bca.extract.txt --export A --out /input/test/MGB_10.bca
./plink --bfile /input/test/MGB_10 --extract /input/test/cad.extract.txt --export A --out /input/test/MGB_10.cad
./plink --bfile /input/test/MGB_10 --extract /input/test/ibd.extract.txt --export A --out /input/test/MGB_10.ibd
./plink --bfile /input/test/MGB_10 --extract /input/test/t2d.extract.txt --export A --out /input/test/MGB_10.t2d
echo -e "------------\n"

### Step 3 - Generate z-scored feather files
python3 make-feather-for-loader.py --raw /input/test/MGB_10.bca.raw --summary /input/test/bca.summary.tsv --out /input/test/MGB_10.bca
python3 make-feather-for-loader.py --raw /input/test/MGB_10.cad.raw --summary /input/test/cad.summary.tsv --out /input/test/MGB_10.cad
python3 make-feather-for-loader.py --raw /input/test/MGB_10.ibd.raw --summary /input/test/ibd.summary.tsv --out /input/test/MGB_10.ibd
python3 make-feather-for-loader.py --raw /input/test/MGB_10.t2d.raw --summary /input/test/t2d.summary.tsv --out /input/test/MGB_10.t2d
echo -e "\n"

### Step 4 - Dataload and make predictions
python3 GilderoyLockhart.py --age_only True --model_path /input/test/bca.TheMonkeygoesBCAc.pt --config_path /input/test/bca.test.yaml --out_path /output/test/ --disease BCA
python3 GilderoyLockhart.py --model_path /input/test/cad.ChuckAndDevon.pt --config_path /input/test/cad.yaml --out_path /output/test/ --disease CAD
python3 GilderoyLockhart.py --model_path /input/test/ibd.pt --config_path /input/test/ibd.yaml --out_path /output/test/ --disease IBD
python3 GilderoyLockhart.py --model_path /input/test/t2d.BillieEilishSaidItsNoT2Die.pt --config_path /input/test/t2d.yaml --out_path /output/test/ --disease T2D

python3 PENGUINS.py --inter_milan /output/test/ --out_path /output/test/

echo -e 'Script completed'
