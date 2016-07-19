import yaml
import os
import time
import collections
import subprocess

def cmdOut(cmd):
  return subprocess.check_output(cmd, shell=True).rstrip()

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
    "link": "''' + cmdOut("minikube service spin-deck --namespace spinnaker --url") + '''"
    },

        {
    "title": "Cluster Performace",
    "description": "Performance analytics UI",
    "link": "''' + cmdOut("minikube service kubedash --namespace kube-system --url") + '''"
    }



]
}
'''

os.system("rm -f services.json")

with open("services.json", "w") as text_file:
  text_file.write(services)