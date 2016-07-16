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
os.system("minikube start --memory 8000 --cpus 4")
time.sleep(10)
poll()
os.system("kubectl create namespace spinnaker")

os.system("rm -f minikube")
os.system("mkdir minikube")

ip = os.popen('minikube ip').read().rstrip()

kubeConfig = """\
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /root/.kube/apiserver.crt
    server: https://""" + ip + """:443
  name: minikube
contexts:
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
preferences: {}
users:
- name: minikube
  user:
    client-certificate: /root/.kube/apiserver.crt
    client-key: /root/.kube/apiserver.key
"""

with open("minikube/config", "w") as text_file:
  text_file.write(kubeConfig)



time.sleep(1)

os.system("kubectl create secret generic spinnaker-config --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")



os.system("cp ~/.minikube/apiserver.crt minikube/apiserver.crt")
os.system("cp ~/.minikube/apiserver.key minikube/apiserver.key")

os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")



os.system("kubectl create --namespace spinnaker -f cassandra.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f cassandra-service.json")

os.system("kubectl create --namespace spinnaker -f redis.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f redis-service.json")

os.system("kubectl create --namespace spinnaker -f spin-front50.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f front50-service.json")

os.system("kubectl create --namespace spinnaker -f spin-clouddriver.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f clouddriver-service.json")
poll()

os.system("minikube dashboard")

