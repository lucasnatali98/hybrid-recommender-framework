#!/usr/bin/env bash

#Comecei mas não concluí....
# a intenção era fazer o complemento para análise fatorial completa sobre o risco.
#======
#Amazon
#======
#MO-Risk-FWLS-Sel-IndRisk
#MO-Risk-FWLS-Sel-IndSUM
#MO-Risk-FWLS-Sel-Risk
#MO-Risk-FWLS-Sel-SUM
#MO-Risk-HR-All-IndRisk
#MO-Risk-HR-All-IndSUM
#MO-Risk-HR-All-Risk
#MO-Risk-HR-All-SUM
#SO-Risk-HR-All
#SO-Risk-STREAM-All
#
#-- Executar:
#MO-FWLS-All
#MO-HR-Sel
#SO-HR-Sel
#SO-STREAM-Sel
#
#============
#Bookcrossing
#============
#MO-Risk-HR-Sel-IndRisk
#MO-Risk-HR-Sel-IndSUM
#MO-Risk-HR-Sel-Risk
#MO-Risk-HR-Sel-SUM
#MO-Risk-STREAM-All-IndRisk
#MO-Risk-STREAM-All-IndSUM
#MO-Risk-STREAM-All-Risk
#MO-Risk-STREAM-All-SUM
#SO-Risk-FWLS-All
#SO-Risk-HR-All
#
#-- Executar:
#MO-STREAM-Sel
#MO-HR-All
#SO-HR-Sel
#SO-FWLS-Sel
#
#======
#Jester
#======
#MO-Risk-HR-All-IndRisk
#MO-Risk-HR-All-IndSUM
#MO-Risk-HR-All-Risk
#MO-Risk-HR-All-SUM
#MO-Risk-STREAM-Sel-IndRisk
#MO-Risk-STREAM-Sel-IndSUM
#MO-Risk-STREAM-Sel-Risk
#MO-Risk-STREAM-Sel-SUM
#SO-Risk-FWLS-All
#SO-Risk-HR-All
#
#-- Executar:
#MO-STREAM-All
#MO-HR-Sel
#SO-HR-Sel
#SO-FWLS-Sel
#
#=====
#ML20M
#=====
#MO-Risk-HR-Sel-IndRisk
#MO-Risk-HR-Sel-IndSUM
#MO-Risk-HR-Sel-Risk
#MO-Risk-HR-Sel-SUM
#MO-Risk-STREAM-Sel-IndRisk
#MO-Risk-STREAM-Sel-IndSUM
#MO-Risk-STREAM-Sel-Risk
#MO-Risk-STREAM-Sel-SUM
#SO-Risk-FWLS-All
#SO-Risk-HR-Sel
#
#-- Executar:
#MO-STREAM-All
#MO-HR-All
#SO-HR-All
#SO-FWLS-Sel


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
CORES_EVAL=${7}
CORES_MAIN=${8}
RELEVANT=${9}
R1=${10}
R2=${11}
if [ ! -z ${12} ]; then
    ALPHA=${12}
else
    ALPHA=5
fi
echo ""

RunFolder="run/mo"
OutFolder="${DATASET}/out/mo/"
mkdir -p ${OutFolder}

TUNING_CONFIG_MO="01;0;0;0;0/02;1;0;0;0/03;0;0;1;0/04;1;0;1;0/05;0;1;0;0/06;1;1;0;0/07;0;1;1;0/08;1;1;1;0"
TUNING_CONFIG_SO="01;0;0/02;0;1/03;1;1/04;1;2"

if [ "${DATASET}" = "Amazon" ]; then
    array_MO=("HR-sel" "FWLS-all")
