import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Roy.12345@localhost:3306/secure_banking_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Roy.12345,"
    JWT_SECRET_KEY = "Roy.12345,"  # Load from environment variable
    DEBUG = True
