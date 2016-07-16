import yaml
import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True)

def poll():
  creating = "ContainerCreating"
  while creating.find("ContainerCreating") != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nwaiting for services to start..."
    time.sleep(2)


os.system("minikube delete")
os.system("minikube start --memory 8000 --cpus 2")
time.sleep(10)
poll()
os.system("kubectl create namespace spinnaker")

os.system("rm -f minikube")
os.system("mkdir minikube")

ip = os.popen('minikube ip').read().strip()

os.system("cp ~/.kube/config minikube/config2")

with open("minikube/config3", "wt") as fout:
    with open("minikube/config2", "rt") as fin:
        for line in fin:
            fout.write(line.replace('/home/chad', '/root'))

with open("minikube/config", "wt") as fout:
    with open("minikube/config3", "rt") as fin:
        for line in fin:
            fout.write(line.replace('.minikube', '.kube'))

time.sleep(1)

os.system("kubectl create secret generic spinnaker-config --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")



os.system("cp ~/.minikube/apiserver.crt minikube/apiserver.crt")
os.system("cp ~/.minikube/apiserver.key minikube/apiserver.key")
os.system("cp ~/.minikube/ca.crt minikube/ca.crt")

os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")



os.system("kubectl create --namespace spinnaker -f sets/cassandra.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/cassandra.json")

os.system("kubectl create --namespace spinnaker -f sets/redis.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/redis.json")

os.system("kubectl create --namespace spinnaker -f sets/front50.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/front50.json")

os.system("kubectl create --namespace spinnaker -f sets/clouddriver.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/clouddriver.json")
poll()

os.system("minikube dashboard")

