import setup
import glob
import json
import typer
# from aws_lambda_powertools import Logger
import logging

import main

event_json_format = {
  "requestContext": {
    "http": {
      "method": "POST"
    }
  },
}

app = typer.Typer()
logger = logging.getLogger()

@app.command()
def mock():
  create_pageview()
  add_pageview()
  get_pageview()
  return

@app.command()
def create_pageview():
  
  create_events_files = glob.glob("app/events/create-page-views/*.json")
  for event_file in create_events_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return 

@app.command()
def add_pageview():
  add_event_files     = glob.glob("app/events/add-views/*.json")
  for event_file in add_event_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return 

@app.command()
def get_pageview():
  get_event_files     = glob.glob("app/events/get-views/*.json")
  for event_file in get_event_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return


if __name__ == "__main__":
  app()
