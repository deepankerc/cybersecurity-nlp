#!/bin/bash
RAW_FILES="$(ls raw/)"
for filename in $RAW_FILES; do
    echo $filename
    textract ./raw/"$filename" > ./text/"$filename".txt
done
