#!/usr/bin/env bash

NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Inicio: Executing Dataset"

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
FOLDS=${6}
CUTOFF=${7}
if [ ! -z ${8} ]; then
    NUM_USERS=${8}
else
    NUM_USERS=15000
fi

if [ "${DATASET}" == "Amazon" ]; then
    CONTENTBASEDF="books-meta.txt"
    FACTOR=5
    RELEVANT=0.8
elif [ "${DATASET}" == "Bookcrossing" ]; then
    CONTENTBASEDF="books-content.txt"
    FACTOR=10
    RELEVANT=0.7
elif [ "${DATASET}" == "Jester" ]; then
    CONTENTBASEDF="jokes_content.txt"
    FACTOR=21
    RELEVANT=0.57
elif [ "${DATASET}" == "ML20M" ]; then
    CONTENTBASEDF="movies-meta.txt"
    FACTOR=5
    RELEVANT=0.8
fi

echo ""

RunFolder="run/dataset"
OutFolder="${DATASET}/out/dataset/"
mkdir -p ${OutFolder}

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="normalizeRatings"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FACTOR>:${FACTOR}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="dataSelection"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLDS>:${FOLDS}:g" -e "s:<CUTOFF>:${CUTOFF}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="sampleSelection"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<NUM_USERS>:${NUM_USERS}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='4'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="mergeContent"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    python -u run/dataset/mergeContent.py ${DATASET} ${CONTENTBASEDF} "items-content.txt" > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}-PY.out
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="buildUserProfiles"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<CONTENT>:${CONTENTBASEDF}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<OUT>:${OutFolder}${SEQ}_N${NUM_RUN}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
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
