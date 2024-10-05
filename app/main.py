import setup
import typer
import json
import counter
import logging

app     = typer.Typer()
logger  = logging.getLogger(__name__)

@app.command()
def create_views_table():
  counter.create_views_table()
  logger.info("Table created")

@app.command()
def create_page(page_id: str):
  result = counter.create_page(page_id)
  if result is None:
    logger.warning(f"Page {page_id} already exists")
    return
  logger.info(f"Created page {page_id}")
  logger.info("Page record: %s", result)
  return result

@app.command()
def add_page_view(page_id: str):
  count = counter.get_counts_for_page(page_id)
  if count is None:
    logger.warning(f"Page {page_id} does not exist")
    exit(1)
  logger.info(f"Page {page_id} already viewed {count[0]} times")
  counter.increase_count_for_page(page_id)
  logger.info(f"Increased {page_id} view count to {count[0] + 1}")

@app.command()
def get_counts_for_page(page_id: str):
  count = counter.get_counts_for_page(page_id)
  if count is None:
    logger.warning(f"Page {page_id} does not exist")
    exit(1)
  logger.info(f"Page {page_id} viewed {count[0]} times")
  return count

def lambda_handler(event, context):
  body = {}
  if "requestContext" in event:
    requestContext = event["requestContext"]
    if "http" in requestContext:
      http = requestContext["http"]
      if "method" in http:
        method = http["method"]
        if method == "POST":
          body = json.loads(event["body"])
  logger.debug("Body: ", body)
  if "method" in body and "url" in body:
    method = body["method"]
    if "host" in body:
      host = body["host"]
      logger.debug("We are getting calls from host: ", host)
    if method == "add-view":
      logger.debug("We will add a page view to this url: ", body["url"])
      complete_url = f"{host}{body['url']}"
      add_page_view(complete_url)
    if method == "get-view":
      logger.debug("We will get the views for this url: ", body["url"])
      complete_url = f"{host}{body['url']}"
      get_counts_for_page(complete_url)
    if method == "create-page-view":
      logger.debug("We will create the views for this url: ", body["url"])
      complete_url = f"{host}{body['url']}"
      create_page(complete_url)
  return

if __name__ == "__main__":
  app()
