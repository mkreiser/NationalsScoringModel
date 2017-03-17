from . import helpers
import xlrd

def searchForAthlete(array, name, club):
  for a in array:
    if (a['name'] == name and a['club'] == club):
      return a

def searchForClub(array, club):
  for a in array:
    if (a['club'] == club):
      return a

def overrideAthletes(eventsObject, isWomens):
  overrideBook = xlrd.open_workbook('Overrides.xlsx')
  overrideSheet = overrideBook.sheet_by_name('Overrides')

  if (isWomens):
    column = 0
  else:
    column = 4

  for row in range(2, overrideSheet.nrows):
    if (overrideSheet.cell(row, column).value):
      event = overrideSheet.cell(row, column).value

      if (overrideSheet.cell(row, column + 1).value):
        athleteData = searchForAthlete(eventsObject[event], overrideSheet.cell(row, column + 1).value, overrideSheet.cell(row, column + 2).value)
      else:
        athleteData = searchForAthlete(eventsObject[event], overrideSheet.cell(row, column + 2).value)

      if (not athleteData):
        athleteData = {}

      athleteData['calculatedTime'] = overrideSheet.cell(row, column + 3).value
      athleteData['mean'] = -1
      athleteData['median'] = -1

      athleteData['prettyCalculatedTime'] = helpers.twoDecimalFloat(athleteData['calculatedTime'])
      athleteData['prettyMean'] = -1
      athleteData['prettyMedian'] = -1
