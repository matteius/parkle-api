from django.conf.urls import patterns, url

from api import views as api_views


urlpatterns = patterns(
    '',
    url(r'^game-state[/]?$', api_views.GameStatedView.as_view(), name='game_state_view'),
    url(r'^request-player[/]?$', api_views.RequestPlayerKeyView.as_view(), name='request_player_view'),

)
