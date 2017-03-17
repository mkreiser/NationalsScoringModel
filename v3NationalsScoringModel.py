from submodules import convertEvents, extractResults, getAthleteData, helpers, mergeResultObjects, modelMeet, override, openBooks, scoreByPureAverage, scoreByCalculatedTime
import sys, time

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

  override.overrideAthletes(womensAthletesAnalyzedTimes, True)
  override.overrideAthletes(mensAthletesAnalyzedTimes, False)

  scoreByPureAverage.scoreByPureAverage(womensAthletesAnalyzedTimes, 'outputs/Womens-Average-Score.txt')
  scoreByPureAverage.scoreByPureAverage(mensAthletesAnalyzedTimes, 'outputs/Mens-Average-Score.txt')

  scoreByCalculatedTime.scoreByCalculatedTime(womensAthletesAnalyzedTimes, 'outputs/Womens-Calculated-Score.txt')
  scoreByCalculatedTime.scoreByCalculatedTime(mensAthletesAnalyzedTimes, 'outputs/Mens-Calculated-Score.txt')

  modelMeet.modelMeet(womensAthletesAnalyzedTimes, 'outputs/Womens-Model-Score.txt', int(sys.argv[1]))
  modelMeet.modelMeet(mensAthletesAnalyzedTimes, 'outputs/Mens-Model-Score.txt', int(sys.argv[1]))

  helpers.printDuration('Completed program', envStartTime, time.time())
