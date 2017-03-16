
from . import helpers
import time, xlrd

def openBooks():
  BooksStartTime = time.time()

  # Open the indoor workbook and grab the sheets
  indoorWB = xlrd.open_workbook('Indoor.xlsx')
  indoorWomenSheet = indoorWB.sheet_by_name('Women')
  indoorMenSheet = indoorWB.sheet_by_name('Men')

  # Open the outoor workbook and grab the sheets
  outdoorWB = xlrd.open_workbook('Outdoor.xlsx')
  outdoorWomenSheet = outdoorWB.sheet_by_name('Women')
  outdoorMenSheet = outdoorWB.sheet_by_name('Men')

  helpers.printDuration('Done opening books', BooksStartTime, time.time())

  # Return all indoor and outdoor sheets
  return (indoorWomenSheet, indoorMenSheet, outdoorWomenSheet, outdoorMenSheet)
