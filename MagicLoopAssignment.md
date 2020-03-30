# Magic Loop Assignment
<p align="right">
<b> - Ashwin Jayakumar</b>
</p>

### Answers:

#### 1.
The back up link to the office sites can be configured as a secure Site-to-Site GRE/IPSec tunnel sourced from the loopback to the loopback of the endpoint with a routing overlay (any protocol like BGP,OSPF etc) configured on it as this can provide a virtual back up to the untrusted dedicated circuit over the internet. 
This would involve configuration of routing globally and on the tunnel. 
The tunnel configuration would require an IP address, logical bandwidth config,routing config,tunnel source and destination as well as applying any QOS policy-maps
The IPSec tunnel on the Endpoint routers would also require the corresponding configs on its end to establish the backup link
BFD configuration at the interface and routing protocol levels can be used to provide sub-second failure detection which provides greater resiliency and convergence time in the event of a failure. 

#### 2.
The local internet access would be a WAN connection that goes out to the service provider (MPLS cloud). BGP can be configured to peer with the PE router.  

#### 3.
The local site would follow a hierarchial architecture - Access/Distribution/Core that ties into a FW pair. The VPN termination could be on the firewall itself or a pair of border/tunnel router. These tunnel routers would peer with the MPLS clouds. 

### Bonus Answers:
#### Configuration on DC side(Cisco ASR Series Router):
```
interface Tunnel123
 description GRE tunnel to Office
 bandwidth 2048
 bandwidth qos-reference 2048
 ip address 10.20.30.40 255.255.255.252
 ip ospf message-digest-key 1 md5 ambiguity
 ip ospf network point-to-point
 ip ospf dead-interval 6
 ip ospf hello-interval 1
 ip ospf cost 48
 tunnel source Loopback1
 tunnel destination 10.20.30.41
 service-policy output MPLS
 no shut
 
 router ospf 100
 router-id 10.10.10.10
 area 1 authentication message-digest
 area 1 range 10.20.30.40 255.255.255.252

crypto isakmp policy 2
 encr aes 256
 authentication pre-share
 group 15
crypto isakmp key 6 12345 address 10.20.30.41   
crypto isakmp keepalive 10
!
!
crypto ipsec transform-set AES_ESP esp-aes 256 esp-sha-hmac 
 mode transport
!
crypto ipsec profile AES_ESP
 set security-association replay window-size 512 
 set transform-set AES_ESP 
 ```
 
 ### Office Site CE Router(Cisco ISR Series Router):
 ```
 router ospf 1
 router-id 1.1.1.1
 area 1 nssa
 passive-interface default
 no passive-interface Tunnel123
 network 10.20.30.40 0.0.0.3 area 1
!

interface Tunnel123
 description GRE OSPF tunnel to DC 
 bandwidth 2048
 bandwidth qos-reference 2048
 ip address 10.20.30.41 255.255.255.252
 ip ospf network point-to-point
 ip ospf dead-interval 6
 ip ospf hello-interval 1
 ip ospf cost 48
 tunnel source Loopback1
 tunnel destination 10.20.30.40
 tunnel protection ipsec profile AES_ESP
 service-policy output MPLS
!

crypto isakmp policy 2
 encr aes 256
 authentication pre-share
 group 15
crypto isakmp key 6 12345 address 10.20.30.40   
crypto isakmp keepalive 10
!
!
crypto ipsec transform-set AES_ESP esp-aes 256 esp-sha-hmac 
 mode transport
!
crypto ipsec profile AES_ESP
 set security-association replay window-size 512 
 set transform-set AES_ESP 
 ```
### Automation for IPSEC configuration using Ansible:
```ansible
---
- name: Office Router configuration
  hosts: xyz
  gather_facts: no

  vars:
    EP_Router_public_ip: "{{ hostvars['EP_Router'] }}"
    DC_public_ip: "{{ hostvars['DC_Router'] }}"

  tasks:
  - name: Setting up tunnel interface on Endpoint Router
  ios_config: 
	lines:
	 - description GRE tunnel to Office
	 - bandwidth 2048
	 - bandwidth qos-reference 2048
	 - ip address 10.20.30.41 255.255.255.252
	 - ip ospf message-digest-key 1 md5 ambiguity
	 - ip ospf network point-to-point
	 - ip ospf dead-interval 6
	 - ip ospf hello-interval 1
	 - ip ospf cost 48
	 - tunnel source Loopback1
	 - tunnel destination {{ DC_Router_public_ip }}
	 - service-policy output MPLS
	 - no shut
	parents: interface Tunnel123

  - name: IPSEC configuration on Endpoint Router
  ios_config:
	lines:
	- crypto isakmp policy 2
 	- encr aes 256
	- authentication pre-share
	- group 15
	- crypto isakmp key 6 12345 address {{ DC_Router_public_ip }}  
	- crypto isakmp keepalive 10
	- crypto ipsec transform-set AES_ESP esp-aes 256 esp-sha-hmac 
	- mode transport
	- crypto ipsec profile AES_ESP
	- set security-association replay window-size 512 
	- set transform-set AES_ESP 

  - name: Routing configuration
  ios_config:
  	lines:
	 -  router-id 1.1.1.1
	 - area 1 nssa
	 - passive-interface default
	 - no passive-interface Tunnel123
	 - network 10.20.30.40 0.0.0.3 area 1
	parents: router ospf 1
	
   - name: SAVE & BACKUP CONFIGURATION
     ios_config:
       authorize: yes
       save: yes
       backup: yes
```
DC router would have a similar playbook to implement the IPSEC VPN configurations
