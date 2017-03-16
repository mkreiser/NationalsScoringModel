from . import helpers, textOut
from operator import itemgetter
import copy, random, re, statistics, time

def modelMeet(resultList, filename, runs):
  modelMeetTime = time.time()
  # Open an output to .txt file
  textOutput = open(filename, 'w')

  # Set up storage
  meetAverageScore = {}
  meetModelScore = {}
  numberOfRunsSimmed = 0

  # For every outdoor event
  for outdoorColumn in helpers.getOutdoorColumns():
    # Grab the event name and set up event specific storage
    eventName = outdoorColumn['event']
    eventScoreAgg = []
    eventAthleteAgg = []

    # Notify console that a new event is being run
    print('Running event: ', eventName, ' (' + str(time.time() - modelMeetTime) + ')')

    # If there are results, then grab the top calculated time
    if (len(resultList[eventName])):
      eventTopTime = sorted(copy.deepcopy(resultList[eventName]), key=itemgetter('calculatedTime'), reverse=(eventName in helpers.getDistanceEvents()))[0]['calculatedTime']
    # Else, if there are no results, skip processing this event
    else:
      continue

    # Run the event (runs) times
    for r in range(runs):
      # Set up run specific storage
      eventScore = {}
      eventAthlete = {}
      eventResultCopy = copy.deepcopy(resultList[eventName])

      # for every athlete in the event
      for athleteResult in eventResultCopy:
        # Grab the distribution
        distribution = helpers.getDistribution()

        # Calculate the random time influence as (the top time *  a value from the distribution) - the top time
        # e.g. if the top time is 100 (seconds) and the distribution returns 0.97, then (100 * 0.97) - 100 - -3.00
        timeDiff = (eventTopTime * random.choice(distribution)) - eventTopTime
        # Apply the time influence to the athlete's original weighted time
        athleteResult['simulatedTime'] = athleteResult['calculatedTime'] + timeDiff
        # Round for printing
        athleteResult['prettySimulatedTime'] = helpers.twoDecimalFloat(athleteResult['simulatedTime'])

        # Keep track of how many performances are modeled
        numberOfRunsSimmed += 1

      # Now that all of the events have been "modeled", sort the results (order high-to-low if event is a distance event)
      sortedEventArray = sorted(eventResultCopy, key=itemgetter('simulatedTime'), reverse=(eventName in helpers.getDistanceEvents()))

      # Get the point scale
      pointScale = helpers.getPointScale()

      # For every scoring position
      for i in range(len(pointScale)):
        # If there exists a result at this scoring position
        if (len(sortedEventArray) > i):
          # Grab the club belonging to the performance
          clubName = sortedEventArray[i]['club']

          # If name is present, then the performance is from an athlete (not a relay)
          if ('name' in sortedEventArray[i]):
            # Let name be identifible
            athleteName = sortedEventArray[i]['name'] + ' $ ' + sortedEventArray[i]['club']
            # add in the points
            eventAthlete[athleteName] = pointScale[i]
          else:
            # Add in the points assuming it's a club (means it's a relay result)
            eventAthlete[sortedEventArray[i]['club']] = pointScale[i]

          # If the performance counts toward the meet score
          if (clubName in eventScore and (eventName not in helpers.getRelayEvents()) and eventScore[clubName]['count'] < 3):
            eventScore[clubName]['points'] += pointScale[i]
            eventScore[clubName]['count'] += 1

          # Performance is first one from the club, so count it
          elif (clubName not in eventScore):
            eventScore[clubName] = {
              'points': pointScale[i],
              'count': 1
            }

      # Append the run results to the event storage
      eventScoreAgg.append(eventScore)
      eventAthleteAgg.append(eventAthlete)

    # Process the event
    # Set up storage
    eventTotalScore = {}
    eventStdDev = {}

    # For each event sim run
    for singleEventScore in eventScoreAgg:
      # Grab each club
      for club in singleEventScore:
        # Add the club points to the total points scored in the event (averaged next)
        if (club in eventTotalScore):
          eventTotalScore[club] += singleEventScore[club]['points']
          eventStdDev[club].append(singleEventScore[club]['points'])
        else:
          eventTotalScore[club] = singleEventScore[club]['points']
          eventStdDev[club] = [singleEventScore[club]['points']]

    # Average the event results and add them to the meet scoring
    eventSummary = {}
    for club in eventTotalScore:
      # Average the event points
      if (len(eventStdDev[club]) > 1):
        eventSummary[club] = {
          'average': eventTotalScore[club] / runs,
          'stddev': helpers.sixDecimalFloat(statistics.stdev(eventStdDev[club]))
        }
      else:
        eventSummary[club] = {
          'average': eventTotalScore[club] / runs,
          'stddev': 0
        }

      # Add the points to the meet scoring
      if (club in meetAverageScore):
        meetAverageScore[club]['points'] += eventSummary[club]['average']
        meetAverageScore[club]['variance'] += eventSummary[club]['stddev'] ** 2
      else:
        meetAverageScore[club] = {
          'points': eventSummary[club]['average'],
          'variance': eventSummary[club]['stddev'] ** 2
        }

    # Process how each athlete scores in the event sim
    eventTotalAthleteScore = {}
    eventAthleteStdDev = {}

    # For every event sim run
    for singleEventAthletes in eventAthleteAgg:
      # For each scoring athlete
      for athlete, points in singleEventAthletes.items():
        # Add their points to the summary storage
        if (athlete in eventTotalAthleteScore):
          eventTotalAthleteScore[athlete]['points'] += points
          eventTotalAthleteScore[athlete]['pointsList'].append(points)
          eventTotalAthleteScore[athlete]['count'] += 1
          eventAthleteStdDev[athlete].append(points)
        else:
          eventTotalAthleteScore[athlete] = {
            'points': points,
            'pointsList': [ points ],
            'count': 1
          }
          eventAthleteStdDev[athlete] = [points]

    # Process the event athelte summary storage
    eventAthleteSummary = {}
    for athlete, data in eventTotalAthleteScore.items():
      # If there is a standard deviation
      if (len(eventAthleteStdDev[athlete]) > 1):
        # Calculate the mode
        try:
          mode = statistics.mode(eventTotalAthleteScore[athlete]['pointsList']),
          mode = mode[0]
        except statistics.StatisticsError:
          mode = eventTotalAthleteScore[athlete]['pointsList'][0]

        # Produce the athlete's summary of their model data
        eventAthleteSummary[athlete] = {
          'average': eventTotalAthleteScore[athlete]['points'] / runs,
          'inScoring': str(helpers.twoDecimalFloat((eventTotalAthleteScore[athlete]['count'] / runs) * 100)) + '%',
          'median': statistics.median(eventTotalAthleteScore[athlete]['pointsList']),
          'mode': mode,
          'stddev': helpers.sixDecimalFloat(statistics.stdev(eventAthleteStdDev[athlete]))
        }
      # Produce the athlete's summary of their model data
      else:
        eventAthleteSummary[athlete] = {
          'average': eventTotalAthleteScore[athlete]['points'] / runs,
          'inScoring': str(helpers.twoDecimalFloat((eventTotalAthleteScore[athlete]['count'] / runs) * 100)) + '%',
          'median': statistics.median(eventTotalAthleteScore[athlete]['pointsList']),
          'mode': eventTotalAthleteScore[athlete]['pointsList'][0],
          'stddev': 0
        }

    # Sort the athletes' performances by their averages
    sortedEventAthletes = sorted(eventAthleteSummary.items(), key=lambda x: x[1]['average'], reverse=True)

    # Score the event by where the athletes placed in the model sim (not adding their average points)
    pointScale = helpers.getPointScale()
    for i in range(len(pointScale)):
      if (i < len(sortedEventAthletes)):
        modelResult = sortedEventAthletes[i]
      else:
        continue

      if (eventName in helpers.getRelayEvents()):
        club = modelResult[0]
      else:
        name, club = re.split('[$]+', modelResult[0])
        club = club.strip()

      if (club in meetModelScore):
        meetModelScore[club] += pointScale[i]
      else:
        meetModelScore[club] = pointScale[i]

    # Sort the club point summary for the event
    sortedEventScores = sorted(eventSummary.items(), key=lambda x: x[1]['average'], reverse=True)
    textOutput.write('\n-----------------------------' + eventName + '-----------------------------\n')
    # Print the athlete's result in the event in the model
    textOut.printModelEventAthleteScores(textOutput, sortedEventAthletes)
    # Print the club's points in the event in the model
    textOut.printModelEventScores(textOutput, sortedEventScores)

  # Process the meet
  for club in meetAverageScore:
    # Round the points and calculate the stddev
    meetAverageScore[club]['points'] = helpers.twoDecimalFloat(meetAverageScore[club]['points'])
    meetAverageScore[club]['stddev'] = helpers.sixDecimalFloat(meetAverageScore[club]['variance'] ** 0.5)
    meetAverageScore[club].pop('variance', None)

  # Print the sum of the average scores in the model
  sortedMeetAverageScores = sorted(meetAverageScore.items(), key=lambda x: x[1]['points'], reverse=True)
  textOut.printMeetScoresWithDev(textOutput, sortedMeetAverageScores)

  # Print the sum of the positional scores in the model
  sortedMeetModelScores = sorted(meetModelScore.items(), key=lambda x: x[1], reverse=True)
  textOut.printMeetScores(textOutput, sortedMeetModelScores)

  # Close the text output
  textOutput.close()

  # Notify console
  print('Number of runs simulated: ', '{:,}'.format(numberOfRunsSimmed))

  helpers.printDuration('Finished model meet', modelMeetTime, time.time())
