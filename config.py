# config.py
import os
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    
    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', '141.209.241.91')
    MYSQL_USER = os.getenv('MYSQL_USER', 'sp2025bis698g2')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Group@2')
    MYSQL_DB = os.getenv('MYSQL_DB', 'sp2025bis698g2s')
    MYSQL_CURSORCLASS = 'DictCursor'


