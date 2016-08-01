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
  os.system("kubectl create -f yaml/" + component + ".yml")
  time.sleep(1)

