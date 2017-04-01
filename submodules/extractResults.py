from . import helpers
import time

def getBlacklistedClubs():
  return ['Iowa', 'GWU']

def extractResults(resultList, columns):
  extractStartTime = time.time()
  # All results from this object
  results = {}

  # For every event
  for column in columns:
    event = column['event']
    columnNum = column['column']

    # Create empty event in result object
    results[event] = {}

    # For every result row
    for row in range(2, resultList.nrows):
      # If there is a result in that column
      if (resultList.cell(row, columnNum).value):
        # If the event is a relay event (3 column)
        if (event in helpers.getRelayEvents()):
          result = {
            'club': resultList.cell(row, columnNum).value,
            'result': resultList.cell(row, columnNum + 1).value,
            'date': resultList.cell(row, columnNum + 2).value
          }

          athleteName = str(result['club'])
        # Else is a 4 column event
        else:
          result = {
            'athlete': resultList.cell(row, columnNum).value,
            'club': resultList.cell(row, columnNum + 1).value,
            'result': resultList.cell(row, columnNum + 2).value,
            'date': resultList.cell(row, columnNum + 3).value
          }

          # Generate namekey for dict
          athleteName = str(result['athlete']) + ' $ ' + str(result['club'])

        # If event is in string form and needs to be converted to float
        if (event in helpers.getStringEvents()):
          result['result'] = helpers.convertStrTimeToFloat(result['result'])

        if (result['club'] in getBlacklistedClubs()):
          continue

        # Insert result into object
        if (athleteName not in results[event].keys()):
          results[event][athleteName] = [ result ]
        else:
          results[event][athleteName].append(result)

  helpers.printDuration('Finished extracting result sheet', extractStartTime, time.time())
  return results
