#!/usr/bin/env python 2
"""Configuration class for managing .env for the DC2 Data Lake API."""

import flask
from flask.ext.dotenv import DotEnv

class Config:
    SECRET_KEY = ":'("

    @classmethod
    def init_app(self, app):
        # env = DotEnv(app)
        env = DotEnv()
        env.init_app(app)