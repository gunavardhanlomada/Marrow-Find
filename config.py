import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'output'
    DATABASE = 'database.db'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
