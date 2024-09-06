# Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim
The project consist of deploying a 5G network using Open5gs and Ueransim inside ComNetsEmu, where each component is a docker, talking to the others using a network with links that have bandwidth and delay. The challenge is to use only a custom network without the help of the predefined docker network, this means that each component will have a custom interface with a new IP.

## Network Topology
![](https://github.com/emilianmanoleuni/Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim/blob/main/images/networkTopologyWithBorders.png)


## Tools
* Open5gs v2.7.1 Docker by Gradiant
* Open5gs-WebUI v2.7.1 Docker by Gradiant
* Open5gs-dbctl v0.10.3 Tool by Gradiant
* Ueransim v3.2.6 Docker by Gradiant
* MongoDB v7.0.1 Docker Official 
> It is provided a script to pull all the correct docker images and to build the modified ones

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
  #### **OPTIONAL**
  * At line 32 you can modify the number of CPUS
   ```
    CPUS = 2
   ```
   > I use CPUS = 10 just to be sure
   * At line 36 you can modify the number of CPUS
   ```
    RAM = 4096
   ```
   > I use RAM = 8192 just to be sure

 #### **TO DO IN ORDER TO HAVE ACCESS TO THE WEBUI**
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
git clone https://github.com/emilianmanoleuni/Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim.git
cd Advanced-Deploy-in-ComNetsEmu-of-Open5gs-and-Ueransim
sudo pip install python-dotenv
```
### Installation of Docker Images
> If you get problems with docker like "permission denied check FAQ at the bottom"
```
cd build
./pullDockerImages.sh
```
Now we need to modify all images because they are missing some dependecy

```
cd mongo
./build.sh
cd ..
cd open5gs
./build.sh
cd ..
cd open5gs_webui
./build.sh
cd ..
cd ueransim
./build.sh
cd ..
cd ..
```

## Try the tool
The containers IPs:
| Container | IP |
| --- | --- |
| MONGO | 10.0.0.2 |
| AMF | 10.0.0.3 |
| AUSF | 10.0.0.4 |
| BSF | 10.0.0.5 |
| NRF | 10.0.0.6 |
| NSSF | 10.0.0.7 |
| PCF | 10.0.0.8 |
| SCP | 10.0.0.9 |
| SMF | 10.0.0.10 |
| UDM | 10.0.0.11 |
| UDR | 10.0.0.12 |
| UPF | 10.0.0.13 |
| WEBUI | 10.0.0.14 |
| GNB | 10.0.0.20 |
| UE | 10.0.0.21 |
> uesimtun IPs interfaces are above

To start the project:
```
sudo python3 startTopology.py
```
Now you have to wait a bit to let everything start.
The subscribers to Open5gs are automaticaly added.

You may get for each container an error in terminal while starting, this is becuse the interface assigned for each one is started only at final stage.
### Check if all dockers are running
```
docker ps -a

CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS          PORTS                                           NAMES
b1c9b372c624   ueransim_modified_image        "/entrypoint.sh bash…"   13 minutes ago   Up 13 minutes                                                   ue
3384345a8a0f   ueransim_modified_image        "/entrypoint.sh bash…"   14 minutes ago   Up 13 minutes                                                   gnb
eb905d5be8db   open5gs_webui_modified_image   "node server/index.j…"   14 minutes ago   Up 14 minutes   0.0.0.0:9999->9999/tcp, :::9999->9999/tcp       webui
adce3ae38a38   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes   0.0.0.0:2152->2152/tcp, :::2152->2152/tcp       upf
ec95532d30e5   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   udr
aa1a512acbe6   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   udm
639756f5c4d9   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   smf
abe7bec94df2   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   scp
0f449d709c10   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   pcf
52f88a440e9b   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   nssf
9a030a4c5106   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   nrf
68b29589ca66   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   bsf
98f5927274e9   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes                                                   ausf
489e45081cd6   open5gs_modified_image         "/entrypoint.sh bash…"   14 minutes ago   Up 14 minutes   0.0.0.0:38412->38412/tcp, :::38412->38412/tcp   amf
d76f56c1c4df   mongo_modified_image           "docker-entrypoint.s…"   14 minutes ago   Up 14 minutes   27017/tcp                                       mongo
```
To check the log of a single docker
```
docker logs <name>
EXAMPLE:
docker logs amf

09/05 16:34:01.365: [gmm] INFO: [imsi-001010000000004] Registration complete (../src/amf/gmm-sm.c:2313)
09/05 16:34:01.365: [amf] INFO: [imsi-001010000000004] Configuration update command (../src/amf/nas-path.c:591)
09/05 16:34:01.365: [gmm] INFO:     UTC [2024-09-05T16:34:01] Timezone[0]/DST[0] (../src/amf/gmm-build.c:558)
09/05 16:34:01.365: [gmm] INFO:     LOCAL [2024-09-05T16:34:01] Timezone[0]/DST[0] (../src/amf/gmm-build.c:563)
09/05 16:34:01.366: [amf] INFO: [Added] Number of AMF-Sessions is now 5 (../src/amf/context.c:2683)
09/05 16:34:01.366: [gmm] INFO: UE SUPI[imsi-001010000000004] DNN[internet] S_NSSAI[SST:1 SD:0xffffff] smContextRef[NULL] smContextResourceURI[NULL] (../src/amf/gmm-handler.c:1285)
09/05 16:34:01.367: [gmm] INFO: SMF Instance [9078f848-6ba4-41ef-96c1-5179374a2e0a] (../src/amf/gmm-handler.c:1326)
09/05 16:34:01.514: [amf] INFO: [imsi-001010000000005:1:11][0:0:NULL] /nsmf-pdusession/v1/sm-contexts/{smContextRef}/modify (../src/amf/nsmf-handler.c:915)
09/05 16:34:01.528: [amf] INFO: [imsi-001010000000001:1:11][0:0:NULL] /nsmf-pdusession/v1/sm-contexts/{smContextRef}/modify (../src/amf/nsmf-handler.c:915)
09/05 16:34:01.560: [amf] INFO: [imsi-001010000000003:1:11][0:0:NULL] /nsmf-pdusession/v1/sm-contexts/{smContextRef}/modify (../src/amf/nsmf-handler.c:915)
09/05 16:34:01.697: [amf] INFO: [imsi-001010000000002:1:11][0:0:NULL] /nsmf-pdusession/v1/sm-contexts/{smContextRef}/modify (../src/amf/nsmf-handler.c:915)
09/05 16:34:01.790: [amf] INFO: [imsi-001010000000004:1:11][0:0:NULL] /nsmf-pdusession/v1/sm-contexts/{smContextRef}/modify (../src/amf/nsmf-handler.c:915)
```
When you get the above log from the amf everything should be working.

### Check the WebUI
Depending on the configuration that you are running there are 2 ways:
* Running inside a remote vm:
  Go to the browser and access
  ```
  http://<VM_IP>:9999/
  ```
* Running on the host:
  ```
  http://localhost:9999/
  ```
   Credentials:
   * Username: admin 
   * Password:  1423

> WebUI could be useful to check the imsi registered and the configuration of each one, but it seams that modifying something actually isn't applied if the amf isn't restarted.

### Testing
To test enter in ue docker
  ```
  ./enter_container.sh ue
  ```
To check if uesimtun were created
  ```
  ifconfig

  uesimtun0: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.2  netmask 255.255.255.255  destination 10.45.0.2
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 392  bytes 23691 (23.6 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 704  bytes 954441 (954.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   uesimtun1: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.3  netmask 255.255.255.255  destination 10.45.0.3
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 2428  bytes 142577 (142.5 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3676  bytes 5103746 (5.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   uesimtun2: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.4  netmask 255.255.255.255  destination 10.45.0.4
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 2978  bytes 175809 (175.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4439  bytes 6174644 (6.1 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   uesimtun3: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.5  netmask 255.255.255.255  destination 10.45.0.5
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 3031  bytes 176831 (176.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5039  bytes 7014644 (7.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

   uesimtun4: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.6  netmask 255.255.255.255  destination 10.45.0.6
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 933  bytes 54773 (54.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1718  bytes 2373332 (2.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
  ```
  Now by using one of them ping google.it
  ```
  ping -I uesimtun3 google.it
  ```
  The 5 ue-s have different Session-AMBR Downlink and Session-AMBR Uplink
  ```
  iperf3 -c 10.45.0.1 -B 10.45.0.2 -t 5
  iperf3 -c 10.45.0.1 -B 10.45.0.3 -t 5
  iperf3 -c 10.45.0.1 -B 10.45.0.4 -t 5
  iperf3 -c 10.45.0.1 -B 10.45.0.5 -t 5
  iperf3 -c 10.45.0.1 -B 10.45.0.6 -t 5
  ```
  The interface is assigned "first-served" imsi, infact the script registering them modify the speed based on imsi and doesn't follow uesintun numeration.
  | Interface | IP | Downlink | Uplink |
  | --- | --- | --- | --- |
  | uesimtun0 | 10.45.0.2 | 1 Mbits | 1 Mbits |
  | uesimtun1 | 10.45.0.3 | 10 Mbits | 10 Mbits |
  | uesimtun2 | 10.45.0.4 | 10 Mbits | 10 Mbits |
  | uesimtun3 | 10.45.0.5 | 10 Mbits | 10 Mbits |
  | uesimtun4 | 10.45.0.6 | 3 Mbits | 3 Mbits |
  > In my case
  
  This script is using open5gs-dbctl tool which allow easily to register and modify the subscribers to mongodb. As the WebUI the modification aren't applied until restart of the amf container.
  ```
  /mongo/config/register_subscriber.sh
  ```
  

## How to increase UE-s
There are 2 steps:
  ```
  cd /ueransim/scripts/
  nano init_ue.sh
  ```
At last line change to the number you whant to deploy
 ```
./entrypoint.sh ue -n 5
 ```
Now you need to create the profile for the new subscriptions
  ```
  cd /mongo/config/
  nano register_subscribers.sh
  ```
  To add new one
  ```
  ./opt/mongo/open5gs-dbctl add <imsi> 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
  ```
  To modify the Session-AMBR Downlink and Session-AMBR Uplink
   ```
   ./opt/mongo/open5gs-dbctl ambr_speed <imsi> <downlink> <[0=bps 1=Kbps 2=Mbps 3=Gbps 4=Tbps ]> <uplink> <[0=bps 1=Kbps 2=Mbps 3=Gbps 4=Tbps ]>
   ```
## FAQ
* Docker "permission denied"
  If you have problems with docker pulling and running images because and error like "permission denied" there is a script that may help:
  ```
  /utilities/dockerFix.sh
  ```

## References
* [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu)
* [Open5Gs](https://open5gs.org/open5gs/docs/)
* [Gradiant](https://github.com/Gradiant/5g-images)
* [Ueransim](https://github.com/aligungr/UERANSIM)
