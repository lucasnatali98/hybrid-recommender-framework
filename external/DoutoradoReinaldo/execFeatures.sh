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
if [ ! -z ${6} ]; then
    IGNORE_CB=${6}
else
    IGNORE_CB="False"
fi
echo ""

RunFolder="run/features"
OutFolder="${DATASET}/out/features/"
mkdir -p ${OutFolder}

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="extractStats"
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
    ExecFile="createFeatures"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<IGNORE_CB>:${IGNORE_CB}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="featureSelection"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:HR:g"     -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:STREAM:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:FWLS:g"   -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='4'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="createSelFeatures"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:HR:g"     -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:STREAM:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<STRATEGY>:FWLS:g"   -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="createTuningFeatures"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
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
