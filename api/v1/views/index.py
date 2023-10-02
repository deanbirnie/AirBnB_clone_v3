#!/usr/bin/python3
"""Module creates a route and works in conjunction with our views file"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON string with the status"""
    return jsonify({"status": "OK"})
