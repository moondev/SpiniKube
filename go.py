import yaml
import os
import time
import collections
import subprocess


def checkStatus(command, term):
  portOpen = False
  while portOpen == False:
    result = subprocess.check_output(command, shell=True)
    if term in result:
      print "waiting..."
      time.sleep(2)
    else:
      portOpen = True

os.system("minikube delete")
os.system("minikube start --memory 4000 --cpus 4")

checkStatus("kubectl get pods --namespace kube-system", "0/1")

#os.system("kubectl delete --namespace spinnaker -f cassandra.yml")
#time.sleep(10)
#os.system("kubectl delete --namespace spinnaker -f front50.yml")
#time.sleep(10)
#os.system("kubectl delete namespace spinnaker")
#time.sleep(5)
os.system("kubectl create namespace spinnaker")
#time.sleep(5)
os.system("kubectl create --namespace spinnaker -f cassandra.yml")
#time.sleep(10)
os.system("kubectl expose deployment cassandra --namespace spinnaker --type=NodePort")
#time.sleep(30)
#os.system("kubectl delete secret front50cfg --namespace spinnaker")
#os.system("kubectl create secret generic front50cfg --from-file=./config/front50.yml --namespace spinnaker")
#time.sleep(5)
os.system("kubectl create --namespace spinnaker -f front50.yml")



os.system("minikube dashboard")