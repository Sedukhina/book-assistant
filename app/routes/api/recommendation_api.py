from flask import Blueprint, request, jsonify,session

from services.recommendation_service import RecommendationService

recommendation_api = Blueprint("recommendation",__name__,url_prefix="/recommendation")

API_KEY = "<API_KEY>"


@recommendation_api.route("/test",methods=['POST'])
def test():
    recommendation_service = RecommendationService(API_KEY, session.get('username'))
    query = request.json['query']
    result = recommendation_service.recommend(query)

    return jsonify({'message':'ok','data':result}), 200