from . import helpers

def printEventAthletes(outputObject, result, resultKey, points):
  if ('name' in result):
    outputObject.write(result['name'] + ' ' + result['club'] + ': ' + str(result[resultKey]) + ', points: ' + str(points) + '\n')
  else:
    outputObject.write(result['club'] + ': ' + str(result[resultKey]) + ', points: ' + str(points) + '\n')

def printEventScores(outputObject, sortedEventScores):
  outputObject.write('\n')
  for i in range(len(sortedEventScores)):
    score = sortedEventScores[i]
    if (i < 9):
      outputObject.write(str(i + 1) + '.)  ' + score[0] + ': ' + str(score[1]) + '\n')
    else:
      outputObject.write(str(i + 1) + '.) ' + score[0] + ': ' + str(score[1]) + '\n')


def printMeetScores(outputObject, sortedMeetScores):
  outputObject.write('\nMeet Score:\n')
  for i in range(len(sortedMeetScores)):
    club = sortedMeetScores[i]
    if (i < 9):
      outputObject.write(str(i + 1) + '.)  ' + str(club[0]) + ': ' + str(club[1]) + '\n')
    else:
      outputObject.write(str(i + 1) + '.) ' + str(club[0]) + ': ' + str(club[1]) + '\n')
