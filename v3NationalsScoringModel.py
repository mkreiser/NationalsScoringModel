from submodules import convertEvents, extractResults, getAthleteData, helpers, mergeResultObjects, modelMeet, openBooks, scoreByPureAverage, scoreByCalculatedTime
import time

if __name__ == '__main__':
  envStartTime = time.time()

  indoorWomenSheet, indoorMenSheet, outdoorWomenSheet, outdoorMenSheet = openBooks.openBooks()

  indoorWomensResults = extractResults.extractResults(indoorWomenSheet, helpers.getIndoorColumns())
  indoorMensResults = extractResults.extractResults(indoorMenSheet, helpers.getIndoorColumns())

  outdoorWomensResults = extractResults.extractResults(outdoorWomenSheet, helpers.getOutdoorColumns())
  outdoorMensResults = extractResults.extractResults(outdoorMenSheet, helpers.getOutdoorColumns())

  convertEvents.convertEvents(indoorWomensResults)
  convertEvents.convertEvents(indoorMensResults)

  mergeResultObjects.mergeResultObjects(indoorWomensResults, outdoorWomensResults)
  mergeResultObjects.mergeResultObjects(indoorMensResults, outdoorMensResults)

  womensAthletesAnalyzedTimes = getAthleteData.getAthleteData(outdoorWomensResults)
  mensAthletesAnalyzedTimes = getAthleteData.getAthleteData(outdoorMensResults)

  scoreByPureAverage.scoreByPureAverage(womensAthletesAnalyzedTimes, 'outputs/Womens-Pure-Score.txt')
  scoreByPureAverage.scoreByPureAverage(mensAthletesAnalyzedTimes, 'outputs/Mens-Pure-Score.txt')

  scoreByCalculatedTime.scoreByCalculatedTime(womensAthletesAnalyzedTimes, 'outputs/Womens-Calculated-Score.txt')
  scoreByCalculatedTime.scoreByCalculatedTime(mensAthletesAnalyzedTimes, 'outputs/Mens-Calculated-Score.txt')

  modelMeet.modelMeet(womensAthletesAnalyzedTimes, 'outputs/Womens-Model-Score.txt', 10000)
  modelMeet.modelMeet(mensAthletesAnalyzedTimes, 'outputs/Mens-Model-Score.txt', 10000)

  helpers.printDuration('Completed program', envStartTime, time.time())
