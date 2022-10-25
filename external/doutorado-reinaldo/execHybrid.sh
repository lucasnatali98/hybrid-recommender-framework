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
if [ ! -z ${7} ]; then
    R1=${6}
    R2=${7}
else
    R1=1
    R2=1
fi

echo ""

RunFolder="run/hybrid"
OutFolder="${DATASET}/out/hybrid/"
mkdir -p ${OutFolder}

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="scikitTuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="scikitTunedConfigs"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<PREFIX>:1_N${NUM_RUN}_scikitTuning.:g" -e "s:<OUT_FOLD>:${OutFolder}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="scikitTunedPrediction"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        sed -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:F1234-5:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        sed -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:F1235-4:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        sed -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:F1245-3:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        sed -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:F1345-2:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        sed -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:F2345-1:g" -e "s:<R>:R${R}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
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
