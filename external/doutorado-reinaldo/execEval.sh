#!/usr/bin/env bash

NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Inicio: Executing features"

NOW=$(date +"%Y-%m-%d_%H.%M.%S")
START=$(date +%s)

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
#EXECUÇÃO INICIAL = ${2}
#EXECUÇÃO FINAL = ${3}
NUM_RUN=${4}
CORES=${5}
MEM=${6}
CORES_MAIN=${7}
RELEVANT=${8}
TOP_N=${9}
R1=${10}
R2=${11}
if [ ! -z ${12} ]; then
    ALPHA=${12}
else
    ALPHA=5
fi

echo ""

RunFolder="run/eval"
OutFolder="${DATASET}/out/eval/"
mkdir -p ${OutFolder}

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)
array_samples_train=(2345 1345 1245 1235 1234)
array_samples_test=(1 2 3 4 5)

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="sortPredictions"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<TOP_N>:0:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="evaluationMetricsCalculator"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for f in $(seq 0 $((${#array_folds[*]}-1))); do
            FOLD=${array_folds[f]}
            TRAIN=${array_samples_train[f]}
            TEST=${array_samples_test[f]}
            sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:${TRAIN}:g" -e "s:<TEST>:${TEST}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<R>:R${R}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="rankAlgorithms"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} - alpha ${ALPHA}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    #sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Metafeatured:g"     -e "s:<CONFIG>:1 1 1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    #sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:MetafeaturedRisk:g" -e "s:<CONFIG>:0 1 1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    #sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Risk:g"             -e "s:<CONFIG>:0 0 1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    #sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:IndED:g"            -e "s:<CONFIG>:0 0 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:All:g"            -e "s:<CONFIG>:0 0 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Pref-All:g"         -e "s:<CONFIG>:1 1 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${SAMPLE}-${ALPHA}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='4'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="createLossesWins"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} - alpha ${ALPHA}"
    if [ "${DATASET}" = "Amazon" ]; then
        baseline="HR-sel-*"
    elif [ "${DATASET}" = "Bookcrossing" ]; then
        baseline="HR-sel-*"
    elif [ "${DATASET}" = "Jester" ]; then
        baseline="HR-all-*"
    elif [ "${DATASET}" = "ML20M" ]; then
        baseline="FWLS-all-*"
    fi
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<BASELINE>:${baseline}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${SAMPLE}-${ALPHA}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="usersPreferencesPlots"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    python -u ${RunFolder}/usersPreferencesPlots.py ${1} Weights >${OutFolder}${ExecFile}.out
fi

#####
SEQ='6'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="distancesComputation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_samples_test[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='7'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="hypervolume"
    # rodar:
    # 1. calculo da metrica
    # 2. Estatísticas e plot
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}Processing_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}Processing.txt >> ${TEMP_FILE}
            sed -e "s:RANK-6h/MO:MF/MO:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}ProcessingALL_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}Processing.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    python -u ${RunFolder}/hypervolumePlots.py ${DATASET} Results/HV Results/HV hypervolume_${DATASET} > ${OutFolder}${SEQ}_${ExecFile}Plots_N${NUM_RUN}.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='8'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="hypervolume"
    # rodar:
    # 1. calculo da metrica
    # 2. Estatísticas e plot
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}-risk"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}Processing-Risk_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}Processing.txt >> ${TEMP_FILE}
            sed -e "s:RANK-6h/MO:RISK-6h/MO:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}ProcessingALL-Risk_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}Processing.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-Risk-${NUM_RUN}-SH.out
    python -u ${RunFolder}/hypervolumePlotsRisk.py ${DATASET} Results/HV Results/HV hypervolume_risk_${DATASET} > ${OutFolder}${SEQ}_${ExecFile}Plots_Risk_N${NUM_RUN}.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='9'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="generationalDistancesComputation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-Risk-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

# segmentação de usuários
# comparação com constituintes

#####
SEQ='11'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="sortPredictionsConst"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<TOP_N>:0:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='12'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="evaluationMetricsCalculatorConst"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for f in $(seq 0 $((${#array_folds[*]}-1))); do
            FOLD=${array_folds[f]}
            TRAIN=${array_samples_train[f]}
            TEST=${array_samples_test[f]}
            sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:${TRAIN}:g" -e "s:<TEST>:${TEST}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<R>:R${R}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='13'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="rankAlgorithmsConst"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} - alpha ${ALPHA}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Constituent:g"     -e "s:<CONFIG>:0 1 1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${SAMPLE}-${ALPHA}-SH.out
    rm -f ${TEMP_FILE}
fi

# Avaliação segmentada para PREF (Top e Bot)

#####
SEQ='21'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="prepareTopBotFiles"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for f in $(seq 0 $((${#array_folds[*]}-1))); do
        TRAIN=${array_samples_train[f]}
        TEST=${array_samples_test[f]}
        sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:${TRAIN}:g" -e "s:<TEST>:${TEST}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='22'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="evaluationMetricsCalculatorTopBot"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for f in $(seq 0 $((${#array_folds[*]}-1))); do
            FOLD=${array_folds[f]}
            TRAIN=${array_samples_train[f]}
            TEST=${array_samples_test[f]}
            sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:${TRAIN}:g" -e "s:<TEST>:${TEST}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<R>:R${R}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='23'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="distancesComputationTopBot"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_samples_test[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${NUM_RUN}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='24'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="rankAlgorithmsTopBot"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} - alpha ${ALPHA}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Seg:g"            -e "s:<CONFIG>:0 0 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed  -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Pref-Seg:g"       -e "s:<CONFIG>:1 1 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${SAMPLE}-${ALPHA}-SH.out
    rm -f ${TEMP_FILE}
fi

END=$(date +%s)
DIFF=$(($END - $START))
echo ""
echo ""
NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Fim: $DIFF seconds"
echo ""
echo ""
