#!/bin/bash

input_reports_dir="./data/input/"
output_reports_dir="./data/output/"

hf_token="$1"
hf_repo_id="$2"
json_path="$3"

if [ ! -d $input_reports_dir ]; then
	echo "Input directory not found."
	exit 1
fi

if [ ! -d $output_reports_dir ]; then
	echo "Output directory not found."
	exit 1
fi

# python3 -m src.main_normalize
#
# echo "Dados devidamente normalizados!"

python3 -m src.main_json $json_path

echo "Json produzido!"

python3 -m src.main_dataset $hf_token $hf_repo_id $json_path

echo "Upload do dataset feito!"

exit 0
