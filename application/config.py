import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")
    DEBUG = True
    SECRET_KEY =  "ash ah secet"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379


