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
    "title": "Kubernetes Dashboard",
    "description": "Management UI",
    "link": "''' + cmdOut("minikube service kubernetes-dashboard --namespace kube-system --url") + '''"
    },

    {
    "title": "Kubedash",
    "description": "Performance analytics UI",
    "link": "''' + cmdOut("minikube service kubedash --namespace kube-system --url") + '''"
    },

    {
    "title": "Jenkins",
    "description": "Automation Server",
    "link": "''' + cmdOut("minikube service spin-deck --namespace spinnaker --url") + '''"
    },


    {
    "title": "Tectonic Console",
    "description": "Alternative management UI",
    "link": "''' + cmdOut("minikube service tectonic --url") + '''"
    },

        {
    "title": "Spinnaker",
    "description": "Spinnaker UI",
    "link": "''' + cmdOut("minikube service spin-deck --namespace spinnaker --url") + '''"
    },

            {
    "title": "Portus",
    "description": "private container registry",
    "link": "localhost"
    }

]
}
'''

os.system("rm -f services.json")

with open("services.json", "w") as text_file:
  text_file.write(services)