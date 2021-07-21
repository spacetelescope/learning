# Chatbot using Facebook's BlenderBot 2.0
Launches a search service using ElasticSearch for domain specific content.
Hosts a Python Flask web service to index content and search
Runs the BlenderBot 2.0 in interactive mode connected to the search service

## Install

```
$ docker-compose build
```

## Run Search Server

```
$ docker-compose up -d elasticsearch chatbot-server
```

## Loading Content

Use example Slack help articles in `helps.json`

```
docker-compose exec chatbot-server python -c "from server import helper; helper()"
```

## Starting the Chatbot

```
docker-compose up chatbot-interactive
```

The first time this runs it will download the model files first before starting the chat prompt.

## Accessing the Chatbot

Once the chatbot is running, just head to [http://localhost:8080](http://localhost:8080) to start your conversation.
