#Database credentials
import os

host = os.environ['DB_HOST']
port = int(os.environ['DB_PORT'])
user = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
database = os.environ['DB_NAME']
