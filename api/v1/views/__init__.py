#!/usr/bin/python3
"""Module registers views for our API application"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from . import index, states, cities, amenities, users, places
