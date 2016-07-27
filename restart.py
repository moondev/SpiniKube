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

os.system("kubectl delete namespace spinnaker")

time.sleep(60)

os.system("kubectl create namespace spinnaker")

os.system("rm -rf minikube")
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

os.system("kubectl create secret generic spinnaker-config --from-file=./config/echo.yml --from-file=./config/igor.yml --from-file=./config/gate.yml --from-file=./config/orca.yml --from-file=./config/rosco.yml --from-file=./config/front50.yml --from-file=./config/clouddriver.yml --namespace spinnaker")

os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")

os.system("kubectl create secret generic nginx-config --from-file=./nginx/nginx.conf --namespace spinnaker")

os.system("rm -rf minikube")


components = ('cassandra', 'redis', 'front50' 'clouddriver', 'rosco', 'orca', 'gate')

os.system("kubectl create --namespace spinnaker -f sets/cassandra.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/cassandra.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/redis.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/redis.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/front50.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/front50.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/clouddriver.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/clouddriver.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/rosco.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/rosco.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/orca.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/orca.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/gate.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/gate.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/jenkins.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/jenkins.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/igor.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/igor.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/registry.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/registry.json")
time.sleep(1)

os.system("kubectl create --namespace spinnaker -f sets/registryui.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/registryui.json")
time.sleep(1)

time.sleep(5)

os.system("kubectl create -f sets/deck.yml --namespace spinnaker")
os.system("kubectl expose deployment spin-deck --namespace spinnaker --type=NodePort")

os.system("kubectl create --namespace spinnaker -f sets/registry-proxy.yml")





poll()

#os.system("minikube dashboard")


#mount -t vboxsf hosthome /hosthome