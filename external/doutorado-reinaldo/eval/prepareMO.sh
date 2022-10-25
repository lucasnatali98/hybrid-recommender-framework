#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
CONT_01=${2}
CONT_02=${3}
WHF_01=${4}
WHF_02=${5}
R1=${6}
R2=${7}

echo ""

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

mkdir -p ${DATASET}/WHF
mv ${DATASET}/Predictions ${DATASET}/WHF
mv ${DATASET}/Results ${DATASET}/WHF
cp -R ${DATASET}/MF/Predictions ${DATASET}
rm ${DATASET}/Predictions/R*/*/RISK_*
rm ${DATASET}/Predictions/R*/*/*-GeoRisk*
rm ${DATASET}/Predictions/R*/*/*_E-true*
rm ${DATASET}/Predictions/R*/*/*_S-true*

rm -r ${DATASET}/Predictions/hybrid
for R in $(seq ${R1} ${R2}); do
    for FOLD in "${array_folds[@]}"; do
        mkdir -p ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/constituent/${FOLD}/${CONT_01}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/constituent/${FOLD}/${CONT_02}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/hybrid/R${R}/${FOLD}/${WHF_01}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/hybrid/R${R}/${FOLD}/${WHF_02}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    done
done
