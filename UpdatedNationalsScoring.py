from operator import itemgetter
import copy, math, random, re, statistics, time, xlrd

# Open all workbooks
start_time = time.time()
print('Opening books')
indoorWB = xlrd.open_workbook('Indoor.xlsx')
outdoorWB = xlrd.open_workbook('Outdoor.xlsx')

womenIndoorSheet = indoorWB.sheet_by_name('Women')
menIndoorSheet = indoorWB.sheet_by_name('Men')

womenOutdoorSheet = outdoorWB.sheet_by_name('Women')
menOutdoorSheet = outdoorWB.sheet_by_name('Men')

prettyTextOutput = open('meetoutput.txt', 'w')
print('Done opening books: ' + str(time.time() - start_time))

# Create data structures to hold all results from Excel files
womensIndoorResults = {}
mensIndoorResults = {}
womensOutdoorResults = {}
mensOutdoorResults = {}

indoorExcelRange = [0, 5, 10, 15, 20, 25, 30, 35, 39, 43, 47, 52, 57]
outdoorExcelRange = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 50, 54, 58, 63, 68, 73, 78]
distanceEvents = ['Long Jump', 'High Jump', 'Triple Jump', 'Shotput', 'Discus']
relayEvents = ['4x100m Relay', '4x400m Relay', '4x800m Relay']

points = [10, 8, 7, 6, 5, 4, 3, 2, 1]

def twoDecimalFloat(num):
	return float('{0:.2f}'.format(num))

def fourDecimalFloat(num):
	return float('{0:.4f}'.format(num))

def sixDecimalFloat(num):
	return float('{0:.6f}'.format(num))

def seasonResultAgg(sheet, resultArray, sheetRanges, shortedRanges):
	for column in sheetRanges:
		resultArray[sheet.cell(0, column).value] = []

		for row in range(2, sheet.nrows):
			if (sheet.cell(row, column).value):
				if (column not in shortedRanges):
					result = {
						'athlete' : sheet.cell(row, column).value,
						'club': sheet.cell(row, column + 1).value,
						'result': sheet.cell(row, column + 2).value,
					}
				else:
					result = {
						'club' : sheet.cell(row, column).value,
						'result': sheet.cell(row, column + 1).value
					}

				resultArray[sheet.cell(0, column).value].append(result)

def convertStringTimes(seasonArray, indoor=False):
	dropColons = ['5000m', '1500m', '800m', '3000m Steeplechase', '4x400m Relay', '4x800m Relay', '1 Mile', '3000m']

	for event in dropColons:
		if (event in list(seasonArray.keys())):
			for i in range(len(seasonArray[event])):
				mark = seasonArray[event][i]
				if (isinstance(mark['result'], str)):
					minutes, seconds, hunds = re.split('[:.]+', mark['result'])
					mark['result'] = (int(minutes) * 60 + int(seconds) + int(hunds) / 100)

	for event in distanceEvents:
		if (not indoor or (indoor and (event is not 'Shotput' and event is not 'Discus'))):
			for i in range(len(seasonArray[event])):
				mark = seasonArray[event][i]
				if (isinstance(mark['result'], str)):
					mark['result'] = float(mark['result'].split('m')[0])

def convertEvent(indoorResults, outdoorResults, indoorEvent, outdoorEvent, conversionFormula):
	for i in range(len(indoorResults[indoorEvent])):
		mark = indoorResults[indoorEvent][i]
		mark['result'] = twoDecimalFloat(conversionFormula(mark['result']))
		outdoorResults[outdoorEvent].append(mark)

def mergeEventDelegate(event, eventArray, mergedDict):
	# Loop through every mark in eventArray
	for mark in eventArray:
		# Give athlete unique name for hashing in mergedDict
		if('athlete' in mark):
				name = mark['athlete'] + '$$$' + mark['club']
		else:
			name = mark['club']

		# If athlete already exists in mergedDict
		if (name in mergedDict[event]):
			if (event in distanceEvents):
				if (mark['result'] > mergedDict[event][name]['result']):
					mergedDict[event][name]['result'] = mark['result']
			else: 
				if (mark['result'] < mergedDict[event][name]['result']):
					mergedDict[event][name]['result'] = mark['result']

			mergedDict[event][name]['average'] += mark['result']
			mergedDict[event][name]['count'] += 1

		# Else add athlete to mergedDict
		else:
			mergedDict[event][name] = mark
			mergedDict[event][name]['average'] = mark['result']
			mergedDict[event][name]['count'] = 1


