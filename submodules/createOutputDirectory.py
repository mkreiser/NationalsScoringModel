import os, time

def createOutputDirectory():
  curTime = time.strftime("%Y-%m-%d----%H-%M-%S", time.localtime())
  path = 'outputs/' + str(curTime) + '/'

  os.makedirs(path, exist_ok=True)
  return path
