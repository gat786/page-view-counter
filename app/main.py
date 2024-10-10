import re
import setup
import typer
import json
import counter
import logging
import secrets_private

app     = typer.Typer()
logger  = logging.getLogger()

@app.command()
def create_views_table():
  try:
    logger.info("Creating table")
    counter.create_views_table()
    logger.info("Table created")
  except Exception as e:
    logger.error("Error creating table: %s", e)
    exit(1)

@app.command()
def create_page(page_id: str):
  """
  Creates a page with the given page_id in the database,
  so that you can track the number of views for that page
  
  Parameters:
  -----------
  page_id: str # this is generally the url that you want to track
  views for for e.g. https://devops-stuff.com/blogs/2021/01/01/what-is-devops

  Returns:
  --------
  TupleRow | None
    This is the record of the page that was created
  """
  result = counter.create_page(page_id)
  if result is None:
    logger.warning(f"Page creation for: {page_id} failed")
    return
  logger.info(f"Created page {page_id}")
  logger.info("Page record: %s", result)
  return result

@app.command()
def add_page_view(page_id: str):
  """
  Adds 1 to the count of views for the page with the given page_id
  
  Parameters:
  -----------
  page_id: str # this is generally the url that you want to track
  views for for e.g. https://devops-stuff.com/blogs/2021/01/01/what-is-devops

  Returns:
  --------
  dict
    { "page_id": str, "count": int } # the page_id and the number 
    of views for that page
  """
  count = counter.get_counts_for_page(page_id)
  if count is None:
    logger.warning(f"Page {page_id} does not exist, or the table does not exist")
    exit(1)
  logger.info(f"Page {page_id} already viewed {count[0]} times")
  counter.increase_count_for_page(page_id)
  current_count = counter.get_counts_for_page(page_id)
  logger.info(f"Increased {page_id} view count to {current_count}")
  return {
    "page_id": page_id,
    "count": current_count
  }

@app.command()
def get_counts_for_page(page_id: str) -> dict:
  """
  Get the number of views for the page with the given page_id
  
  Parameters:
  -----------
  page_id: str # this is generally the url that you want to track
  views for for e.g. https://devops-stuff.com/blogs/2021/01/01/what-is-devops

  Returns:
  --------
  dict
    { "page_id": str, "count": int } # the page_id and the number 
    of views for that page
  """
  count = counter.get_counts_for_page(page_id)
  if count is None:
    logger.warning(f"Page {page_id} does not exist")
    exit(1)
  logger.info(f"Page {page_id} viewed {count[0]} times")
  return {
    "page_id": page_id,
    "count": count[0]
  }


def lambda_handler(event, context):
  logger.info(f"Executing lambda function for event: {event}",)
  body = {}
  if "requestContext" in event:
    requestContext = event["requestContext"]
    if "http" in requestContext:
      http = requestContext["http"]
      if "method" in http:
        method = http["method"]
        if method == "POST":
          if "body" in event:
            body = json.loads(event["body"])
          else:
            return {
              "statusCode": 400,
              "body": json.dumps("No body provided")
            }
        else:
          return {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
          }
  logger.debug(f"Body: {body}")
  response = {}
  required_keys = ["method", "url", "website", "host"]
  for key in required_keys:
    if key not in body:
      return {
        "statusCode": 400,
        "body": json.dumps({
          "message": f"Missing required key: {key}",
          "keys_required": required_keys
        })
      }
  url     = body["url"]
  method  = body["method"]
  host    = body["host"]
  website = body["website"]
  logger.info("Received request from host: %s", host)
  if method == "add-view":
    logger.debug(f"We will add a page view to this url: {body["url"]}")
    complete_url = f"{website}{url}"
    response = add_page_view(complete_url)
  if method == "get-view":
    logger.debug(f"We will get the views for this url: {body["url"]}")
    complete_url = f"{website}{url}"
    response = get_counts_for_page(complete_url)
  if method == "create-page-view":
    logger.debug(f"We will create the views for this url: {body["url"]}")
    complete_url = f"{website}{url}"
    response = create_page(complete_url)
  return {
    "statusCode": 200,
    "body": json.dumps(response)
  }

if __name__ == "__main__":
  app()
