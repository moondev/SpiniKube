import yaml
import os
import time
import collections
import subprocess

while subprocess.check_output("kubectl get pods --all-namespaces", shell=True).find("ContainerCreating") != -1:
  print "waiting for services to start..."
  os.system("kubectl get pods --all-namespaces")
  time.sleep(2)

print "services done!"