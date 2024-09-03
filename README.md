# Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim
The project consist of deploying a 5G network using Open5gs and Ueransim inside ComNetsEmu, where each component is a docker, talking to the others using a network with links that have bandwidth and delay.

## Tools
* Open5gs v2.7.1 Docker by Gradiant
* Open5gs-WebUI v2.7.1 Docker by Gradiant
* Ueransim v3.2.6 Docker by Gradiant
* MongoDB v7.0.1 Docker Official 
> It is provided a script to pull all the correct docker images

## Configuration of the enviroment
> My configuration was inside a VM
### VM Details
* OS: Ubuntu 20.04.6 LTS (ubuntu-20.04.6-desktop-amd64.iso)
* HyperVisor: Proxmox
> Numbers of Cores, RAM and Disk is just a reference, should work also with 4 Cores, 8 GB RAM and 20 GB Disk

| Hardware | Description |
| --- | --- |
| CPU | Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz |
| KVM hardware virtualization | Yes |
| Type | Host |
| Socket | 1 |
| Cores  | 20 |
| RAM    | 16 GB |
| DISK   | 60 GB |

### Installation of ComNetsEmu
First you need to install some dependency
```
sudo apt update && sudo apt upgrade && sudo apt install git vagrant virtualbox
```
Now clone , patch the Vagrantfile and enter comnetsemu
```
cd ~
git clone https://git.comnets.net/public-repo/comnetsemu.git
cd comnetsemu
```
You need to modify the Vagrantfile:
 * #### **OPTIONAL**
  * At line 32 you can modify the number of CPUS
   ```
    CPUS = 2
   ```
   > I use CPUS = 4 just to be sure
   * At line 36 you can modify the number of CPUS
   ```
    RAM = 4096
   ```
 * #### **TO DO IN ORDER TO HAVE ACCESS TO THE WEBUI**
 > Do it now to avoid 'vagrant reload'
  
  Add at line 204:
  ```
   comnetsemu.vm.network "forwarded_port", guest: 9999, host: 9999
  ```
Now be patient while
> Could take 15/20 min
```
vagrant up comnetsemu
vagrant ssh comnetsemu
```
### Installation of The Tool
```
cd comnetsemu
cd app
git clone https://github.com/emilianmanoleuni/Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim-or-srsRAN-5Gs.git
sudo pip install python-dotenv
```
### Installation of Docker Images
> If you get problems with docker like "permission denied check FAQ at the bottom"
```
cd utilities
./pullDockerImages.sh
```
> Open5gs WebUI images is patched in order to work in this context
How to build images:
```
cd utilities
cd build
./buildOpen5gs.sh       # For Open5gs
./buildOpen5gsWebUI.sh  # For Open5gs WebUI
./buildUeransim.sh      # For Ueransim
```
## Try the tool
```
sudo python3 basic_topology.py
```
## Ueransim Problem
## References
* [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu)
* [Open5Gs](https://open5gs.org/open5gs/docs/)
* [Gradiant](https://github.com/Gradiant/5g-images)
* [Ueransim](https://github.com/aligungr/UERANSIM)
