#!/usr/bin/python3
"""Module creates API methods and routes for place review objects"""
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    user = storage.get('User', body['user_id'])
    if user is None:
        abort(404)
    if 'text' not in body:
        abort(400, 'Missing text')
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    for key, value in body.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
