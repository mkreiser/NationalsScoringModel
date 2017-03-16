from . import helpers
import re, statistics, time

def calculateAthleteData(event, eventResults):
  # Create storage for analyzed results
  analyzedEventResults = []
  # Get the weighting used for analysis
  dateWeights = helpers.getDateWeights()

  # For every athlete and their results in the event
  for name, results in eventResults.items():
    rawResults = []

    # If it's a relay event, only use club name
    if (event in helpers.getRelayEvents()):
      athleteData = {
        'runningTimeSum': 0,
        'runningWeightSum': 0,
        'club': name
      }

    # If not, attach both name and club
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

    # For every result, sum the results with the weight applied and keep track of the weights applied
    for result in results:
      rawResults.append(result['result'])
      athleteData['runningTimeSum'] += result['result'] * dateWeights[result['date']]
      athleteData['runningWeightSum'] += dateWeights[result['date']]

    # Calculate mean, median, and weighted time for the athlete in this event
    athleteData['mean'] = sum(rawResults) / len(rawResults)
    athleteData['median'] = statistics.median(rawResults)
    athleteData['calculatedTime'] = (athleteData['runningTimeSum'] / athleteData['runningWeightSum'])

    # Attached rounded values for printing
    athleteData['prettyMean'] = helpers.twoDecimalFloat(athleteData['mean'])
    athleteData['prettyMedian'] = helpers.twoDecimalFloat(athleteData['median'])
    athleteData['prettyCalculatedTime'] = helpers.twoDecimalFloat(athleteData['calculatedTime'])

    # Add the analyzed result to the storage object
    analyzedEventResults.append(athleteData)

  # Return all of the analyzed results
  return analyzedEventResults

def getAthleteData(resultsObject):
  getAthleteTime = time.time()

  # Keep storage for every event
  athleteAnalyzedResults = {}
  # For every outdoor event
  for outdoorColumn in helpers.getOutdoorColumns():
    # Analyze the event using helper method
    event = outdoorColumn['event']
    athleteAnalyzedResults[event] = calculateAthleteData(event, resultsObject[event])

  helpers.printDuration('Analyzed athletes', getAthleteTime, time.time())

  # Return a results object with analyzed data
  return athleteAnalyzedResults
