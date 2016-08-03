#!/usr/local/bin/python

import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).strip()

def poll(txt):
  creating = txt
  while creating.find(txt) != -1:
    creating = cmdOut("kubectl get pods --all-namespaces")
    os.system("clear")
    print creating
    print "\nwaiting for pods ..."
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

def d(cmd):
  o("kubectl delete -f " + cmd + " --namespace spinnaker")
  time.sleep(2)

components = ('front50', 'clouddriver', 'rosco', 'orca', 'igor', 'gate', 'deck')
for component in components:
  d("applications/spinnaker/" + component + "/controller.yml")

poll("Terminating")

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


components = ('front50', 'clouddriver', 'rosco', 'orca', 'igor', 'gate', 'deck')
for component in components:
  c("applications/spinnaker/" + component + "/controller.yml")

poll("ContainerCreating")