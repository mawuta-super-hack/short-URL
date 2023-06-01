import os

# from logging import config as logging_config
# from core.logger import LOGGING

# logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'URL-for-shorten')
PROJECT_HOST = os.getenv('PROJECT_HOST', '127.0.0.1')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8080'))
SHORT_URL_ID_LENGTH = 6
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
