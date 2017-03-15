from . import helpers

def printEventAthletes(outputObject, result, resultKey, points):
  if ('name' in result):
    outputObject.write(result['name'] + ' ' + result['club'] + ': ' + str(result[resultKey]) + ', points: ' + str(points) + '\n')
  else:
    outputObject.write(result['club'] + ': ' + str(result[resultKey]) + ', points: ' + str(points) + '\n')

def printEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  for score in sortedEventScores:
      outputObject.write(score[0] + ': ' + str(score[1]) + '\n')

def printMeetScores(outputObject, sortedMeetScores):
  outputObject.write('\nMeet Score:\n')
  for club in sortedMeetScores:
    outputObject.write(str(club[0]) + ': ' + str(club[1]) + '\n')
