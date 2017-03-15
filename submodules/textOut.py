from . import helpers

def printEventAthletes(outputObject, result, points, position):
  arrayToJoin = [position]
  if ('name' in result):
    keysToGrab = ['name', 'club', 'prettyCalculatedTime', 'prettyMean', 'prettyMedian']
  else:
    keysToGrab = ['club', 'prettyCalculatedTime', 'prettyMean', 'prettyMedian']

  arrayToJoin += [result[key] for key in keysToGrab]
  outputObject.write(''.join(str(text).ljust(20) for text in arrayToJoin))
  outputObject.write('\n')

def printEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Team', 'Points', 'Count']
    outputObject.write(''.join(key.ljust(26) for key in keyArray))
    outputObject.write('\n')

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['points'], score[1]['count'] ]

    outputObject.write(''.join(str(text).ljust(26) for text in arrayToJoin))
    outputObject.write('\n')

def printModelEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Team', 'Average', 'Stddev']
    outputObject.write(''.join(key.ljust(26) for key in keyArray))
    outputObject.write('\n')

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['average'], score[1]['stddev'] ]

    outputObject.write(''.join(str(text).ljust(26) for text in arrayToJoin))
    outputObject.write('\n')

def printModelEventAthleteScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Athlete/Team', 'Average', 'Stddev', 'In Scoring', 'Median', 'Mode']
    outputObject.write(''.join(key.ljust(26) for key in keyArray))
    outputObject.write('\n')

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['average'], score[1]['stddev'], score[1]['inScoring'], score[1]['median'], score[1]['mode']]

    outputObject.write(''.join(str(text).ljust(26) for text in arrayToJoin))
    outputObject.write('\n')

def printMeetScores(outputObject, sortedMeetScores):
  outputObject.write('\n-----------------------------Meet Score:-----------------------------\n\n')

  keys = ['Position', 'Team', 'Points']
  outputObject.write(''.join(str(text).ljust(26) for text in keys))
  outputObject.write('\n')

  for i in range(len(sortedMeetScores)):
    club = sortedMeetScores[i]
    values = [i + 1, club[0], club[1]]
    outputObject.write(''.join(str(text).ljust(26) for text in values))
    outputObject.write('\n')

def printMeetScoresWithDev(outputObject, sortedMeetScores):
  outputObject.write('\n-----------------------------Meet Score-----------------------------\n\n')

  keyArray = ['Position', 'Team', 'Average points', 'Stddev']
  outputObject.write(''.join(key.ljust(26) for key in keyArray))
  outputObject.write('\n')

  for i in range(len(sortedMeetScores)):
    club = sortedMeetScores[i]

    arrayToJoin = [ i + 1, club[0], club[1]['points'], club[1]['stddev'] ]

    outputObject.write(''.join(str(text).ljust(26) for text in arrayToJoin))
    outputObject.write('\n')
