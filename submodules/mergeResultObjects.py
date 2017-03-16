from . import helpers
import time

def mergeResultObjects(indoorEventObject, outdoorEventObject):
  mergeStartTime = time.time()

  # For all outdoor events
  for outdoorColumn in helpers.getOutdoorColumns():
    event = outdoorColumn['event']

    # Verify event is an indoor event as well
    if event in indoorEventObject:
      # Get indoor and outdoor event results
      indoorEventResults = indoorEventObject[event]
      outdoorEventResults = outdoorEventObject[event]

      # Grab every athlete in indoor results
      for name, athleteResults in indoorEventResults.items():
        # If athlete is already in the outdoor results, merge
        if name in outdoorEventResults:
          outdoorEventResults[name] = outdoorEventResults[name] + athleteResults
        # Else add the athlete to outdoor result
        else:
          outdoorEventResults[name] = athleteResults

  helpers.printDuration('Merged result objects', mergeStartTime, time.time())