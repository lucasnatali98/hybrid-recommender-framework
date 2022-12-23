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
OutFolder="${DATASET}/out/fairness/eval/"
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
            sed -e "s:Predictions/:Fairness/Predictions/:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<TOP_N>:0:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
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
            sed -e "s:Predictions/:Fairness/Predictions/:g" -e "s:Results/:Fairness/Results/:g" -e "s/1;2;3;4:alpha=5;5:alpha=5;6:alpha=5/1;2;3;4:alpha=5;5:alpha=5;6:alpha=5;13;14;15/g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:${TRAIN}:g" -e "s:<TEST>:${TEST}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<R>:R${R}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
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
    sed -e "s:/rankAlgorithms.py:/rankAlgorithmsFairness.py:g" -e "s:/Results:/Fairness/Results:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:All:g"            -e "s:<CONFIG>:0 0 0:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
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
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:Results:Fairness/Results:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}-${SAMPLE}-${ALPHA}-SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="rankAlgorithms"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} - Best - alpha ${ALPHA}"
    TEMP_FILE=${DATASET}_${R1}_${R2}_${ExecFile}.Best.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    if [ "${DATASET}" = "Amazon" ]; then
        BestAlgs="MO-Risk-HR-All-SUM;MO-Rank-FWLS-Sel-SUM;STREAM-All;Biased-MF;SO-Rank-STREAM-All;SO-Risk-HR-All"
    elif [ "${DATASET}" = "Bookcrossing" ]; then
        BestAlgs="MO-Risk-HR-All-IndSUM;SO-Risk-FWLS-All;MO-Rank-HR-Sel-SUM;SO-Rank-FWLS-All;FWLS-All;ALS"
    elif [ "${DATASET}" = "Jester" ]; then
        BestAlgs="HR-All;MO-Rank-HR-All-SUM;MO-Risk-HR-All-SUM;UserKNN;SO-Rank-HR-All;SO-Risk-HR-All"
    elif [ "${DATASET}" = "ML20M" ]; then
        BestAlgs="MO-Risk-HR-All-SUM;MO-Rank-STREAM-Sel-SUM;FWLS-All;ItemKNN;SO-Risk-FWLS-All;SO-Rank-FWLS-All"
    fi
    sed -e "s:/rankAlgorithms.py:/rankAlgorithmsFairness.py:g" -e "s:/Results:/Fairness/Results:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<TOP_N>:${TOP_N}:g" -e "s:<NAME>:Best:g"            -e "s:<CONFIG>:0 0 0 \"\" \"${BestAlgs}\":g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
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
