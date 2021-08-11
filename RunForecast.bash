#!/bin/bash
counter=0
while true; do

echo the counter is $counter
#################################################
######## First Download the bnd condition for the Local wave model, Set up the bnd and run the model
if [ $counter -eq 0 ]
then
./Run_FijiWave-Forecast
else
./Run_FijiWave-Forecast_1
fi


# Process Wave model output into Graphs and maps
cd ./out/
./proc_swanout
cd ..

#initiate the ploting and wl_forecast but don t wait
./Run_plots_1 &
./Run_RBF
let "counter = counter +1"
#Wait for a while
sleep 300
done