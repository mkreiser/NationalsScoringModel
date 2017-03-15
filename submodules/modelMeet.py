from . import helpers, textOut
from operator import itemgetter
import copy, random, re, statistics, time

def modelMeet(resultList, filename, runs):
  modelMeetTime = time.time()
  textOutput = open(filename, 'w')

  meetAverageScore = {}
  meetModelScore = {}
  numberOfRunsSimmed = 0

  for outdoorColumn in helpers.getOutdoorColumns():
    eventName = outdoorColumn['event']
    eventScoreAgg = []
    eventAthleteAgg = []

    print('Running event: ', eventName, ' (' + str(time.time() - modelMeetTime) + ')')

    if (len(resultList[eventName])):
      eventTopTime = sorted(copy.deepcopy(resultList[eventName]), key=itemgetter('calculatedTime'), reverse=(eventName in helpers.getDistanceEvents()))[0]['calculatedTime']
    else:
      continue

    for r in range(runs):
      eventScore = {}
      eventAthlete = {}
      eventResultCopy = copy.deepcopy(resultList[eventName])

      for event in eventResultCopy:
        distribution = helpers.getDistribution()

        timeDiff = (eventTopTime * random.choice(distribution)) - eventTopTime
        event['simulatedTime'] = event['calculatedTime'] + timeDiff
        event['prettySimulatedTime'] = helpers.twoDecimalFloat(event['simulatedTime'])

        numberOfRunsSimmed += 1

      sortedEventArray = sorted(eventResultCopy, key=itemgetter('simulatedTime'), reverse=(eventName in helpers.getDistanceEvents()))

      # Get the point scale
      pointScale = helpers.getPointScale()

      for i in range(len(pointScale)):
        # If there exists a result at this scoring position
        if (len(sortedEventArray) > i):
          clubName = sortedEventArray[i]['club']

          if ('name' in sortedEventArray[i]):
            athleteName = sortedEventArray[i]['name'] + ' $ ' + sortedEventArray[i]['club']
            eventAthlete[athleteName] = pointScale[i]
          else:
            eventAthlete[sortedEventArray[i]['club']] = pointScale[i]

          if (clubName in eventScore and (event not in helpers.getRelayEvents()) and eventScore[clubName]['count'] < 3):
            eventScore[clubName]['points'] += pointScale[i]
            eventScore[clubName]['count'] += 1

          elif (clubName not in eventScore):
            eventScore[clubName] = {
              'points': pointScale[i],
              'count': 1
            }

      eventScoreAgg.append(eventScore)
      eventAthleteAgg.append(eventAthlete)

    eventTotalScore = {}
    eventStdDev = {}

    for singleEventScore in eventScoreAgg:
      for club in singleEventScore:
        if (club in eventTotalScore):
          eventTotalScore[club] += singleEventScore[club]['points']
          eventStdDev[club].append(singleEventScore[club]['points'])
        else:
          eventTotalScore[club] = singleEventScore[club]['points']
          eventStdDev[club] = [singleEventScore[club]['points']]

    eventTotalAthleteScore = {}
    eventAthleteStdDev = {}

    for singleEventAthletes in eventAthleteAgg:
      for athlete, points in singleEventAthletes.items():
        if (athlete in eventTotalAthleteScore):
          eventTotalAthleteScore[athlete]['points'] += points
          eventTotalAthleteScore[athlete]['count'] += 1
          eventAthleteStdDev[athlete].append(points)
        else:
          eventTotalAthleteScore[athlete] = {
            'points': points,
            'count': 1
          }
          eventAthleteStdDev[athlete] = [points]

    eventAthleteSummary = {}
    for athlete, data in eventTotalAthleteScore.items():
      if (len(eventAthleteStdDev[athlete]) > 1):
        eventAthleteSummary[athlete] = {
          'average': eventTotalAthleteScore[athlete]['points'] / runs,
          'inScoring': str((eventTotalAthleteScore[athlete]['count'] / runs) * 100) + '%',
          'stddev': statistics.stdev(eventAthleteStdDev[athlete])
        }
      else:
        eventAthleteSummary[athlete] = {
          'average': eventTotalAthleteScore[athlete]['points'] / runs,
          'inScoring': str((eventTotalAthleteScore[athlete]['count'] / runs) * 100) + '%',
          'stddev': 0
        }

    eventSummary = {}
    for club in eventTotalScore:
      if (len(eventStdDev[club]) > 1):
        eventSummary[club] = {
          'average': eventTotalScore[club] / runs,
          'stddev': statistics.stdev(eventStdDev[club])
        }
      else:
        eventSummary[club] = {
          'average': eventTotalScore[club] / runs,
          'stddev': 0
        }

      if (club in meetAverageScore):
        meetAverageScore[club]['points'] += eventSummary[club]['average']
        meetAverageScore[club]['variance'] += eventSummary[club]['stddev'] ** 2
      else:
        meetAverageScore[club] = {
          'points': eventSummary[club]['average'],
          'variance': eventSummary[club]['stddev'] ** 2
        }

    sortedEventAthletes = sorted(eventAthleteSummary.items(), key=lambda x: x[1]['average'], reverse=True)

    pointScale = helpers.getPointScale()
    for i in range(len(pointScale)):
      if (i < len(sortedEventAthletes)):
        modelResult = sortedEventAthletes[i]
      else:
        continue

      if (eventName in helpers.getRelayEvents()):
        club = modelResult[0]
      else:
        name, club = re.split('[$]+', modelResult[0])
        club = club.strip()

      if (club in meetModelScore):
        meetModelScore[club]['points'] += pointScale[i]
      else:
        meetModelScore[club] = {
          'points': pointScale[i]
        }

    sortedEventScores = sorted(eventSummary.items(), key=lambda x: x[1]['average'], reverse=True)
    textOutput.write('\n' + eventName + ':\n')
    textOut.printEventScores(textOutput, sortedEventAthletes)
    textOut.printEventScores(textOutput, sortedEventScores)

  for club in meetAverageScore:
    meetAverageScore[club]['points'] = helpers.twoDecimalFloat(meetAverageScore[club]['points'])
    meetAverageScore[club]['stddev'] = helpers.fourDecimalFloat(meetAverageScore[club]['variance'] ** 0.5)
    meetAverageScore[club].pop('variance', None)

  sortedMeetAverageScores = sorted(meetAverageScore.items(), key=lambda x: x[1]['points'], reverse=True)
  textOut.printMeetScores(textOutput, sortedMeetAverageScores)

  sortedMeetModelScores = sorted(meetModelScore.items(), key=lambda x: x[1]['points'], reverse=True)
  textOut.printMeetScores(textOutput, sortedMeetModelScores)

  print('Number of runs simulated: ', '{:,}'.format(numberOfRunsSimmed))

  helpers.printDuration('Finished model meet', modelMeetTime, time.time())
