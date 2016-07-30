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

os.system("kubectl delete namespace spinnaker")
time.sleep(10)
poll("Terminating")
time.sleep(10)
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

os.system("kubectl create secret generic spinnaker-config --from-file=./config2/echo.yml --from-file=./config2/igor.yml --from-file=./config2/gate.yml --from-file=./config2/orca.yml --from-file=./config2/rosco.yml --from-file=./config2/front50.yml --from-file=./config2/clouddriver.yml")

os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key --namespace spinnaker")

os.system("kubectl create secret generic minikube-config --from-file=./minikube/config --from-file=./minikube/ca.crt --from-file=./minikube/apiserver.crt --from-file=./minikube/apiserver.key")

os.system("kubectl create secret generic nginx-config --from-file=./nginx/nginx.conf --namespace spinnaker")

os.system("rm -rf minikube")


components = ('cassandra', 'redis', 'front50', 'clouddriver', 'rosco', 'orca', 'gate', 'jenkins', 'igor', 'registry', 'registryui', 'debweb', 'deck')

for component in components:
  os.system("kubectl create --namespace spinnaker -f sets/" + component + ".yml")
  time.sleep(1)
  os.system("kubectl create --namespace spinnaker -f services/" + component + ".json")
  time.sleep(1)

for component in components:
  os.system("kubectl delete -f services2/" + component + ".json")
  time.sleep(1)

for component in components:
  os.system("kubectl create -f services2/" + component + ".json")
  time.sleep(1)

os.system("kubectl create -f sets2/cassandra.yml")
os.system("kubectl create -f sets2/redis.yml")

os.system("kubectl create --namespace spinnaker -f sets/registry-proxy.yml")

os.system("kubectl create -f kubedash/bundle.yaml")

os.system("kubectl create -f tectonic/pull.yml")
os.system("kubectl create -f tectonic/tectonic-console.yaml")
os.system("kubectl create -f tectonic/tectonic.json")
time.sleep(10)
poll("ContainerCreating")

time.sleep(60)

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
    },
      {
    "title": "Container Image Registry",
    "description": "Local image repository",
    "link": "''' + cmdOut("minikube service spin-registryui --namespace spinnaker --url") + '''"
    },
    {
    "title": "Apt Repository",
    "description": "Local apt repository",
    "link": "''' + cmdOut("minikube service spin-debweb --namespace spinnaker --url") + '''"
    }

]
}
'''

os.system("rm -f start/services.json")

with open("start/services.json", "w") as text_file:
  text_file.write(services)

os.system("kubectl create secret generic start-config --from-file=./start/index.html --from-file=./start/services.json --namespace spinnaker")

os.system("kubectl create --namespace spinnaker -f sets/start.yml")
time.sleep(1)
os.system("kubectl create --namespace spinnaker -f services/start.json")
time.sleep(1)


poll("ContainerCreating")

#os.system('minikube service spin-start --namespace spinnaker')