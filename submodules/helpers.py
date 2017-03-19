import re

# Prints a string describing the duration with said duration
def printDuration(string, startTime, endTime):
  print(string, endTime - startTime)

# Converts a string style result time to seconds as a float
# ex: 2:15.45 --> 135.45
def convertStrTimeToFloat(inputTime):
  minutes, seconds, hunds = re.split('[:.]+', inputTime)
  return (int(minutes) * 60 + int(seconds) + int(hunds) / 100)

# Round a float to two decimal places
def twoDecimalFloat(num):
  return float('{0:.2f}'.format(num))

# Round a float to four decimal places
def fourDecimalFloat(num):
  return float('{0:.4f}'.format(num))

# Round a float to six decimal places
def sixDecimalFloat(num):
  return float('{0:.6f}'.format(num))

# Returns the Excel columns for each indoor event
def getIndoorColumns():
  return [
    { 'column': 0, 'event': '60m' },
    { 'column': 4, 'event': '200m' },
    { 'column': 8, 'event': '400m' },
    { 'column': 12, 'event': '800m' },
    { 'column': 16, 'event': '1 Mile' },
    { 'column': 20, 'event': '3000m' },
    { 'column': 24, 'event': '60m HH' },
    # { 'column': 28, 'event': '4x200m' },
    { 'column': 31, 'event': '4x400m' },
    { 'column': 34, 'event': '4x800m' },
    { 'column': 37, 'event': 'LJ' },
    { 'column': 41, 'event': 'TJ' },
    { 'column': 45, 'event': 'HJ' },
    { 'column': 49, 'event': 'Shot' }
  ]

# Returns the Excel columns for each outdoor event
def getOutdoorColumns():
  return [
    { 'column': 0, 'event': '100m' },
    { 'column': 4, 'event': '200m' },
    { 'column': 8, 'event': '400m' },
    { 'column': 12, 'event': '800m' },
    { 'column': 16, 'event': '1500m' },
    { 'column': 20, 'event': '5000m' },
    { 'column': 24, 'event': '100m HH' },
    { 'column': 28, 'event': '400m HH' },
    { 'column': 32, 'event': '3000m Steeplechase' },
    { 'column': 36, 'event': '4x100m' },
    { 'column': 39, 'event': '4x400m' },
    { 'column': 42, 'event': '4x800m' },
    { 'column': 45, 'event': 'LJ' },
    { 'column': 49, 'event': 'TJ' },
    { 'column': 53, 'event': 'HJ' },
    { 'column': 57, 'event': 'Shot' },
    { 'column': 61, 'event': 'Discus' }
  ]

# Returns the weight for each meet date, with date represented as Excel value
def getDateWeights():
  return {
    42812.0 : 5,
    42798.0 : 2,
    42791.0 : 1.6,
    42784.0 : 1,
    42777.0 : 0.75,
    42770.0 : 0.5,
    42763.0 : 0.2,
    42758.0 : 0.1,
    42757.0 : 0.1,
    42756.0 : 0.1,
    42749.0 : 0.08,
    42742.0 : 0.06,
    42713.0 : 0.05,
    42707.0 : 0.01
  }

# Returns probablity distribution for modeling of all events
def getDistribution():
  distribution = [0.95] * 50 + [0.96] * 75 + [0.97] * 100 + [0.98] * 175 + [0.99] * 175
  distribution += [1.00] * 175 + [1.01] * 175 + [1.02] * 80 + [1.03] * 25 + [1.04] * 25
  distribution += [1.05] * 25 + [1.06] * 1 + [1.07] * 1 + [1.08] * 1 + [1.09] * 1
  distribution += [1.10] * 1
  distribution += [1.2] * 1
  return distribution

# Returns all events where the Excel input time is a string, not a float
def getStringEvents():
  return ['800m', '1500m', '1 Mile', '3000m', '5000m', '4x400m', '4x800m', '3000m Steeplechase']

# Returns the relay events
def getRelayEvents():
  return ['4x100m', '4x400m', '4x800m']

# Returns the distance events (these events score where higher is better)
def getDistanceEvents():
  return ['LJ', 'TJ', 'HJ', 'Shot', 'Discus']

# Returns the point scale used to score the event results
def getPointScale():
  return [10, 8, 7, 6, 5, 4, 3, 2, 1]