def mergeAthleteEventResults(indoorArray, outdoorArray):
	mergedWithArrays = {}
	mergedDict = {}

	for event, eventArray in outdoorArray.items():
		mergedWithArrays[event] = []
		mergedDict[event] = {}
		mergeEventDelegate(event, eventArray, mergedDict)

	for event, eventArray in indoorArray.items():
		if (event in list(outdoorArray.keys())):
			mergeEventDelegate(event, eventArray, mergedDict)

	for event in list(outdoorArray.keys()):
		for athlete, performance in mergedDict[event].items():
			performance['average'] = twoDecimalFloat(performance['average'] / performance['count'])
			mergedWithArrays[event].append(performance)

	return copy.deepcopy(mergedWithArrays)

def nonModelMeet(meet):
	meetScore = {}

	for event, eventArray in meet.items():
		eventScore = {}
		eventArrayCopy = copy.deepcopy(eventArray)

		sortedEventArray = sorted(eventArrayCopy, key=itemgetter('result'), reverse=(event in distanceEvents))

		for i in range(9):
			if (len(sortedEventArray) > i):
				if (sortedEventArray[i]['club'] in eventScore and (not event in relayEvents) and eventScore[sortedEventArray[i]['club']]['count'] < 3):
					eventScore[sortedEventArray[i]['club']]['points'] += points[i]
					eventScore[sortedEventArray[i]['club']]['count'] += 1
				else:
					eventScore[sortedEventArray[i]['club']] = {
						'points': points[i],
						'count': 1,
					}

		for club, clubPoints in eventScore.items():
			if (club in meetScore):
				meetScore[club] += clubPoints['points']
			else:
				meetScore[club] = clubPoints['points']

		# Print event scores in order to output
		sortedEvent = sorted(eventScore.items(), key=lambda x: x[1]['points'], reverse=True)
		prettyTextOutput.write('\n' + event + ':\n')
		for score in sortedEvent:
			prettyTextOutput.write(score[0] + ': ' + str(score[1]) + '\n')

	# Output final meet results
	sortedMeet = sorted(meetScore.items(), key=itemgetter(1), reverse=True)
	prettyTextOutput.write('\nFinal Results:\n')
	for club in sortedMeet:
		prettyTextOutput.write(club[0] + ': ' + str(club[1]) + '\n')
	prettyTextOutput.write('\n------------------------------------------\n')

def modelMeet(meet, runs):
	meetScore = {}

	for event, eventArray in meet.items():
		eventScoreAgg = []

		for r in range(runs):
			eventScore = {}
			eventArrayCopy = copy.deepcopy(eventArray)

			for i in range(len(eventArrayCopy)):
				eventArrayCopy[i]['result'] = eventArrayCopy[i]['result'] * random.uniform(0.97, 1.05)

			sortedEventArray = sorted(eventArrayCopy, key=itemgetter('result'), reverse=(event in distanceEvents))

			for i in range(9):
				if (len(sortedEventArray) > i):
					if (sortedEventArray[i]['club'] in eventScore and (not event in relayEvents) and eventScore[sortedEventArray[i]['club']]['count'] < 3):
						eventScore[sortedEventArray[i]['club']]['points'] += points[i]
						eventScore[sortedEventArray[i]['club']]['count'] += 1
					else:
						eventScore[sortedEventArray[i]['club']] = {
							'points': points[i],
							'count': 1
						}

			eventScoreAgg.append(eventScore)

		eventScorer = {}
		eventStdDev = {}
		for singleEventScore in eventScoreAgg:
			for club in singleEventScore:
				if (club in eventScorer):
					eventScorer[club] += singleEventScore[club]['points']
					eventStdDev[club].append(singleEventScore[club]['points'])
				else:
					eventScorer[club] = singleEventScore[club]['points']
					eventStdDev[club] = [singleEventScore[club]['points']]


		eventSummary = {}
		for club in eventScorer:
			if (len(eventStdDev[club]) > 1):
				eventSummary[club] = {
					'average': eventScorer[club] / runs,
					'stddev': statistics.stdev(eventStdDev[club])
				}
			else:
				eventSummary[club] = {
					'average': eventScorer[club] / runs,
					'stddev': 0
				}

			if (club in meetScore):
				meetScore[club]['points'] += eventSummary[club]['average']
				meetScore[club]['variance'] += eventSummary[club]['stddev'] ** 2
			else:
				meetScore[club] = {
					'points': eventSummary[club]['average'],
					'variance': eventSummary[club]['stddev'] ** 2
				}

		sortedEvent = sorted(eventSummary.items(), key=lambda x: x[1]['average'], reverse=True)
		prettyTextOutput.write('\n' + event + ':\n')
		for score in sortedEvent:
			score[1]['stddev'] = fourDecimalFloat(score[1]['stddev'])
			prettyTextOutput.write(score[0] + ': ' + str(score[1]) + '\n')

	for club in meetScore:
		meetScore[club]['points'] = twoDecimalFloat(meetScore[club]['points'])
		meetScore[club]['stddev'] = fourDecimalFloat(meetScore[club]['variance'] ** 0.5)
		meetScore[club].pop('variance', None)

	sortedMeet = sorted(meetScore.items(), key=lambda x: x[1]['points'], reverse=True)

	prettyTextOutput.write('\nFinal Results:\n')
	for club in sortedMeet:
		prettyTextOutput.write(club[0] + ': ' + str(club[1]) + '\n')
	prettyTextOutput.write('\n------------------------------------------\n')

