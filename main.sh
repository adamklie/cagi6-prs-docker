cd /app/

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
