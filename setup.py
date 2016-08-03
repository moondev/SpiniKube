#!/usr/local/bin/python

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
    print "\nwaiting for pods to start..."
    time.sleep(2)

def o(cmd):
  print "Running: " + cmd
  os.system(cmd)
  time.sleep(2)

def k(cmd):
  o("kubectl " + cmd + " --namespace spinnaker")
  time.sleep(2)

def c(cmd):
  o("kubectl create -f " + cmd + " --namespace spinnaker")
  time.sleep(2)

o("minikube delete")

o("minikube start --memory 10000 --cpus 4 --disk-size=60g")

#o("kubectl delete namespace spinnaker")
#time.sleep(30)
o("kubectl create namespace spinnaker")

c("applications/kubedash/bundle.yaml")

c("applications/tectonic/pull.yml")
c("applications/tectonic/tectonic-console.yaml")
c("applications/tectonic/tectonic.json")

components = ('jenkins', 'registry', 'registryui', 'debweb')
for component in components:
  c("applications/" + component + "/deployment.yml")
  c("applications/" + component + "/service.json")

c("applications/kubeproxy/pod.yml")

components = ('cassandra', 'redis')
for component in components:
  c("applications/spinnaker/" + component + "/deployment.yml")
  c("applications/spinnaker/" + component + "/service.json")

poll()

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

os.system("rm -rf minikube")

#print "seeding spinnaking images"
o("./podexec jenkins /usr/local/jenkins/jobs/seed.sh")

components = ('front50', 'clouddriver', 'rosco', 'orca', 'igor', 'gate', 'deck')
for component in components:
  c("applications/spinnaker/" + component + "/controller.yml")
  c("applications/spinnaker/" + component + "/service.json")

poll()

time.sleep(2)

services = '''
{
"services" : [

          {
    "title": "Spinnaker Dashboard",
    "description": "Spinnaker UI",
    "link": "''' + cmdOut("minikube service spinnaker-deck --namespace spinnaker --url") + '''"
    },



    {
    "title": "Kubernetes Dashboard",
    "description": "Management UI",
    "link": "''' + cmdOut("minikube service kubernetes-dashboard --namespace kube-system --url") + '''"
    },

        {
    "title": "Tectonic Console",
    "description": "Alternative management UI",
    "link": "''' + cmdOut("minikube service tectonic --namespace spinnaker --url") + '''"
    },


    {
    "title": "Jenkins",
    "description": "Automation Server",
    "link": "''' + cmdOut("minikube service spinnaker-jenkins --namespace spinnaker --url") + '''"
    },

        {
    "title": "Cluster Performace",
    "description": "Performance analytics UI",
    "link": "''' + cmdOut("minikube service kubedash --namespace spinnaker --url") + '''"
    },
      {
    "title": "Container Image Registry",
    "description": "Local image repository",
    "link": "''' + cmdOut("minikube service spinnaker-registryui --namespace spinnaker --url") + '''"
    },
    {
    "title": "Apt Repository",
    "description": "Local apt repository",
    "link": "''' + cmdOut("minikube service spinnaker-debweb --namespace spinnaker --url") + '''"
    }

]
}
'''

os.system("rm -f applications/start/services.json")

with open("applications/start/services.json", "w") as text_file:
  text_file.write(services)

os.system("kubectl create secret generic start-config --from-file=./applications/start/index.html --from-file=./applications/start/services.json --namespace spinnaker")

#cqlsh -e "COPY front50.pipeline TO '/front50.pipeline.csv' WITH HEADER = 'true'"

c("applications/start/deployment.yml")
c("applications/start/service.json")

poll()

#add example pipeline
o("./podexec spinnaker apt-get update")
o("./podexec spinnaker apt-get install -y git")
o("./podexec spinnaker git clone git@github.com:moondev/SpiniKube.git /SpiniKube")
o("./podexec spinnaker apt-get install -y cqlsh -e 'COPY front50.pipeline FROM \'/SpiniKube/pipelines/pipelines.csv\' WITH HEADER = \'true\';'")

o("minikube service spinnaker-start -n spinnaker")