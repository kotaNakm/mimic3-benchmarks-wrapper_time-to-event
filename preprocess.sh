#!/bin/sh

cd mimic3-benchmarks

python -m mimic3benchmark.scripts.extract_subjects ../raw_data/mimic3-full-1.4/  data/root/

python -m mimic3benchmark.scripts.validate_events data/root/

python -m mimic3benchmark.scripts.extract_episodes_from_subjects data/root/

python -m mimic3benchmark.scripts.split_train_and_test data/root/

python -m mimic3benchmark.scripts.create_in_hospital_mortality data/root/ data/in-hospital-mortality/

python -m mimic3benchmark.scripts.create_phenotyping data/root/ data/phenotyping/

mkdir ../preprocessed

mkdir ../preprocessed/data

mkdir ../preprocessed/meta_data

# sequential data and meta_data from phenotyping
cp data/phenotyping/train/*series.csv ../preprocessed/data

cp data/phenotyping/test/*series.csv ../preprocessed/data

cp data/phenotyping/train/listfile.csv ../preprocessed/meta_data/pheno_train.csv

cp data/phenotyping/test/listfile.csv ../preprocessed/meta_data/pheno_test.csv

# meta_data from motality
cp data/in-hospital-mortality/train/listfile.csv ../preprocessed/meta_data/mortal_train.csv

cp data/in-hospital-mortality/test/listfile.csv ../preprocessed/meta_data/mortal_test.csv

mkdir Acute Chronic Mixed