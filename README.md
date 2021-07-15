[![Python package](https://github.com/dm-bell-networking/net_define/actions/workflows/python-package.yml/badge.svg)](https://github.com/dm-bell-networking/net_define/actions/workflows/python-package.yml)
# net_define
A declarative framework for building CLI-based network configurations

##About
Netdefine attempts to address pain points found when moving from hand-crafted CLI files to CLI templates and abstracted variable data. 

Using Netdefine, engineers can build device templates from a self-service repository of shared components. 
These components are referenced by Features, which contain the required data for each template. Each device template then becomes a list of Features that describes the configuration of the device. 

Netdefine tracks the state of each file in your configuration repository by computing a hash of the file bytes, when a file is changed, `netdefine plan` can be ran to track which devices require updates due to a change in an underlying feature or component. 

##Directory Structure
This is an example of a basic directory structure for a Netdefine project. 

The components directory stores all resubale CLI templates as J2 files. 
The Features directory contains the features written per-device, each feature references a component and provides the required data to produce the template.

The templates directory contains template files which link features together to produce a device configuration. 

```
├── components
│   ├── example-cisco_ios_baseline.j2
│   ├── example-cisco_ios_bgp.j2
│   ├── example-cisco_ios_l3_interfaces.j2
│   ├── example-cisco_ios_ospf.j2
│   └── example-cisco_ios_static_routes.j2
├── configs
│   └── first_change-config-example-cisco_ios_router_1.yml.txt
├── features
│   ├── example_router_1_baseline.yml
│   ├── example_router_1_bgp.yml
│   ├── example_router_1_interfaces.yml
│   ├── example_router_1_ospf.yml
│   └── example_router_1_static_routes.yml
├── state.json
└── templates
    └── example-cisco_ios_router_1.yml
```
By default Netdefine will create a state.json file in your project root directory and output configutation files to the configs directory. 

## Using Netdefine 
This package is in its very early stages and is not pushed to PyPi, to install netdefine, clone this repository and run the setup file after creating a virtual environment.

`python netdefine/src/setup.py`

From there, you will have access to the netdefine command. Change into the examples/globomantics directory and run `netdefine plan`

Netdefine will then create a state file to track the project folder.
```
(venv) daltonbell@Daltons-MacBook-Pro globomantics % netdefine plan
State file not found, building state...
state built successfully
The state has not changed since the last apply
```


to generate configurations, use the apply command and specify a change 
```
(venv) daltonbell@Daltons-MacBook-Pro globomantics % netdefine apply first_change
apply success for change first_change
```


to validate a change without updating state (check j2 and yaml syntax and references) use the dry_run flag
```commandline
(venv) daltonbell@Daltons-MacBook-Pro globomantics % netdefine apply first_change --dry_run
apply success for change first_change

```


to view the templates produced by change in the console, utilize the --display flag
```commandline
(venv) daltonbell@Daltons-MacBook-Pro globomantics % netdefine apply first_change \        
> --dry_run \
> --display
apply success for change first_change

Template: 
 example-cisco_ios_router_1.yml 

Config: 

hostname example-router-1
ip domain-name globomantics.net
ip name-server 10.254.0.1
ip ssh version 2
username cisco secret cisco
line vty 0 15
 login local
banner motd ^
******************************************
       THIS IS A TEST CONFIGURATION
******************************************
!
router ospf 100
  passive-interface loop0
!
router bgp 65000
 neighbor 10.255.255.2 remote-as 65000
 network 10.100.100.0 mask 255.255.255.0
!
ip route 10.100.100.0 255.255.255.0 10.255.255.3
!
interface loop0
 ip address 10.255.255.1 255.255.255.255
 ip ospf 100 area 0
 no shutdown
!
interface G0
 ip address 10.0.0.1 255.255.255.252
 ip ospf 100 area 0
 no shutdown
!
interface G1
 ip address 10.0.0.5 255.255.255.252
 ip ospf 100 area 0
 no shutdown
!
```


To target a specific template utilize the --target flag
```commandline
(venv) daltonbell@Daltons-MacBook-Pro globomantics % netdefine apply first_change \
--dry_run \
--display \
--target=example-cisco_ios_router_1.yml
apply success for change first_change

Template: 
 example-cisco_ios_router_1.yml 

Config: 

hostname example-router-1
ip domain-name globomantics.net
ip name-server 10.254.0.1
ip ssh version 2
username cisco secret cisco
line vty 0 15
 login local
banner motd ^
******************************************
       THIS IS A TEST CONFIGURATION
******************************************
!
router ospf 100
  passive-interface loop0
!
router bgp 65000
 neighbor 10.255.255.2 remote-as 65000
 network 10.100.100.0 mask 255.255.255.0
!
ip route 10.100.100.0 255.255.255.0 10.255.255.3
!
interface loop0
 ip address 10.255.255.1 255.255.255.255
 ip ospf 100 area 0
 no shutdown
!
interface G0
 ip address 10.0.0.1 255.255.255.252
 ip ospf 100 area 0
 no shutdown
!
interface G1
 ip address 10.0.0.5 255.255.255.252
 ip ospf 100 area 0
 no shutdown
!
```

##Contributing to Netdefine

Install dev requirements using `pip install - requirements.dev.txt`

Run the test suite with `pytest`

```commandline
(venv) daltonbell@Daltons-MacBook-Pro net_define % pytest                                   
====================================================================== test session starts ======================================================================
platform darwin -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/daltonbell/github-repos/net_define
plugins: cov-2.12.1
collected 12 items                                                                                                                                              

netdefine/tests/test_config_template.py .                                                                                                                 [  8%]
netdefine/tests/test_netdefine.py ...........                                                                                                             [100%]

====================================================================== 12 passed in 0.22s =======================================================================
(venv) daltonbell@Daltons-MacBook-Pro net_define % 

```