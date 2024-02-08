#!/bin/bash

for config in layers_none
do
    reload="True"
    for i in 1 2 3 4 5
    do
        python main.py --map=Town03 --map_config=$config --scene=$i --reload=$reload --pc=home 
        echo "scene: $i - map_config: $config"
    done
done
