import os
from environs import Env

# Load env variables from projects root .env file
env = Env()
env.read_env(os.getcwd() + '/.env')
