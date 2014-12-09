research-dashboard
==================

A simple middleware to interface [Geckoboard](https://www.geckoboard.com/) with [Firebase](https://www.firebase.com/) for reporting of key Data Research Analysis KPIs

#Deployment

Create a service manager configuration file `/etc/init/appbackrdash.conf`

```
description "appbackr analysis dashboard middleware"
start on runlevel [2345]
stop on runlevel [06]

exec python /home/ubuntu/research-dashboard/geckoboard-firebase-interface/dashboard.py
```

Start the service

```
sudo service appbackrdash start
```

#Motivations

[Geckoboard](https://www.geckoboard.com/)'s push interface is not immediately compatible with [Firebase](https://www.firebase.com/) which was used for real-time static analysis progress monitoring. This middleware serves to bridge the gap by receiving and restructuring KPIs from Firebase to Geckoboard.

#About

Requires [Boto](http://boto.readthedocs.org) for AWS integration, [Firebasin](https://github.com/abeisgreat/python-firebasin) for Firebase in Python