# aiq-assignment

## Docker Image
Docker image is made publicly available in docker hub

available here : https://hub.docker.com/repository/docker/dilanim/aiq-assignment

tag : dilanim/aiq-assignment:python-aiq

## DB

MongoDB Atlas has been used. No IP restrictions added.

## How to run the APIs

###### API Key

Token based authentication has been implented. Pass this key in the header to access the APIs.

a2ed122d508fbf0ba62adaf9155409a7b9120b1d

###### Endpoints

**Base url** : http://host/power-generation/api/

-**get_states_annual_generation** - get net annual generation of all states in MWh

-**get_plants_annual_generation** - get net annual generation of all plants in MWh

-**get_top_n_plants?n=5** - get top n plants

-**filter_by_state?state=AK** - Filter by a state

-**get_plant_details?plant=Anchorage 1** - Retrieve details of a single plant

## UI
A simple UI has been developed

Available here: git hub link

    
[Screenshot of ui available here](ui.png)
