
# #!/usr/local/bin/python

import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()

def poll():
  creating = "ContainerCreating"
  while creating.find("ContainerCreating") != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nwaiting for services to start..."
    time.sleep(2)


os.system("minikube delete")
time.sleep(5)
os.system("minikube start --memory 10000 --cpus 4 --disk-size=60g")
time.sleep(10)
poll()


os.system("python restart.py")









time.sleep(10)

poll()


os.system('minikube service spin-start --namespace spinnaker')

