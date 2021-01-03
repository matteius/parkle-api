from django.urls import path

from api import views as api_views

app_name = 'api'

urlpatterns = [
    path('game-state/', api_views.GameStateView.as_view(), name='game_state_view'),
    path('request-player/', api_views.RequestPlayerKeyView.as_view(), name='request_player_view'),
    path('create-game/', api_views.CreateGameView.as_view(), name='create_game'),
    path('game-action/', api_views.GameActionView.as_view(), name='game_action'),
]
