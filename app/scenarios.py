from flask import session

from services.recommendation_service import RecommendationService



def process_command(command):
    # Ініціалізація RecommendationService
    recommendation_service = RecommendationService(
        api_key="<API_KEY>",
        username=session.get("username")
    )
    """
    Використовує RecommendationService для генерації відповіді на команду користувача.
    """
    response = recommendation_service.recommend(command)
    return response or "Вибачте, я не зміг обробити ваш запит."
