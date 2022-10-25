#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
MO_01=${2}
DM_MO_01=${3}
MO_02=${4}
DM_MO_02=${5}
SO_01=${6}
SO_02=${7}
R1=${8}
R2=${9}

echo ""

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

# processando novas predições MO
# Tudo ficará na pasta MF, como está para Amazon (que rodou tudo de uma vez)
# PredictionsRANK foi criada temporariamente para guardar arquivos da execução de avaliação RANK
if [ -d "${DATASET}/PredictionsRANK" ]; then
    rsync -a ${DATASET}/MO/ ${DATASET}/MF/MO/
    rsync -a ${DATASET}/SO/ ${DATASET}/MF/SO/
    rsync -a ${DATASET}/Predictions/ ${DATASET}/MF/Predictions/
    # RISK-old contém arquivos executados para análises antigas que serão mantidos para não perder execuções
    rsync -a ${DATASET}/RISK-old/MO/ ${DATASET}/MF/MO/
    rsync -a ${DATASET}/RISK-old/SO/ ${DATASET}/MF/SO/
    rsync -a ${DATASET}/RISK-old/Predictions/ ${DATASET}/MF/Predictions/
    rm -r ${DATASET}/MO/
    rm -r ${DATASET}/SO/
    rm -r ${DATASET}/Predictions/
    mv ${DATASET}/PredictionsRANK ${DATASET}/Predictions/
fi

mkdir -p ${DATASET}/RANK
mv ${DATASET}/Predictions ${DATASET}/RANK
mv ${DATASET}/Results ${DATASET}/RANK

for R in $(seq ${R1} ${R2}); do
    for FOLD in "${array_folds[@]}"; do
        mkdir -p ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RANK/Predictions/hybrid/R${R}/${FOLD}/*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RANK/Predictions/R${R}/${FOLD}/MO*${MO_01}*${DM_MO_01}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RANK/Predictions/R${R}/${FOLD}/MO*${MO_02}*${DM_MO_02}.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RANK/Predictions/R${R}/${FOLD}/SO*${SO_01}*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        cp ${DATASET}/RANK/Predictions/R${R}/${FOLD}/SO*${SO_02}*.tsv.sorted ${DATASET}/Predictions/hybrid/R${R}/${FOLD}
        mkdir -p ${DATASET}/Predictions/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/R${R}/${FOLD}/RISK_MO*${MO_01}*E-false_S-false*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/R${R}/${FOLD}/RISK_MO*${MO_02}*E-false_S-false*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/R${R}/${FOLD}/RISK_SO*${SO_01}*E-false*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
        cp ${DATASET}/MF/Predictions/R${R}/${FOLD}/RISK_SO*${SO_02}*E-false*.tsv.sorted ${DATASET}/Predictions/R${R}/${FOLD}
    done
done
