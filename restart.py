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



os.system("kubectl delete secret spinnaker-config --namespace=spinnaker")
os.system("kubectl delete secret minikube-config --namespace=spinnaker")
os.system("kubectl delete secret nginx-config --namespace=spinnaker")

os.system("kubectl create secret generic spinnaker-config --from-file=./config/gate.yml --from-file=./config/orca.yml --from-file=./config/rosco.yml --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")


os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")

os.system("kubectl create secret generic nginx-config --from-file=./config/nginx.conf --namespace spinnaker")

os.system("kubectl delete deployment spin-front50 --namespace=spinnaker")
os.system("kubectl delete deployment spin-clouddriver --namespace=spinnaker")
os.system("kubectl delete deployment spin-rosco --namespace=spinnaker")
os.system("kubectl delete deployment spin-orca --namespace=spinnaker")
os.system("kubectl delete deployment spin-gate --namespace=spinnaker")

os.system("kubectl delete service spin-front50 --namespace=spinnaker")
os.system("kubectl delete service spin-clouddriver --namespace=spinnaker")
os.system("kubectl delete service spin-rosco --namespace=spinnaker")
os.system("kubectl delete service spin-orca --namespace=spinnaker")
os.system("kubectl delete service spin-gate --namespace=spinnaker")



os.system("kubectl create --namespace spinnaker -f sets/front50.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/front50.json")

os.system("kubectl create --namespace spinnaker -f sets/clouddriver.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/clouddriver.json")

os.system("kubectl create --namespace spinnaker -f sets/rosco.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/rosco.json")

os.system("kubectl create --namespace spinnaker -f sets/orca.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/orca.json")

os.system("kubectl create --namespace spinnaker -f sets/gate.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/gate.json")



poll()

#os.system("minikube dashboard")


#mount -t vboxsf hosthome /hosthome