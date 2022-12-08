#!/usr/bin/env bash

#Rodando novas métricas fairness para o artigo SIGIR-2022
# Métodos:
# - Rank: todos HR, FWLS, STREAM - all e sel
# - Risk: selecionados os melhores para cada base
# -- MO:
# ---- Amazon:          FWLS-Sel   / HR-All
# ---- Bookcrossing:    STREAM-All / HR-Sel
# ---- Jester:          STREAM-Sel / HR-All
# ---- Movielens:       STREAM-Sel / HR-Sel
# -- SO:
# ---- Amazon:          FWLS-All / HR-Sel
# ---- Bookcrossing:    FWLS-All / HR-All
# ---- Jester:          FWLS-All / HR-All
# ---- Movielens:       FWLS-All / HR-Sel

# ESCOLHA: Rodar HR e FWLS All que estiverem faltando e copiar os executados.


NOW=$(date +"%D %T")
echo "***** $NOW"
echo "Inicio: Executing Fairness"

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
OutFolder="${DATASET}/out/fairness/"
mkdir -p ${OutFolder}

TUNING_CONFIG_MO="01;0;0;0;0/02;1;0;0;0/03;0;0;1;0/04;1;0;1;0/05;0;1;0;0/06;1;1;0;0/07;0;1;1;0/08;1;1;1;0"
TUNING_CONFIG_SO="01;0;0/02;0;1/03;1;1/04;1;2"

array_hybrid=("HR" "FWLS")
array_features=("all" "sel")
array_bool=("true" "false")
array_conf=("0.05" "0.1")
array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)

