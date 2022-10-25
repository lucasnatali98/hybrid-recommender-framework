#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
CONT_01=${2}
CONT_02=${3}
R1=${4}
R2=${5}

echo ""

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

# no momento da execução as pastas eram para análise dos modelos com risco
mkdir -p ${DATASET}/RISK
mv ${DATASET}/MO ${DATASET}/RISK
mv ${DATASET}/SO ${DATASET}/RISK
mv ${DATASET}/Predictions ${DATASET}/RISK
mv ${DATASET}/Results ${DATASET}/RISK
cp -R ${DATASET}/MF/Predictions ${DATASET}
rm -r ${DATASET}/Predictions/R1

for R in $(seq ${R1} ${R2}); do
    for FOLD in "${array_folds[@]}"; do
        cp ${DATASET}/constituent/${FOLD}/${CONT_01}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/constituent/${FOLD}/${CONT_02}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    done
done
