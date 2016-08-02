import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()


jenkins = cmdOut("minikube service spin-jenkins --namespace spinnaker --url")

components = ('front50', 'clouddriver', 'rosco', 'orca', 'gate', 'igor', 'deck')

for component in components:
  os.system("curl -XPOST --silent --show-error --user jenkins:jenkins " + jenkins + "/job/spinnaker-" + component + "/build " + '--data-urlencode json=\'{"parameter": [{"name":"SERVICE", "value":"' + component + '"}]}\'')
  
  done = False
  print "Building " + component
  while done == False:
    result = cmdOut('curl --silent ' + jenkins + "/job/spinnaker-" + component + '/lastBuild/api/json')
    if result.find('"result":null') != -1:
      done = True
    else:
      done = False
    time.sleep(2)

#os.system('minikube service spin-start --namespace spinnaker')

components = ('cassandra', 'redis', 'front50', 'clouddriver', 'rosco', 'orca', 'gate', 'igor', 'deck')