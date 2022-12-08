#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
MO_01=${2}
MO_02=${3}
SO_01=${4}
SO_02=${5}
NUM_RUN=${6}

echo ""

mv ${DATASET}/MO ${DATASET}/MO-bkp
mv ${DATASET}/SO ${DATASET}/SO-bkp

mkdir -p ${DATASET}/MO/R0
mkdir -p ${DATASET}/SO/R0

HOME="RISK-old"

cp ${DATASET}/${HOME}/MO/R0/MO_${MO_01}_E-false_S-false_* ${DATASET}/MO/R0/
cp ${DATASET}/${HOME}/MO/R0/MO_${MO_02}_E-false_S-false_* ${DATASET}/MO/R0/
cp ${DATASET}/${HOME}/SO/R0/SO_${SO_01}_E-false_* ${DATASET}/SO/R0/
cp ${DATASET}/${HOME}/SO/R0/SO_${SO_02}_E-false_* ${DATASET}/SO/R0/

./run/execMO.sh ${DATASET} 8 10 ${NUM_RUN} 4 30 1 5 0.8 1 1 5 > ${DATASET}/out/execMO-8-10.R-1-1.N${NUM_RUN}.out
./run/execMO.sh ${DATASET} 11 11 ${NUM_RUN} 20 0 0 0 0.8 1 1 5 > ${DATASET}/out/execMO-11-11.R-1-1.N${NUM_RUN}.out
./run/execEval.sh ${DATASET} 1 1 ${NUM_RUN} 20 0 0 0.8 0 1 1 5 > ${DATASET}/out/execEval-1-1.R-1-1.N${NUM_RUN}.out

# copiando híbridos
mkdir -p ${DATASET}/Predictions/hybrid
cp -r ${DATASET}/WHF/Predictions/hybrid/R1 ${DATASET}/Predictions/hybrid/
rm ${DATASET}/Predictions/hybrid/R1/*/FWLS*

# copiando MO e SO que já tinham rodado
array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)
R=1
for FOLD in "${array_folds[@]}"; do
    mkdir -p ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    cp ${DATASET}/WHF/Predictions/hybrid/R${R}/${FOLD}/ALS*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    cp ${DATASET}/WHF/Predictions/hybrid/R${R}/${FOLD}/Biased*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    cp ${DATASET}/WHF/Predictions/hybrid/R${R}/${FOLD}/HR*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    cp ${DATASET}/WHF/Predictions/hybrid/R${R}/${FOLD}/STREAM*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
    cp ${DATASET}/RANK-6h/Predictions/R${R}/${FOLD}/MO*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
    cp ${DATASET}/RANK-6h/Predictions/R${R}/${FOLD}/SO*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
done

./run/execEval.sh ${DATASET} 2 4 ${NUM_RUN} 5 20 4 0.8 5 1 1 5 > ${DATASET}/out/execEval-2-4.R-1-1.N${NUM_RUN}.out

mkdir -p ${DATASET}/RANK-6h-Anova
mv ${DATASET}/MO ${DATASET}/RANK-6h-Anova/
mv ${DATASET}/SO ${DATASET}/RANK-6h-Anova/
mv ${DATASET}/Predictions ${DATASET}/RANK-6h-Anova/
mv ${DATASET}/Results ${DATASET}/RANK-6h-Anova/
mv ${DATASET}/MO-bkp ${DATASET}/MO
mv ${DATASET}/SO-bkp ${DATASET}/SO
