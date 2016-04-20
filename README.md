# Nationals Scoring Model

Program that inputs individual's results per track event, models an outdoor meet to simulate the NIRCA National Track and Field Championship, and output meet and event results with averages and standard deviations. 

The program works as follows:

1. Input indoor and outdoor results from the season to-date.

2. Convert all times to float representations.

3. Convert indoor events to outdoor events using standard coaching conversions.

4. Score meet based purely on input, without model

5. Score meet with model, running each event 10000 times, changing each person's time randomly per iteration.

6. Output results

7. Run cleanup
