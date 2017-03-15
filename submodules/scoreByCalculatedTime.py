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

    sortedEventArray = sorted(eventResultCopy, key=itemgetter('calculatedTime'), reverse=(event in helpers.getDistanceEvents()))

    # Get the point scale
    pointScale = helpers.getPointScale()
    # Score the event
    textOutput.write('\n' + event + ':\n')
    # For as many scoring positions
    for i in range(len(pointScale)):
      # If there exists a result at this scoring position
      if (len(sortedEventArray) > i):
        clubName = sortedEventArray[i]['club']

        textOut.printEventAthletes(textOutput, sortedEventArray[i], 'prettyCalculatedTime', pointScale[i])

        if (clubName in eventScore and (event not in helpers.getRelayEvents()) and eventScore[clubName]['count'] < 3):
          eventScore[clubName]['points'] += pointScale[i]
          eventScore[clubName]['count'] += 1

        elif (clubName not in eventScore):
          eventScore[clubName] = {
            'points': pointScale[i],
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

  helpers.printDuration('Finished scoring by calculated time', scoreByPureTime, time.time())
