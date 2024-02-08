#!/bin/bash

for config in traffic 
do
    reload="True"
    for i in 1 2 3
    do
        python main.py --map=Town02 --map_config=$config --scene=$i --reload=$reload --pc=aisyslab 
        echo "scene: $i - map_config: $config"
    done
done
