research-dashboard
==================

A simple client-sided HTML5 dashboard for monitoring key Data Research Analysis KPIs

#Usage

Navigate to http://mongo.appbackr.com:8080 for a live demo

#Deployment

## Local Machine

Bundled with isolated Python environment for testing and debugging

```
chmod a+x dashboard.py
```

```
./dashboard.py
```

## Server

Create a service manager configuration file `/etc/init/appbackrdash.conf`

```
# simple uWSGI script to start appbackr analysis dashboard

description "appbackr analysis dashboard"
start on runlevel [2345]
stop on runlevel [06]

exec uwsgi --processes 4 --die-on-term --plugins python --http-socket :8080 --wsgi-file /home/ubuntu/research-dashboard/dashboard.py --callable app
```

Start the service

```
sudo service appbackrdash start
```

#Motivations

The wheel had to be reinvented, as [Geckoboard](https://www.geckoboard.com/) does not play nice with layouting for multiple KPI reporting on small screens and awesome [Firebase](https://www.firebase.com/) which was used for real-time static analysis progress monitoring.

#About

Served by Python [Flask](http://flask.pocoo.org). Powered by [RazorFlow](https://www.razorflow.com/) Open Source HTML5 Dashboard Framework