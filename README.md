# Sliced_LLC_champsim
This is the final repository for CS422 course project

The champsim folder contains code for sliced LLC for a 2 core modulo hash function. THe main changes done are in config.sh file and adding l2c.cc and l2c.h files. The hash function can be changed by modifying the get_slice function of l2c.cc file. The number of cores and LLC sizes can be varied through the json file. Rest all steps remain same for running traces on champsim.
Some debug information is printed when we run ./config.sh champsim_config.json in champsim. Kindly ignore that.

THe graphs folder contains all the graphs present in the report.

postprocessing_scripts contain the scripts we are using to extract relevant information from the stats printed by champsim.

results_champsim_stats contain the original stats printed by champsim during the experiments. Note that some of them may not match the experimental setup mentioned in the report, since a large set of experiments were performed by differnt members of the groupand some of them were repeated.
