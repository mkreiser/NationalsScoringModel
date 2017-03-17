from . import helpers

# Prints a spaced line of columns
def printJoinedLine(outputObject, arrayToJoin, justNum):
  outputObject.write(''.join(str(text).ljust(justNum) for text in arrayToJoin))
  outputObject.write('\n')

# Prints the athlete's data for an event in non-model sims
def printEventAthletes(outputObject, result, points, position):
  arrayToJoin = [position]
  if ('name' in result):
    keysToGrab = ['name', 'club', 'prettyCalculatedTime', 'prettyMean', 'prettyMedian']
  else:
    keysToGrab = ['club', 'prettyCalculatedTime', 'prettyMean', 'prettyMedian']

  arrayToJoin += [result[key] for key in keysToGrab]
  printJoinedLine(outputObject, arrayToJoin, 20)

# Prints the total scores for team in an event for a non-model sim
def printEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Team', 'Points', 'Count']
    printJoinedLine(outputObject, keyArray, 15)

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['points'], score[1]['count'] ]
    printJoinedLine(outputObject, arrayToJoin, 15)

# Prints the athlete's data for an event in a model meet
def printModelEventAthleteScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Athlete/Team', 'Average', 'Stddev', 'In Scoring', 'Median', 'Mode']
    printJoinedLine(outputObject, keyArray, 26)

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['average'], score[1]['stddev'], score[1]['inScoring'], score[1]['median'], score[1]['mode']]
    printJoinedLine(outputObject, arrayToJoin, 26)

# Prints the total scores for team in an event for a model sim
def printModelEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  if (len(sortedEventScores) > 0):
    keyArray = ['Position', 'Team', 'Average', 'Stddev']
    printJoinedLine(outputObject, keyArray, 15)

  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    arrayToJoin = [ i + 1, score[0], score[1]['average'], score[1]['stddev'] ]
    printJoinedLine(outputObject, arrayToJoin, 15)

# Prints the total scoring for a meet in a non-model sim
def printMeetScores(outputObject, sortedMeetScores):
  outputObject.write('\n-----------------------------Meet Score-----------------------------\n\n')

  keys = ['Position', 'Team', 'Points']
  printJoinedLine(outputObject, keys, 15)

  for i in range(len(sortedMeetScores)):
    club = sortedMeetScores[i]
    values = [i + 1, club[0], club[1]]
    printJoinedLine(outputObject, values, 15)

# Print the total scoring for a meet in a model sim
def printMeetScoresWithDev(outputObject, sortedMeetScores):
  outputObject.write('\n-----------------------------Meet Score-----------------------------\n\n')

  keyArray = ['Position', 'Team', 'Average points', 'Stddev']
  printJoinedLine(outputObject, keyArray, 15)

  for i in range(len(sortedMeetScores)):
    club = sortedMeetScores[i]
    arrayToJoin = [ i + 1, club[0], club[1]['points'], club[1]['stddev'] ]
    printJoinedLine(outputObject, arrayToJoin, 15)
