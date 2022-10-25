#!/bin/bash

source ./venv/bin/activate
pip install --upgrade pip
pip freeze > requirements.txt
docker build -t mpacheco95/task_executor:1.0.0 .
docker push mpacheco95/task_executor:1.0.0
