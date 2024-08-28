# Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim-or-srsRAN-5Gs
The project consist of deploying a 5G network using Open5gs and Ueransim/srsRAN-5Gs inside ComNetsEmu, where each component is a docker.

## Configuration of the enviroment
### VM Details
* OS: Ubuntu 22.04.4 LTS
  
| Hardware | Description |
| --- | --- |
| CPU | Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz |
| Type | Host |
| Socket | 1 |
| Cores  | 20 |
| RAM    | 20 GB |
| DISK   | 60 GB |

### Installation of ComNetsEmu
First you need to install some dependency
```
apt
```
Now clone and enter comnetsemu
```
cd ~
git clone https://git.comnets.net/public-repo/comnetsemu.git
vagrant up comnetsemu
vagrant ssh comnetsemu
```
