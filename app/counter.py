import re
from psycopg import connection
import psycopg
from psycopg.rows import TupleRow
import pg
import logging

logger = logging.getLogger()

def get_counts_for_page(page_id: str) -> TupleRow | None:
  with psycopg.connect(
      host='localhost',
      port=5432,
      user='postgres',
      password='postgres',
    ) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT count FROM views WHERE page_id = %s", (page_id,))
    record = cursor.fetchone()
    return record if record else None

def increase_count_for_page(page_id: str) -> TupleRow | None:
  with psycopg.connect(
      host='localhost',
      port=5432,
      user='postgres',
      password='postgres',
    ) as connection:
    cursor = connection.cursor()
    result = cursor.execute("UPDATE views SET count = count + 1 WHERE page_id = %s", (page_id,))
    if result.rowcount == 0:
      logger.warning(f"Page {page_id} does not exist")
      return None
    result = cursor.execute("SELECT * FROM views WHERE page_id = %s", (page_id,))
    page_record = result.fetchone()
    connection.commit()
    return page_record

def create_page(page_id: str) -> TupleRow | None:
  with psycopg.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres',
  ) as connection:
    try:
      cursor = connection.cursor()
      cursor.execute("INSERT INTO views (page_id) VALUES (%s)", (page_id,))
      connection.commit()
      records = cursor.execute("SELECT * FROM views WHERE page_id = %s", (page_id,))
      page_record = records.fetchone()
      return page_record
    except psycopg.errors.UniqueViolation:
      logger.warning(f"Page {page_id} already exists")
      return None

def create_views_table():
  with psycopg.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres',
  ) as connection:
    cursor = connection.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS views (
        page_id VARCHAR(255) NOT NULL PRIMARY KEY,
        count INT NOT NULL DEFAULT 0
      )
    """)
    connection.commit()
    