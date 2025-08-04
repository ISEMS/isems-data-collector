# ISEMS Data Collector [![Build Status](https://travis-ci.com/ISEMS/isems-data-collector.svg?branch=master)](https://travis-ci.com/ISEMS/isems-data-collector) [![codecov](https://codecov.io/gh/ISEMS/isems-data-collector/branch/master/graph/badge.svg)](https://codecov.io/gh/ISEMS/isems-data-collector)


> [!IMPORTANT]
> This project (the backend, along with the [frontend](https://github.com/isems/isems-app)) is no
> longer being maintained and therefore marked as archived. The hardware part of the project lives on though. You
> can find more information on the project (along with an alternative data tarnsport mechanism via MQTT)
> on the website [isems.de](https://www.isems.de).

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
There are two ways in which the app can look for data. It can either manually
call a set of predefined node IP-addresses to collect information from them, or it 
can subscribe to a central MQTT broker to which all the nodes send their data.

### Option 1: isems-data-collector talks to nodes directly
If you want the data-collector to talk to the individual nodes, you should configure
the `ISEMS_ROUTER_IPS` environment variable to a comma separated list of IP addresses.
You can then trigger an import by calling `flask update-data` from the repository root.
Note that this only does a one time import. In order to continuously pull new data,
you should set up a cronjob.

### Option 2: isems-data-collector subscribes to central MQTT broker
If you want to load data from a central MQTT broker, set the `MQTT_SERVER` environment
variable to the domain of the broker. You can then call `flask subscribe` which will
start a long-running process that will subscribe to the broker and update the data in
the local database, whenever it is received from the broker.

## Endpoints
### `/measurements/latest`
Returns the latest measurement for each node known to the system that has been active within the 
last 30 days (configurable with `HIDE_INACTIVE_AFTER_DAYS`).
You can add `?all=true` to also show data for nodes that have not been active for a longer time.
This endpoint is used by the app for the overview page.

### `/measurements/<node_id>/latest`
Returns the latest (60 * 24 = 1440) measurements for the given node. 
This endpoint is used by the app for charting details for the node.


## Configuration
The behavior of the data-collector can be configured via the following environment variables:

|Name|Description|Default Value|
|----|----|----|
|DATABASE_URL|The url to the database|`sqlite:////tmp/test.db`|
|HIDE_INACTIVE_AFTER_DAYS|Number of days after which nodes should no longer appear in `/measurements/latest` if they have not sent data|`30`|
|ISEMS_ROUTER_IPS|Nodes to query for data, comma separated (used in Option 1 described above)|`10.36.158.33`|
|MQTT_SERVER|Domain name for the MQTT broker to subscribe to (used in Option 2 described above)|_None_|
|SENTRY_DSN|If configured, the [DSN](https://docs.sentry.io/product/sentry-basics/dsn-explainer/) to use to send data to Sentry |_None_|

## Testing
```bash
pytest
```

## Deploying
The complete ISEMS setup can be deployed with [isems-ansible](https://github.com/isems/isems-ansible).
Refer to the documentation there for more information.
