import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()


#jenkins = cmdOut("minikube service spin-jenkins --namespace spinnaker --url")

components = ('front50', 'clouddriver', 'rosco', 'orca', 'gate', 'igor', 'deck')


for component in components:
  os.system("curl -XPOST --silent --show-error --user jenkins:jenkins " + jenkins + "/job/spinnaker-" + component + "/build " + '--data-urlencode json=\'{"parameter": [{"name":"SERVICE", "value":"' + component + '"}]}\'')
  
  done = False
  print "Building " + component
  while done == False:
    result = ('curl ' + jenkins + "/job/spinnaker-" + component + '/lastBuild/api/json | grep --color result\":null' )
    if result.find('"building":true,') != -1:
      done = False
    else:
      done = True
    time.sleep(60*10)

for component in components:
  #os.system("kubectl create -f yaml/" + component + ".yml")
  os.system("kubectl create -f services2/" + component + ".json")