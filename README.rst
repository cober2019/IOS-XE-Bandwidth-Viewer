.. image:: https://travis-ci.com/cober2019/IOS-XE-Bandwidth-Viewer.svg?branch=main
    :target: https://travis-ci.com/cober2019/IOS-XE-Bandwidth-Viewer
.. image:: https://img.shields.io/badge/NETCONF-required-blue
    :target: -
.. image:: https://img.shields.io/badge/IOS--XE-required-blue
    :target: -
    
Bandwidth Viewer
-----------------

Bandwidth Viewer enables you to view bandwidth usage on devices as well as CPU usage for a device. It uses bot NETCONF-YANG and SNMP to collect data and Javascript to 
present data in live graph views.

SNMP OID:
  - 1.3.6.1.4.1.9.2.1.56.0

YANG Model(s):
  - ietf-interfaces.yang
  - Cisco-IOS-XE-native.yang


**Device Login:**
==================
  - Use URL http://{**your_local_ip**}:5000/
  
.. image:: https://github.com/cober2019/IOS-XE-Bandwidth-Viewer/blob/main/images/Login.PNG
    :target: -
    
**Index/Home Page:**
=====================

  - Select dropdown action button for viewing interface badnwidth or interface details (CLI View of interface.) <- Cisco IOS-XE

.. image:: https://github.com/cober2019/IOS-XE-Bandwidth-Viewer/blob/main/images/Index.PNG
    :target: -

.. image:: https://github.com/cober2019/IOS-XE-Bandwidth-Viewer/blob/main/images/InterfaceDetails.PNG
    :target: -
    
**Live Charts --> (REQUIRES BROWSER POP-UPS):**
================================================

  - All data should reflect positive numbers. If a -1 is returned it means that there was a error in calculation
  - If graph shows '0' it means there wasn't a difference in packet in/out in the polling period (15 Seconds)

.. image:: https://github.com/cober2019/IOS-XE-Bandwidth-Viewer/blob/main/images/Bandwidth.PNG
    :target: -

