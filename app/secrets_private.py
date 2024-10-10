import logging
import boto3
import setup

logger = logging.getLogger()

def get_postgres_password():
  if setup.IS_RUNNING_IN_AWS:
    secret_name = setup.PG_PASSWORD_SECRET_NAME
    s3 = boto3.client("secretsmanager")
    secretswrapper = GetSecretWrapper(s3)
    return secretswrapper.get_secret(secret_name)
  else:
    return setup.PG_PASSWORD

class GetSecretWrapper:
  def __init__(self, secretsmanager_client):
    self.client = secretsmanager_client


  def get_secret(self, secret_name):
    """
    Retrieve individual secrets from AWS Secrets Manager using the get_secret_value API.
    This function assumes the stack mentioned in the source code README has been successfully deployed.
    This stack includes 7 secrets, all of which have names beginning with "mySecret".

    :param secret_name: The name of the secret fetched.
    :type secret_name: str
    """
    try:
      get_secret_value_response = self.client.get_secret_value(
          SecretId=secret_name
      )
      logging.info("Secret retrieved successfully.")
      return get_secret_value_response["SecretString"]
    except self.client.exceptions.ResourceNotFoundException:
      msg = f"The requested secret {secret_name} was not found."
      logger.info(msg)
      return msg
    except Exception as e:
      logger.error(f"An unknown error occurred: {str(e)}.")
      raise