#####
SEQ='1'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuning"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    #MO
    array_strategy=()
    if [ "${DATASET}" = "Amazon" ]; then
        array_strategy=("FWLS-all")
    elif [ "${DATASET}" = "Bookcrossing" ]; then
        array_strategy=("FWLS-all" "HR-all")
    elif [ "${DATASET}" = "Jester" ]; then
        array_strategy=("FWLS-all")
    elif [ "${DATASET}" = "ML20M" ]; then
        array_strategy=("FWLS-all" "HR-all")
    fi
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:MO/:Fairness/MO/:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<EXTREME>:false:g" -e "s:<STATISTICALTEST>:false:g" -e "s:<CONFIDENCE>:0:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_MO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningMORisk.txt >> ${TEMP_FILE}
    done
    #SO
    array_strategy=()
    if [ "${DATASET}" = "Amazon" ]; then
        array_strategy=("HR-all") #ERRO: Deveria ser FWLS-all
    elif [ "${DATASET}" = "Bookcrossing" ]; then
        array_strategy=()
    elif [ "${DATASET}" = "Jester" ]; then
        array_strategy=()
    elif [ "${DATASET}" = "ML20M" ]; then
        array_strategy=("HR-all")
    fi
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:SO/:Fairness/SO/:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<SO_CONFIG>:${TUNING_CONFIG_SO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_SO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningSORisk.txt >> ${TEMP_FILE}
    done
    # FAIR
    array_strategy=("FWLS-all" "HR-all")
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:MO/:Fairness/MO/:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<EXTREME>:false:g" -e "s:<STATISTICALTEST>:false:g" -e "s:<CONFIDENCE>:0:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<MO_CONFIG>:${TUNING_CONFIG_MO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_MO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningMOFair.txt >> ${TEMP_FILE}
    done
    for strategy in "${array_strategy[@]}"; do
        sed -e "s:SO/:Fairness/SO/:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:tuning:g" -e "s:<STRATEGY>:${strategy}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:5400000:g" -e "s:<TIME_SAVE>:0:g" -e "s:<SO_CONFIG>:${TUNING_CONFIG_SO}:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_SO_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/tuningSOFair.txt >> ${TEMP_FILE}
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='2'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="tuningEvaluation"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    echo "- tuningEvaluation: hypervolumeProcessing"
    python -u ${RunFolder}/hypervolumeProcessing.py ${RunFolder}/hv-1.3-src/hv ${DATASET}/Fairness/MO/R0/ "" tuningEval_Hypervolume.csv >> ${OutFolder}${SEQ}_${ExecFile}_HypervolumeProcessing.${NUM_RUN}.out
    echo "- tuningEvaluation: processTunedWinners"
    python -u ${RunFolder}/processTunedWinners.py ${RunFolder}/ ${DATASET}/Fairness/MO/R0/tuningEval_Hypervolume.csv ${TUNING_CONFIG_MO} ${DATASET}/Fairness/SO/R0 ${TUNING_CONFIG_SO} search_Winners_fairness_${DATASET}.txt > ${OutFolder}${SEQ}_${ExecFile}_processTunedWinners.${NUM_RUN}.out
fi

#####
SEQ='3'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="searchWinners"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for FOLD in "${array_folds[@]}"; do
        sed -e "s:MO/:Fairness/MO/:g" -e "s:SO/:Fairness/SO/:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<TIME_LIMIT>:21600000:g" -e "s:<TIME_SAVE>:900000:g" -e "s:<CORES_EVAL>:${CORES_EVAL}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}_N${NUM_RUN}:g" ${RunFolder}/search_Winners_fairness_${DATASET}.txt >> ${TEMP_FILE}
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='4'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="decisionMaking"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            sed -e "s:MO/:Fairness/MO/:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}:g" ${RunFolder}/${ExecFile}.txt >> ${TEMP_FILE}
        done
    done
    for FOLD in "${array_folds[@]}"; do
        for hybrid in "${array_hybrid[@]}"; do
            for feature in "${array_features[@]}"; do
                sed -e "s:MO/:Fairness/MO/:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<MEM>:${MEM}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<R1>:${R1}:g" -e "s:<R2>:${R2}:g" -e "s:<ALPHA>:${ALPHA}:g" -e "s:<RELEVANT>:${RELEVANT}:g" -e "s:<CORES_MAIN>:${CORES_MAIN}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}Ind:g" ${RunFolder}/${ExecFile}Ind.txt >> ${TEMP_FILE}
            done
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} > ${OutFolder}${SEQ}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='5'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="predictions"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    TEMP_FILE=${DATASET}_${ExecFile}.${FOLD}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.temp.exec
    rm -f ${TEMP_FILE}
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            PRED_FOLD="Fairness/Predictions/R${R}/${FOLD}"
            mkdir -p "${DATASET}/${PRED_FOLD}"
            for hybrid in "${array_hybrid[@]}"; do
                for feature in "${array_features[@]}"; do
                    sed -e "s:MO/:Fairness/MO/:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<PRED_FOLD>:${PRED_FOLD}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}MO:g" ${RunFolder}/${ExecFile}MO.txt >> ${TEMP_FILE}
                    sed -e "s:SO/:Fairness/SO/:g" -e "s:<RUN>:${RunFolder}:g" -e "s:<BD>:${DATASET}:g" -e "s:<FOLD>:${FOLD}:g" -e "s:<R>:R${R}:g" -e "s:<hybrid>:${hybrid}:g" -e "s:<feature>:${feature}:g" -e "s:<PRED_FOLD>:${PRED_FOLD}:g" -e "s:<OUT>:${OutFolder}${SEQ}_${ExecFile}SO:g" ${RunFolder}/${ExecFile}SO.txt >> ${TEMP_FILE}
                done
            done
        done
    done
    python -u run/executeCommands.py ${TEMP_FILE} ${CORES} >> ${OutFolder}${SEQ}_${ExecFile}.${ALPHA}.${R1}.${R2}.${NUM_RUN}.SH.out
    rm -f ${TEMP_FILE}
fi

#####
SEQ='6'
if [ "${2}" -le "${SEQ}" ] && [ "${SEQ}" -le "${3}" ]; then
    ExecFile="copying previous predictions"
    echo ""
    echo "*****************************************************************"
    echo "${SEQ} - ${ExecFile}"
    for R in $(seq ${R1} ${R2}); do
        for FOLD in "${array_folds[@]}"; do
            rm -r -f ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}
            mkdir -p ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}
            cp ${DATASET}/RISK-6h/Predictions/hybrid/R${R}/${FOLD}/*.tsv.sorted ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}
            cp ${DATASET}/RISK-6h/Predictions/R${R}/${FOLD}/*.tsv.sorted        ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}
            rm ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}/RISK_*-sel_*
            if [ "${DATASET}" = "Amazon" ]; then #ERRO apontado na seq 1
                rm ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}/RISK_SO_HR-all*
            else
                rm ${DATASET}/Fairness/Predictions/hybrid/R${R}/${FOLD}/RISK_*_STREAM-*
            fi
        done
    done
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
