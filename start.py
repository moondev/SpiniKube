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
time.sleep(5)
os.system("minikube start --memory 8000 --cpus 2")
time.sleep(10)
poll()
os.system("kubectl create namespace spinnaker")

os.system("rm minikube/apiserver.crt")
os.system("rm minikube/apiserver.key")
os.system("rm minikube/ca.crt")



os.system("rm -f minikube")
os.system("mkdir minikube")
os.system("cp ~/.minikube/apiserver.crt minikube/apiserver.crt")
os.system("cp ~/.minikube/apiserver.key minikube/apiserver.key")
os.system("cp ~/.minikube/ca.crt minikube/ca.crt")

ip = os.popen('minikube ip').read().strip()

kubeConfig = """
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /root/.kube/ca.crt
    server: https://""" + ip + """:8443
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

os.system("kubectl create secret generic spinnaker-config --from-file=./config/gate.yml --from-file=./config/orca.yml --from-file=./config/rosco.yml --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")





os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")

os.system("kubectl create secret generic nginx-config --from-file=./config/nginx.conf --namespace spinnaker")


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

os.system("kubectl create --namespace spinnaker -f sets/rosco.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/rosco.json")

os.system("kubectl create --namespace spinnaker -f sets/orca.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/orca.json")

os.system("kubectl create --namespace spinnaker -f sets/gate.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/gate.json")

#os.system("minikube ssh 'sudo mount -t vboxsf hosthome /hosthome''")

os.system("kubectl create --namespace spinnaker -f sets/deck.yml")
time.sleep(1)
os.system('kubectl expose deployment spin-deck --namespace spinnaker --type=NodePort')


poll()

os.system("minikube dashboard")



time.sleep(10)

os.system('minikube service spin-deck --namespace spinnaker')


os.system("kubectl create -f kubedash/bundle.yaml")
os.system("kubectl create -f heapster/kube-config/influxdb/")
os.system('minikube service kubedash --namespace kube-system')
#mount -t vboxsf hosthome /hosthome