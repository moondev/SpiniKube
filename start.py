import yaml
import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True)

def poll():
  creating = "ContainerCreating"
  while creating).find("ContainerCreating") != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nwaiting for services to start..."
    time.sleep(2)


os.system("minikube delete")
os.system("minikube start --memory 8000 --cpus 4")
time.sleep(10)
poll()
os.system("kubectl create namespace spinnaker")
time.sleep(1)

os.system("kubectl create secret generic spinnaker-config --from-file=./config/front50.yml --namespace spinnaker")

os.system("kubectl create --namespace spinnaker -f cassandra.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f cassandra-service.json")

os.system("kubectl create --namespace spinnaker -f spin-front50.yml")
poll()

os.system("minikube dashboard")

