#!/usr/bin/env bash

NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Inicio: Executing metafeatures"

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

echo ""

RunFolder="run/metafeatures"
OutFolder="${DATASET}/out/metafeatures/"
mkdir -p ${OutFolder}

NUMFIELDS=1
STARTINGFIELD=2
FIELDS="<field>1<\/field>"
CONTENTBASEDF="items-content.txt"

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="cf-computation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_XML_FILE=${DATASET}_${ExecFile}.${NUM_RUN}
    TEMP_FILE=${TEMP_XML_FILE}.temp.exec
    rm -f ${TEMP_XML_FILE}
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<DATASET>:${DATASET}:g" -e "s:<CONTENTBASEDF>:${CONTENTBASEDF}:g" -e "s:<NUMFIELDS>:${NUMFIELDS}:g" -e "s:<STARTINGFIELD>:${STARTINGFIELD}:g" -e "s:<CORES>:0:g" -e "s:<TEMP_XML_FILE>:${TEMP_XML_FILE}:g" ${RunFolder}/cf_create_xml.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} 23 > ${OutFolder}${SEQ}_A_${ExecFile}.${NUM_RUN}.SH.out
    sed -e "s:<TEMP_XML_FILE>:${TEMP_XML_FILE}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}:g" ${RunFolder}/MetricsCalculator.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} 1 > ${OutFolder}${SEQ}_B_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_XML_FILE}.*.temp.xml
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="item-content-index"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.xml
    rm -f ${TEMP_FILE}
    sed -e "s:HOME:${DATASET}:g" -e "s:DFILE:ratingsNorm.txt:g" -e "s:RFILE:ratingsNorm.txt:g" -e "s:OUTPUTFOLDER::g" -e "s:CONTENTBASEDF:${CONTENTBASEDF}:g" -e "s:NUMFIELDS:${NUMFIELDS}:g" -e "s:STARTINGFIELD:${STARTINGFIELD}:g" ${RunFolder}/config_empty_index.xml > ${TEMP_FILE}
    java -Xmx100G -jar run/MetricsCalculator.jar ${TEMP_FILE} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
    mv ${DATASET}/BD/index ${DATASET}/BD/index-directory
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="content-computation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.xml
    rm -f ${TEMP_FILE}
    sed -e "s:HOME:${DATASET}:g" -e "s:DFILE:ratingsNorm.txt:g" -e "s:RFILE:ratingsNorm.txt:g" -e "s:OUTPUTFOLDER::g" -e "s:FIELDS:${FIELDS}:g" ${RunFolder}/config_empty_cb.xml > ${TEMP_FILE}
    java -Xmx100G -jar run/MetricsCalculator.jar ${TEMP_FILE} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
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
