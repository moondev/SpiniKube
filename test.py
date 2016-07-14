import yaml
import os
import time
import collections
import subprocess


os.system("kubectl delete deployment front50-delay --namespace spinnaker")
os.system("kubectl delete deployment front50-delay --namespace spinnaker")
os.system("kubectl delete deployment front50-delay-secret --namespace spinnaker")
os.system("kubectl delete deployment front50-delay-secret --namespace spinnaker")

os.system("kubectl create --namespace spinnaker -f front50-stock.yml")
time.sleep(5)
os.system("kubectl create --namespace spinnaker -f front50-stock-secret.yml")
time.sleep(5)
os.system("kubectl create --namespace spinnaker -f front50-delay.yml")
time.sleep(5)
os.system("kubectl create --namespace spinnaker -f front50-delay-secret.yml")
time.sleep(5)