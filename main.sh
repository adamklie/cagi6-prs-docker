cd /app/

# Main pipeline for taking individual level genotypes in plink bfile format and outputting predictions
echo -e 'Running CAGI6-PRS Docker Script\n'

### Step 1 - Generate IDs and phenotype file for each disease
python3 make-pheno-for-loader.py --fam /input/MGB.fam --covar /input/MGB.covariates.txt --summary ref/age.summary.tsv --phenotype BCA --out /input/MGB
python3 make-pheno-for-loader.py --fam /input/MGB.fam --covar /input/MGB.covariates.txt --summary ref/age.summary.tsv --phenotype CAD --out /input/MGB
python3 make-pheno-for-loader.py --fam /input/MGB.fam --covar /input/MGB.covariates.txt --summary ref/age.summary.tsv --phenotype IBD --out /input/MGB
python3 make-pheno-for-loader.py --fam /input/MGB.fam --covar /input/MGB.covariates.txt --summary ref/age.summary.tsv --phenotype T2D --out /input/MGB
echo -e "\n"

### Step 2 - Generate raw files for for MGB for each disease
echo -e "Generating raw files\n------------"
./plink --bfile /input/MGB --extract ref/bca.extract.txt --export A --out /input/MGB.bca
./plink --bfile /input/MGB --extract ref/cad.extract.txt --export A --out /input/MGB.cad
./plink --bfile /input/MGB --extract ref/ibd.extract.txt --export A --out /input/MGB.ibd
./plink --bfile /input/MGB --extract ref/t2d.extract.txt --export A --out /input/MGB.t2d
echo -e "------------\n"

### Step 3 - Generate z-scored feather files
python3 make-feather-for-loader.py --raw /input/MGB.bca.raw --summary ref/bca.summary.tsv --out /input/MGB.bca
python3 make-feather-for-loader.py --raw /input/MGB.cad.raw --summary ref/cad.summary.tsv --out /input/MGB.cad
python3 make-feather-for-loader.py --raw /input/MGB.ibd.raw --summary ref/ibd.summary.tsv --out /input/MGB.ibd
python3 make-feather-for-loader.py --raw /input/MGB.t2d.raw --summary ref/t2d.summary.tsv --out /input/MGB.t2d
echo -e "\n"

### Step 4 - Dataload and make predictions
python3 GilderoyLockhart.py --age_only True --model_path models/bca.TheMonkeygoesBCAc.pt --config_path ref/bca.yaml --out_path /output/ --disease BCA
python3 GilderoyLockhart.py --model_path models/cad.ChuckAndDevon.pt --config_path ref/cad.yaml --out_path /output/ --disease CAD
python3 GilderoyLockhart.py --model_path models/ibd.pt --config_path ref/ibd.yaml --out_path /output/ --disease IBD
python3 GilderoyLockhart.py --model_path models/t2d.BillieEilishSaidItsNoT2Die.pt --config_path ref/t2d.yaml --out_path /output/ --disease T2D

python3 PENGUINS.py --inter_milan /output/ --out_path /output/

echo -e 'Script completed'
