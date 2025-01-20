from services.recommendation_service import RecommendationService

# Ініціалізація RecommendationService
recommendation_service = RecommendationService(
    api_key="key",
    username="default_user"  # замініть на відповідного користувача
)

def process_command(command):
    """
    Використовує RecommendationService для генерації відповіді на команду користувача.
    """
    response = recommendation_service.recommend(command)
    return response or "Вибачте, я не зміг обробити ваш запит."
