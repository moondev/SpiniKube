
#!/usr/local/bin/python

import yaml
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
os.system("minikube start --memory 4000 --cpus 2")
time.sleep(10)
poll()




os.system("kubectl create namespace spinnaker")

os.system("rm minikube/apiserver.crt")
os.system("rm minikube/apiserver.key")
os.system("rm minikube/ca.crt")




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

os.system("kubectl create -f kubedash/bundle.yaml")

os.system("kubectl create -f tectonic/pull.yml")
os.system("kubectl create -f tectonic/tectonic-console.yaml")
os.system("kubectl create -f tectonic/tectonic.json")

time.sleep(5)

os.system("kubectl create -f sets/deck.yml --namespace spinnaker")
os.system("kubectl expose deployment spin-deck --namespace spinnaker --type=NodePort")

services = '''
{
"services" : [

          {
    "title": "Spinnaker Dashboard",
    "description": "Spinnaker UI",
    "link": "''' + cmdOut("minikube service spin-deck --namespace spinnaker --url") + '''"
    },

    {
    "title": "Kubernetes Dashboard",
    "description": "Management UI",
    "link": "''' + cmdOut("minikube service kubernetes-dashboard --namespace kube-system --url") + '''"
    },

        {
    "title": "Tectonic Console",
    "description": "Alternative management UI",
    "link": "''' + cmdOut("minikube service tectonic --url") + '''"
    },


    {
    "title": "Jenkins",
    "description": "Automation Server",
    "link": "''' + cmdOut("minikube service spin-jenkins --namespace spinnaker --url") + '''"
    },

        {
    "title": "Cluster Performace",
    "description": "Performance analytics UI",
    "link": "''' + cmdOut("minikube service kubedash --namespace kube-system --url") + '''"
    }



]
}
'''

os.system("rm -f panel/services.json")

with open("panel/services.json", "w") as text_file:
  text_file.write(services)

os.system("kubectl create secret generic panel-config --from-file=./panel/index.html --from-file=./panel/services.json --namespace spinnaker")

os.system("kubectl create --namespace spinnaker -f sets/panel.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/panel.json")
time.sleep(1)

poll()


os.system('minikube service spin-panel --namespace spinnaker')

