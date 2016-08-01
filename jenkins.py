import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()
#
#ContainerCreating
#Terminating
def poll(search):
  creating = search
  while creating.find(search) != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nworking..."
    time.sleep(2)

jenkins = cmdOut("minikube service spin-jenkins --namespace spinnaker --url")

components = ('front50', 'clouddriver', 'rosco', 'orca', 'gate', 'igor', 'deck')

for component in components:
  os.system("curl -XPOST --silent --show-error --user jenkins:jenkins " + jenkins + "/job/spinnaker-" + component + "/build " + '--data-urlencode json=\'{"parameter": [{"name":"SERVICE", "value":"' + component + '"}]}\'')
  
  done = 0
  print "Building " + component
  while done == 0:
    done = ('curl ' + jenkins + "/job/spinnaker-" + component + '/lastBuild/api/json | grep --color result\":null' )
    time.sleep(2)

