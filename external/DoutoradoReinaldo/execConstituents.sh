#!/usr/bin/env bash

NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Inicio: Executing constituents"

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
CORES_INTERNO=${6}

echo ""

if [ "${DATASET}" == "Amazon" ]; then
    RELEVANT=0.8
elif [ "${DATASET}" == "Bookcrossing" ]; then
    RELEVANT=0.7
elif [ "${DATASET}" == "Jester" ]; then
    RELEVANT=0.57
elif [ "${DATASET}" == "ML20M" ]; then
    RELEVANT=0.8
fi

RunFolder="run/constituent"
OutFolder="${DATASET}/out/constituent/"
mkdir -p ${OutFolder}

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="lensKitTuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST1>:4:g" -e "s:<TEST2>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-45_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST1>:3:g" -e "s:<TEST2>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-35_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST1>:3:g" -e "s:<TEST2>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-34_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST1>:2:g" -e "s:<TEST2>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-25_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST1>:2:g" -e "s:<TEST2>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-24_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST1>:2:g" -e "s:<TEST2>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-23_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST1>:1:g" -e "s:<TEST2>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-15_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST1>:1:g" -e "s:<TEST2>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-14_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST1>:1:g" -e "s:<TEST2>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-13_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST1>:1:g" -e "s:<TEST2>:2:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-12_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="myMediaLiteTuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="contentBased"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_PROPERTIES=${DATASET}_${ExecFile}.${NUM_RUN}.temp.properties
    rm -f ${TEMP_PROPERTIES}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TEMP_PROPERTIES>:${TEMP_PROPERTIES}:g" -e "s:<RELEVANT>:${RELEVANT}:g" ${RunFolder}/properties.CB > ${TEMP_PROPERTIES}
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    OUT_PATH=${OutFolder}${SEQ}_${ExecFile}_${NUM_RUN}
    # criando indices de items
    java -Xmx50G -jar ${RunFolder}/CBRecommender.jar ${TEMP_PROPERTIES} false F123-4  > ${OUT_PATH}-F123-4.out
    sed -e "s:indexItem=true:indexItem=false:g" -e "s:indexUser=false:indexUser=true:g" -e "s:<BD>:${DATASET}:g" -e "s:<TEMP_PROPERTIES>:${TEMP_PROPERTIES}:g" -e "s:<RELEVANT>:${RELEVANT}:g" ${RunFolder}/properties.CB > ${TEMP_PROPERTIES}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<PROP_FILE>:${TEMP_PROPERTIES}:g" -e "s:<OUT>:${OUT_PATH}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_PROPERTIES}
    rm -f ${TEMP_FILE}
fi

#####
SEQ='4'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="cbprTuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="ncfPreprocessing"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g"  -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345_:g"  ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1234:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_1234_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1235:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_1235_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1245:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_1245_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1345:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_1345_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:2345:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_2345_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='6'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="ncfTuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:123:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_123-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:124:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_124-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:125:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_125-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:134:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_134-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:135:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_135-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:145:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_145-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:234:g" -e "s:<TEST>:5:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_234-5_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:235:g" -e "s:<TEST>:4:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_235-4_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:245:g" -e "s:<TEST>:3:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_245-3_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:1:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-1_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    sed -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:345:g" -e "s:<TEST>:2:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_345-2_:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='7'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="selectTuned"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp
    rm -f ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt > ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='8'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="lensKit"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} Tuned"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    python -u run/constituent/prepareTuned.py ${DATASET} winners-${DATASET}.txt ${ExecFile}-${DATASET}.txt ${ExecFile} > ${OutFolder}${SEQ}_prepareTuned.${NUM_RUN}.SH.out
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1234:g" -e "s:<TEST>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1235:g" -e "s:<TEST>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1245:g" -e "s:<TEST>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1345:g" -e "s:<TEST>:2:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:2345:g" -e "s:<TEST>:1:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='9'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="myMediaLite"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} Tuned"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    python -u run/constituent/prepareTuned.py ${DATASET} winners-${DATASET}.txt ${ExecFile}-${DATASET}.txt ${ExecFile} > ${OutFolder}${SEQ}_prepareTuned.${NUM_RUN}.SH.out
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1234:g" -e "s:<TEST>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1235:g" -e "s:<TEST>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1245:g" -e "s:<TEST>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1345:g" -e "s:<TEST>:2:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:2345:g" -e "s:<TEST>:1:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='10'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="ncf"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} Tuned"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    python -u run/constituent/prepareTuned.py ${DATASET} winners-${DATASET}.txt ${ExecFile}-${DATASET}.txt ${ExecFile} > ${OutFolder}${SEQ}_prepareTuned.${NUM_RUN}.SH.out
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1234:g" -e "s:<TEST>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1235:g" -e "s:<TEST>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1245:g" -e "s:<TEST>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1345:g" -e "s:<TEST>:2:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:2345:g" -e "s:<TEST>:1:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='11'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="cbpr"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile} Tuned"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    python -u run/constituent/prepareTuned.py ${DATASET} winners-${DATASET}.txt ${ExecFile}-${DATASET}.txt ${ExecFile} > ${OutFolder}${SEQ}_prepareTuned.${NUM_RUN}.SH.out
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1234:g" -e "s:<TEST>:5:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1235:g" -e "s:<TEST>:4:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1245:g" -e "s:<TEST>:3:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:1345:g" -e "s:<TEST>:2:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<TRAIN>:2345:g" -e "s:<TEST>:1:g" -e "s:<CORES>:${CORES_INTERNO}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_:g" ${RunFolder}/${ExecFile}-${DATASET}.txt >> ${TEMP_FILE}
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
