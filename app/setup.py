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

PG_PASSWORD   = os.getenv('PG_PASSWORD')
PG_USER       = os.getenv('PG_USER')
PG_HOST: str  = os.getenv('PG_HOST', "127.0.0.1")
PG_PORT: str  = os.getenv('PG_PORT', "5432")
PG_DATABASE   = os.getenv('PG_DATABASE', "postgres")
PG_PASSWORD_SECRET_NAME = os.getenv('PG_PASSWORD_SECRET_NAME', "mySecretDatabasePassword")
IS_RUNNING_IN_AWS = os.getenv('AWS_LAMBDA_FUNCTION_NAME', False)

print({PG_PASSWORD, PG_USER, PG_HOST, PG_PORT, PG_DATABASE})
