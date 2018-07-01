# ISEMS Data Collector [![Build Status](https://travis-ci.com/ISEMS/isems-data-collector.svg?branch=master)](https://travis-ci.com/ISEMS/isems-data-collector) [![codecov](https://codecov.io/gh/ISEMS/isems-data-collector/branch/master/graph/badge.svg)](https://codecov.io/gh/ISEMS/isems-data-collector)

This is the backend for ISEMS. It is a small Python app that should be deployed on a 
server (such as a raspberry pi) that is deployed in a mesh network which has solar powered nodes. 

The server will run a scheduled task every quarter hour or so and will communicate with all
solar nodes in the network. It will get their status information (such as battery percentage,
temperature etc.) and ingest it into a local database. 

It then provides an API with which users can get information about the solar-network as a whole
as well as individual notes (and their historical measurements). This API is used by the
[isems-app](https://github.com/isems/isems-app) which displays the data in a more user friendly way.


## Setup
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running
Create a virtual environment and set some environment variables:
```
export FLASK_ENV=development
export ISEMS_ROUTER_IPS="<comma-separated list of solar node ips>"
export DATABASE_URL=sqlite:////<path on your machine>
```
You can for example put these `exports` into a `.envrc` file that you source before
running the application. You can start it with `flask run`


## Updating data
The app does not automatically call the routers configured in `ISEMS_ROUTER_IPS`. This
should be triggered by a cronjob when it is deployed. You can also test it locally though
by running `flask update_data`


## Testing
```bash
pytest
```
