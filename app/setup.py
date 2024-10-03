from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'
)

PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_USER     = os.getenv('PG_USER')