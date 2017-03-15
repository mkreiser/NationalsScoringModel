from . import helpers
import re, statistics, time

def calculateAthleteData(event, eventResults):
  analyzedEventResults = []
  dateWeights = helpers.getDateWeights()

  for name, results in eventResults.items():
    rawResults = []
    if (event in helpers.getRelayEvents()):
      athleteData = {
        'runningTimeSum': 0,
        'runningWeightSum': 0,
        'club': name
      }

    else:
      splitName, splitClub = re.split('[$]+', name)
      splitName = splitName.strip()
      splitClub = splitClub.strip()
      athleteData = {
        'runningTimeSum': 0,
        'runningWeightSum': 0,
        'name': splitName,
        'club': splitClub
      }

    for result in results:
      rawResults.append(result['result'])
      athleteData['runningTimeSum'] += result['result'] * dateWeights[result['date']]
      athleteData['runningWeightSum'] += dateWeights[result['date']]

    athleteData['mean'] = sum(rawResults) / len(rawResults)
    athleteData['median'] = statistics.median(rawResults)
    athleteData['calculatedTime'] = (athleteData['runningTimeSum'] / athleteData['runningWeightSum'])

    athleteData['prettyMean'] = helpers.twoDecimalFloat(athleteData['mean'])
    athleteData['prettyMedian'] = helpers.twoDecimalFloat(athleteData['median'])
    athleteData['prettyCalculatedTime'] = helpers.twoDecimalFloat(athleteData['calculatedTime'])

    analyzedEventResults.append(athleteData)

  return analyzedEventResults

def getAthleteData(resultsObject):
  getAthleteTime = time.time()

  athleteAnalyzedResults = {}
  for outdoorColumn in helpers.getOutdoorColumns():
    event = outdoorColumn['event']
    athleteAnalyzedResults[event] = calculateAthleteData(event, resultsObject[event])

  helpers.printDuration('Analyzed athletes', getAthleteTime, time.time())

  return athleteAnalyzedResults
