#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
MO_01=${2}
DM_MO_01=${3}
DM_RISK_MO_01=${4}
MO_02=${5}
DM_MO_02=${6}
DM_RISK_MO_02=${7}
SO_01=${8}
SO_02=${9}
R1=${10}
R2=${11}

echo ""

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

mkdir -p ${DATASET}/PREF-6h
mv ${DATASET}/MO ${DATASET}/PREF-6h
mv ${DATASET}/SO ${DATASET}/PREF-6h
cp -r ${DATASET}/Predictions ${DATASET}/PREF-6h

# apaguei os arquivos do eval de risk, farei a transferência de tudo...
for R in $(seq ${R1} ${R2}); do
    for FOLD in "${array_folds[@]}"; do
        # RANK-6h
        mkdir -p ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RISK-6h/Predictions/hybrid/R${R}/${FOLD}/*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        # RISK-6h
        cp ${DATASET}/RISK-6h/Predictions/R${R}/${FOLD}/RISK_MO*${MO_01}*E-false_S-false*${DM_RISK_MO_01}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RISK-6h/Predictions/R${R}/${FOLD}/RISK_MO*${MO_02}*E-false_S-false*${DM_RISK_MO_02}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RISK-6h/Predictions/R${R}/${FOLD}/RISK_SO*${SO_01}*E-false*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RISK-6h/Predictions/R${R}/${FOLD}/RISK_SO*${SO_02}*E-false*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    done
done
