#!/bin/bash
jobs &>/dev/null
python server.py  &
new_job_started="$(jobs -n)"
if [ -n "$new_job_started" ];then
    VAR=$!
else
    VAR=
fi

echo $VAR

jobs &>/dev/null
python game.py  &
new_job_started="$(jobs -n)"
if [ -n "$new_job_started" ];then
    VAR=$!
else
    VAR=
fi

echo $VAR