from django.urls import path

from api import views as api_views

app_name = 'api'

urlpatterns = [
    path('game-state/', api_views.GameStatedView.as_view(), name='game_state_view'),
    path('request-player/', api_views.RequestPlayerKeyView.as_view(), name='request_player_view'),
]
