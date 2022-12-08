#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}

echo ""

array_folds=(F2345-1 F1345-2 F1245-3 F1235-4 F1234-5)
for FOLD in "${array_folds[@]}"; do
    mv ${DATASET}/Fairness/MO/${FOLD}/R0 ${DATASET}/Fairness/MO/${FOLD}/R1
    mv ${DATASET}/Fairness/SO/${FOLD}/R0 ${DATASET}/Fairness/SO/${FOLD}/R1
done
