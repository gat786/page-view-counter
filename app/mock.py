import setup
import glob
import logging
import json

import main

event_json_format = {
  "requestContext": {
    "http": {
      "method": "POST"
    }
  },
}

logger = logging.getLogger()

def mock():
  # mock_create_pageview()
  # mock_add_pageview()
  mock_get_pageview()
  return

def mock_create_pageview():
  create_events_files = glob.glob("app/events/create-page-views/*.json")
  for event_file in create_events_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return 

def mock_add_pageview():
  add_event_files     = glob.glob("app/events/add-views/*.json")
  for event_file in add_event_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return 

def mock_get_pageview():
  get_event_files     = glob.glob("app/events/get-views/*.json")
  for event_file in get_event_files:
    event = event_json_format.copy()
    with open(event_file, "r") as fp: 
      event["body"] = json.dumps(json.loads(fp.read()))
      logger.info("Event: %s", event)
      main.lambda_handler(event, None)
  return


if __name__ == "__main__":
  mock()
