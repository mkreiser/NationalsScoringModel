import re

def printDuration(string, startTime, endTime):
  print(string, endTime - startTime)

def convertStrTimeToFloat(inputTime):
  minutes, seconds, hunds = re.split('[:.]+', inputTime)
  return (int(minutes) * 60 + int(seconds) + int(hunds) / 100)

def twoDecimalFloat(num):
  return float('{0:.2f}'.format(num))

def fourDecimalFloat(num):
  return float('{0:.4f}'.format(num))

def sixDecimalFloat(num):
  return float('{0:.6f}'.format(num))

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

def getOutdoorColumns():
  return [
    { 'column': 0, 'event': '100m' },
    { 'column': 4, 'event': '200m' },
    { 'column': 8, 'event': '400m' },
    { 'column': 12, 'event': '800m' },
    { 'column': 16, 'event': '1500m' },
    { 'column': 20, 'event': '5000m' },
    { 'column': 24, 'event': '100m HH' },
    { 'column': 28, 'event': '3000m Steeplechase' },
    { 'column': 32, 'event': '4x100m' },
    { 'column': 35, 'event': '4x400m' },
    { 'column': 38, 'event': '4x800m' },
    { 'column': 41, 'event': 'LJ' },
    { 'column': 45, 'event': 'TJ' },
    { 'column': 49, 'event': 'HJ' },
    { 'column': 53, 'event': 'Shot' },
    { 'column': 57, 'event': 'Discus' }
  ]

def getDateWeights():
  return {
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

def getDistribution():
  distribution = [0.95] * 20 + [0.96] * 25 + [0.97] * 30 + [0.98] * 25 + [0.99] * 20
  distribution += [1.00] * 16 + [1.01] * 16 + [1.02] * 16 + [1.03] * 10 + [1.04] * 10
  distribution += [1.05] * 10 + [1.06] * 1 + [1.07] * 1 + [1.08] * 1 + [1.09] * 1
  distribution += [1.10] * 1
  distribution += [1.2] * 1
  return distribution

def getStringEvents():
  return ['800m', '1500m', '1 Mile', '3000m', '5000m', '4x400m', '4x800m', '3000m Steeplechase']

def getRelayEvents():
  return ['4x100m', '4x400m', '4x800m']

def getDistanceEvents():
  return ['LJ', 'TJ', 'HJ', 'Shot', 'Discus']

def getPointScale():
  return [10, 8, 7, 6, 5, 4, 3, 2, 1]
