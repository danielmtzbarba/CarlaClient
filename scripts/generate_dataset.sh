#!/bin/bash

#for config in layers_none layers_all traffic
for config in layers_all
do
    reload="True"
    for i in 1 2 3 4 5 6 7 8 9 10 11
    do
        python main.py --map=Town01 --map_config=$config --scene=$i --reload=$reload
        echo "scene: $i - map_config: $config"
    done
done
