from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger()

logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'))
logger.addHandler(stream_handler)


# logging.basicConfig(
#   level=logging.INFO,
#   format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
#   datefmt='%Y-%m-%d %H:%M:%S'
# )

PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_USER     = os.getenv('PG_USER')
PG_HOST     = os.getenv('PG_HOST')
PG_PORT     = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE', "postgres")


print({PG_PASSWORD, PG_USER, PG_HOST, PG_PORT, PG_DATABASE})
