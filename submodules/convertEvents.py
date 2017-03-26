from . import helpers
import time

def convertSingleEvent(results, conversionFunc):
  # Result object for converted results
  newResultObject = {}
  # For every result in uncnverted array
  for name, athleteResults in results.items():
    # Create entry for athlete
    newResultObject[name] = []

    # For every result the athlete has
    for result in athleteResults:
      # Copy the result for safety's sake
      newResult = result.copy()
      # Apply the conversion function to the result
      newResult['result'] = helpers.sixDecimalFloat(conversionFunc(newResult['result']))
      # Save the converted result
      newResultObject[name].append(newResult)

  # Return the converted results as an event object
  return newResultObject

def convertEvents(indoorResultsObject):
  convertStartTime = time.time()

  # Convert indoor events to outdoor equivalents
  indoorResultsObject['100m'] = convertSingleEvent(indoorResultsObject['60m'], lambda x: x*2 - 3.3)
  indoorResultsObject['100m HH'] = convertSingleEvent(indoorResultsObject['60m HH'], lambda x: x*2 - 2)
  indoorResultsObject['1500m'] = convertSingleEvent(indoorResultsObject['1 Mile'], lambda x: x * 0.9259)
  indoorResultsObject['5000m'] = convertSingleEvent(indoorResultsObject['3000m'], lambda x: x * ((5/3)**1.06))

  helpers.printDuration('Converted event times', convertStartTime, time.time())
