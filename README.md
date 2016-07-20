# SpiniKube = Spinnaker + MiniKube
SpiniKube is a set of scripts and configurations that makes it easy to launch a local kubernetes cluster with Spinnaker and other tools installed.

## Initial Setup Instructions

### Ensure dependencies are installed

#### 1. Download the [`kubectl`](http://kubernetes.io/docs/user-guide/kubectl-overview/) utility and move it into your `PATH`

```
### OSX
curl -O https://storage.googleapis.com/kubernetes-release/release/v1.3.0/bin/darwin/amd64/kubectl && chmod +x kubectl && mv kubectl /usr/local/bin/kubectl

### Linux
curl -O https://storage.googleapis.com/kubernetes-release/release/v1.3.0/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl /usr/local/bin/kubectl

```

#### 2. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

```
### OSX
wget http://download.virtualbox.org/virtualbox/5.1.0/VirtualBox-5.1.0-108711-OSX.dmg
hdiutil mount VirtualBox-5.1.0-108711-OSX.dmg
sudo installer -pkg /Volumes/VirtualBox/VirtualBox.pkg -target /

### LINUX
sudo apt-get install virtualbox 
```

### 3. Install [minikube](https://github.com/kubernetes/minikube)

```
### OSX
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.6.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

### Linux
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.6.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

## Install and start SpiniKube
```
git clone https://github.com/moondev/SpiniKube.git && cd SpiniKube
python start.py
```

This process takes about 10 to 20 minutes depending on your internet connection.

The terminal will show the live status of each component as it is created and launched.

Once complete a brower will launch with the SpiniKube start page with handy links to each application as well as a tutorial for an example Spinnaker pipeline. This documentatin can also be found [here](start/).

## Stopping and restarting
`start.py` is only for initial setup. You can stop and start minikube from any directory with `minikube stop` and `minikube start`