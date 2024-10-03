import setup
import typer
import counter
import logging

app     = typer.Typer()
logger  = logging.getLogger(__name__)

@app.command()
def create_views_table():
  counter.create_views_table()
  typer.echo("Table created")

@app.command()
def create_page(page_id: str):
  result = counter.create_page(page_id)
  if result is None:
    logger.warning(f"Page {page_id} already exists")
    exit(1)
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

if __name__ == "__main__":
  app()