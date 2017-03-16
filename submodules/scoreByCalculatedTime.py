from . import helpers, textOut
from operator import itemgetter
import copy, time

def scoreByCalculatedTime(resultList, filename):
  scoreByPureTime = time.time()
  textOutput = open(filename, 'w')
  meetScore = {}

  for outdoorColumn in helpers.getOutdoorColumns():
    event = outdoorColumn['event']
    eventScore = {}
    eventResultCopy = copy.deepcopy(resultList[event])

    if (len(eventResultCopy) == 0):
      continue

    sortedEventArray = sorted(eventResultCopy, key=itemgetter('calculatedTime'), reverse=(event in helpers.getDistanceEvents()))

    # Get the point scale
    pointScale = helpers.getPointScale()
    # Score the event
    textOutput.write('\n-----------------------------' + event + '-----------------------------\n\n')

    keyArray = ['Position']
    if ('name' in sortedEventArray[0]):
      keyArray.append('Name')

    keyArray += ['Club', 'Calculated Time', 'Mean', 'Median']
    textOutput.write(''.join(key.ljust(20) for key in keyArray))
    textOutput.write('\n')

    for i in range(20):
      if (len(sortedEventArray) > i):
        clubName = sortedEventArray[i]['club']

        if (len(pointScale) > i):
          points = pointScale[i]
        else:
          points = 0

        textOut.printEventAthletes(textOutput, sortedEventArray[i], points, i + 1)

        if (len(pointScale) > i):
          if (clubName in eventScore and (event not in helpers.getRelayEvents()) and eventScore[clubName]['count'] < 3):
            eventScore[clubName]['points'] += points
            eventScore[clubName]['count'] += 1

          elif (clubName not in eventScore):
            eventScore[clubName] = {
              'points': points,
              'count': 1
            }

    for club, clubPoints in eventScore.items():
      if (club in meetScore):
        meetScore[club] += clubPoints['points']
      else:
        meetScore[club] = clubPoints['points']

    sortedEventScores = sorted(eventScore.items(), key=lambda x: x[1]['points'], reverse=True)
    textOut.printEventScores(textOutput, sortedEventScores)

  # Sorts the meets scores for output in format (club, score)
  sortedMeetScores = sorted(meetScore.items(), key=itemgetter(1), reverse=True)
  textOut.printMeetScores(textOutput, sortedMeetScores)

  textOutput.close()

  helpers.printDuration('Finished scoring by calculated time', scoreByPureTime, time.time())
