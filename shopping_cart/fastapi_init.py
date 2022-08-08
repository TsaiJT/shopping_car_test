# built-in
import logging
from logging.handlers import RotatingFileHandler

# 3rd
from fastapi import FastAPI


def create_app():
    app = FastAPI()

    return app

app = create_app()

