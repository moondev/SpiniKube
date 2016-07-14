import yaml
import os
import time
import collections
import subprocess


##############
os.system("minikube delete")
time.sleep(5)
os.system("minikube start --memory 6000 --cpus 4")
#############

###############
#while True:
#  os.system("kubectl get pods --all-namespaces")
#  time.sleep(3)
##############


time.sleep(60)




##################
#os.system("kubectl delete --namespace spinnaker -f cassandra.yml")
#time.sleep(10)
#os.system("kubectl delete --namespace spinnaker -f front50.yml")
#time.sleep(10)
#os.system("kubectl delete namespace spinnaker")
#time.sleep(5)
#####################




###################
os.system("kubectl create namespace spinnaker")
time.sleep(5)
os.system("kubectl create --namespace spinnaker -f cassandra.yml")
time.sleep(10)
os.system("kubectl expose deployment cassandra --namespace spinnaker --type=NodePort")
########################

#os.system("kubectl run front50 --image=quay.io/spinnaker/front50 --namespace spinnaker --port=8080")

########
#os.system("kubectl delete secret front50cfg --namespace spinnaker")
###########



os.system("kubectl create secret generic front50cfg --from-file=./config/front50.yml --namespace spinnaker")
#time.sleep(5)



os.system("kubectl create --namespace spinnaker -f front50.yml")
os.system("kubectl create --namespace spinnaker -f front50-delay.yml")

#kubectl get pods --all-namespaces --output json

#os.system("minikube dashboard")

     #   command:
     #   - "/bin/bash -c 'sleep 5; /opt/front50/bin/front50'"