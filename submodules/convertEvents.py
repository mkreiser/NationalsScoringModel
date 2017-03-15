from . import helpers
import time

def convertSingleEvent(results, conversionFunc):
  newResultObject = {}
  for name, athleteResults in results.items():
    newResultObject[name] = []

    for result in athleteResults:
      newResult = result.copy()
      newResult['result'] = helpers.twoDecimalFloat(conversionFunc(newResult['result']))

      newResultObject[name].append(newResult)

  return newResultObject

def convertEvents(indoorResultsObject):
  convertStartTime = time.time()

  indoorResultsObject['100m'] = convertSingleEvent(indoorResultsObject['60m'], lambda x: x*2 - 3.3)
  indoorResultsObject['100m HH'] = convertSingleEvent(indoorResultsObject['60m HH'], lambda x: x*2 - 3.1)
  indoorResultsObject['1500m'] = convertSingleEvent(indoorResultsObject['1 Mile'], lambda x: x * 0.9259)
  indoorResultsObject['5000m'] = convertSingleEvent(indoorResultsObject['3000m'], lambda x: x * ((5/3)**1.06))

  helpers.printDuration('Converted event times', convertStartTime, time.time())
