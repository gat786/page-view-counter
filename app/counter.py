import setup
from pg8000 import dbapi
from pg8000 import exceptions
# from aws_lambda_powertools import Logger
import logging

logger = logging.getLogger()

def get_counts_for_page(page_id: str) -> tuple | None:
  try:
    
    conn = dbapi.connect(
      host=setup.PG_HOST,
      port=int(setup.PG_PORT),
      user=setup.PG_USER,
      password=setup.PG_PASSWORD,
      database=setup.PG_DATABASE  # Make sure to add this
    )
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM views WHERE page_id = %s", (page_id,))
    record = cursor.fetchone()
    conn.close()
    return record if record else None
  except Exception as e:
    if "relation" in str(e) and "does not exist" in str(e):
      logger.warning("Table does not exist")
    else:
      logger.error(f"An error occurred: {e}")
    return None

def increase_count_for_page(page_id: str) -> tuple | None:
  conn = dbapi.connect(
    host=setup.PG_HOST,
    port=int(setup.PG_PORT),
    user=setup.PG_USER,
    password=setup.PG_PASSWORD,
    database=setup.PG_DATABASE
  )
  cursor = conn.cursor()
  cursor.execute("UPDATE views SET count = count + 1 WHERE page_id = %s", (page_id,))
  if cursor.rowcount == 0:
    logger.warning(f"Page {page_id} does not exist")
    conn.close()
    return None
  cursor.execute("SELECT * FROM views WHERE page_id = %s", (page_id,))
  page_record = cursor.fetchone()
  conn.commit()
  conn.close()
  return page_record

def create_page(page_id: str) -> tuple | None:
  conn = dbapi.connect(
    host=setup.PG_HOST,
    port=int(setup.PG_PORT),
    user=setup.PG_USER,
    password=setup.PG_PASSWORD,
    database=setup.PG_DATABASE
  )
  try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO views (page_id) VALUES (%s)", (page_id,))
    conn.commit()
    cursor.execute("SELECT * FROM views WHERE page_id = %s", (page_id,))
    page_record = cursor.fetchone()
    conn.close()
    return page_record
  except Exception as e:
    if "relation" in str(e) and "does not exist" in str(e):
      logger.warning("Table does not exist")
    elif "duplicate key value" in str(e):
      logger.warning(f"Page {page_id} already exists")
    else:
      logger.error(f"An error occurred: {e}")
    conn.close()
    return None

def create_views_table():
  conn = dbapi.connect(
    host=setup.PG_HOST,
    port=int(setup.PG_PORT),
    user=setup.PG_USER,
    password=setup.PG_PASSWORD,
    database=setup.PG_DATABASE
  )
  logger.info(f"Creating table with connection: {conn}")
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS views (
        page_id VARCHAR(255) NOT NULL PRIMARY KEY,
        count INT NOT NULL DEFAULT 0
    )
  """)
  conn.commit()
  conn.close()