def aggregateResults():
	print('Aggregating indoor results')
	seasonResultAgg(womenIndoorSheet, womensIndoorResults, indoorExcelRange, [35, 39, 43])
	seasonResultAgg(menIndoorSheet, mensIndoorResults, indoorExcelRange, [35, 39, 43])
	print('Aggregating outdoor results')
	seasonResultAgg(womenOutdoorSheet, womensOutdoorResults, outdoorExcelRange, [46, 50, 54])
	seasonResultAgg(menOutdoorSheet, mensOutdoorResults, outdoorExcelRange, [46, 50, 54])
	print('Done aggregating results: ' + str(time.time() - start_time))

def convertTimes():
	print('Converting times and events')
	convertStringTimes(womensIndoorResults, True)
	convertStringTimes(mensIndoorResults, True)
	convertStringTimes(womensOutdoorResults)
	convertStringTimes(mensOutdoorResults)

	convertEvent(womensIndoorResults, womensOutdoorResults, '60m', '100m', lambda x: x*2 - 3.1)
	convertEvent(mensIndoorResults, mensOutdoorResults, '60m', '100m', lambda x: x*2 - 3.1)
	convertEvent(womensIndoorResults, womensOutdoorResults, '60m HH', '100m HH', lambda x: x*2 - 3.1)
	convertEvent(mensIndoorResults, mensOutdoorResults, '60m HH', '110m HH', lambda x: x*2 - 3.1)
	convertEvent(womensIndoorResults, womensOutdoorResults, '1 Mile', '1500m', lambda x: x * 0.9259)
	convertEvent(mensIndoorResults, mensOutdoorResults, '1 Mile', '1500m', lambda x: x * 0.9259)
	convertEvent(womensIndoorResults, womensOutdoorResults, '3000m', '5000m', lambda x: x * ((5/3)**1.06))
	convertEvent(mensIndoorResults, mensOutdoorResults, '3000m', '5000m', lambda x: x * ((5/3)**1.06))
	print('Done converting times and events ' + str(time.time() - start_time))

def runNonModelMeet():
	print('Running nonmodel meets')
	prettyTextOutput.write('NON MODEL MEET\n')
	prettyTextOutput.write('Women\'s Results\n')
	nonModelMeet(mergedWomensResult)
	prettyTextOutput.write('Men\'s Results\n')
	nonModelMeet(mergedMensResult)
	print('Done with nonmodel meets ' + str(time.time() - start_time))

	print('Running model meets')
	prettyTextOutput.write('MODEL MEET:\n')
	prettyTextOutput.write('Women\'s Results\n')
	modelMeet(mergedWomensResult, 10000)
	print('Done with women\'s model meets ' + str(time.time() - start_time))
	prettyTextOutput.write('Men\'s Results\n')
	modelMeet(mergedMensResult, 10000)
	print('Done with men\'s model meets ' + str(time.time() - start_time))

def cleanup():
	prettyTextOutput.close()

aggregateResults()
convertTimes()
mergedWomensResult = mergeAthleteEventResults(womensIndoorResults, womensOutdoorResults)
mergedMensResult = mergeAthleteEventResults(mensIndoorResults, mensOutdoorResults)
runNonModelMeet()
cleanup()
