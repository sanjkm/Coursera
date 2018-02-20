# Gets the application job ID in the first command
# Feeds this parameter into python program that outputs
# the requested numbers
%%bash
yarn application -list -appStates FINISHED | tail -1 | cut -f1