fi
...
array_hybrid=("HR" "STREAM" "FWLS")
array_features=("all" "sel")
array_bool=("true" "false")
array_conf=("0.05" "0.1")
array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuningMORisk"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for hybrid in "${array_hybrid[@]}"; do
        for feature in "${array_features[@]}"; do
            for ext in "${array_bool[@]}"; do
                sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${hybrid}-${feature}:g" -e "s:<EXTREME>:${ext}:g" -e "s:<STATISTICALTEST>:false:g" -e "s:<CONFIDENCE>:0:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
                for ic in "${array_conf[@]}"; do
                    sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${hybrid}-${feature}:g" -e "s:<EXTREME>:${ext}:g" -e "s:<STATISTICALTEST>:true:g" -e "s:<CONFIDENCE>:${ic}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
                done
            done
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='7'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuningSORisk"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for hybrid in "${array_hybrid[@]}"; do
        for feature in "${array_features[@]}"; do
            sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${hybrid}-${feature}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<SO_CONFIG>:${TUNING_CONFIG_SO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='8'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuningEvaluation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    echo "- tuningEvaluation: hypervolumeProcessing"
    python -u ${RunFolder}/hypervolumeProcessing.py ${RunFolder}/hv-1.3-src/hv ${DATASET}/MO/R0/ "" tuningEval_Hypervolume.csv >> ${OutFolder}${SEQ}_${ExecFile}_HypervolumeProcessing.${NUM_RUN}.out
    echo "- tuningEvaluation: processTunedWinners"
    python -u ${RunFolder}/processTunedWinners.py ${RunFolder}/ ${DATASET}/MO/R0/tuningEval_Hypervolume.csv ${TUNING_CONFIG_MO} ${DATASET}/SO/R0 ${TUNING_CONFIG_SO} search_Winners_${DATASET}.txt > ${OutFolder}${SEQ}_${ExecFile}_processTunedWinners.${NUM_RUN}.out
fi

#####
SEQ='9'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="searchWinners"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for FOLD in "${array_folds[@]}"; do
        #sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:10800000:g" -e "s:<TIME_SAVE>:720000:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/search_Winners_${DATASET}.txt >> ${TEMP_FILE}
        sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:21600000:g" -e "s:<TIME_SAVE>:900000:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/search_Winners_${DATASET}.txt >> ${TEMP_FILE}
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='10'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="decisionMaking"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    for FOLD in "${array_folds[@]}"; do
        for hybrid in "${array_hybrid[@]}"; do
            for feature in "${array_features[@]}"; do
                sed -e "s:<RUN>:${RunFolder}:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}Ind:g" ${RunFolder}/${ExecFile}Ind.txt >> ${TEMP_FILE}
            done
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='11'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="predictions"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${FOLD}.${ALPHA}.${R1}.${R2}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            PRED_FOLD="Predictions/R${R}/${FOLD}"
            mkdir -p "${DATASET}/${PRED_FOLD}"
            for hybrid in "${array_hybrid[@]}"; do
                for feature in "${array_features[@]}"; do
                    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<PRED_FOLD>:${PRED_FOLD}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}MO:g" ${RunFolder}/${ExecFile}MO.txt >> ${TEMP_FILE}
                    sed -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<PRED_FOLD>:${PRED_FOLD}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}SO:g" ${RunFolder}/${ExecFile}SO.txt >> ${TEMP_FILE}
                done
            done
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} >> ${OutFolder}${SEQ}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi




#####
SEQ='13'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuningRisk"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    array_strategy=()
    if [ "${DATASET}" = "Bookcrossing" ]; then
        #array_strategy=("HR-sel" "FWLS-all")
        array_strategy=("STREAM-all")
    elif [ "${DATASET}" = "Jester" ]; then
        #array_strategy=("HR-all")
        array_strategy=("STREAM-sel")
    elif [ "${DATASET}" = "ML20M" ]; then
        #array_strategy=("STREAM-sel")
        array_strategy=("HR-sel")
    fi
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<EXTREME>:false:g" -e "s:<STATISTICALTEST>:false:g" -e "s:<CONFIDENCE>:0:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_MO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningMO.txt >> ${TEMP_FILE}
        sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<EXTREME>:false:g" -e "s:<STATISTICALTEST>:false:g" -e "s:<CONFIDENCE>:0:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_MO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningMORisk.txt >> ${TEMP_FILE}
    done
    array_strategy=()
    if [ "${DATASET}" = "Bookcrossing" ]; then
        #array_strategy=("FWLS-all")
        array_strategy=("HR-all")
    elif [ "${DATASET}" = "Jester" ]; then
        #array_strategy=("HR-all")
        array_strategy=("FWLS-all")
    elif [ "${DATASET}" = "ML20M" ]; then
        #array_strategy=("FWLS-all")
        array_strategy=("HR-sel")
    fi
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<SO_CONFIG>:${TUNING_CONFIG_SO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_SO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningSORisk.txt >> ${TEMP_FILE}
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
