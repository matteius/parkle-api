from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from api import serializers
from accounts.models import ParklePlayer
from accounts import utils as account_utils

from parkle import state_utils

import logging
log = logging.getLogger(__name__)


def validation_error_response():
    e = {"error": "Sorry, the requested action was not valid."}
    return Response(e, status=status.HTTP_400_BAD_REQUEST)


class GameStatedView(APIView):
    """ API end-point for requesting a specific Parkle game state. """

    def post(self, request,):
        # Grab and parse request
        request_data = JSONParser().parse(request)
        serializer = serializers.GameStateSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.object
        game_uuid = data.pop('game_uuid')

        # Would be nice to do something to validate the API player's key is part of the game


        # So now we actually have to look up the game state from redis [How to model the state in redis ;-)]


        # Choose how to represent this state in a response from the API
        response = {"game_uuidxxxx": "TOKEN-GAMESTATE"}
        return Response(response, status=status.HTTP_200_OK)


class GameActionView(APIView):
    """ API end-point for performing an action on a specific Parkle Game. """

    def post(self, request, ):
        pass


class CreateGameView(APIView):
    """ API end-point for performing an action on a specific Parkle Game. """

    def post(self, request):
        request_data = JSONParser().parse(request)
        serializer = serializers.InitiateGameSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.object
        #player = None
        player_key = data.pop('player_api_key')
        try:  # Validate the player is who they claim to be -- possibly reusable but avoid overusing queryset
            player = ParklePlayer.objects.get(player_key=player_key)
            secret_key = data.pop('player_secret_key')
            if player.secret_key != secret_key:
                w = "Security key mismatch for player key {0}".format(player_key)
                log.warning(w)
                return validation_error_response()
            game_uuid = state_utils.check_player_for_existing_game(player_key)
            if game_uuid:
                e = {"error": "Sorry, it appears you have an existing game with uuid: {0}".format(game_uuid)}
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except ParklePlayer.DoesNotExist:
            return validation_error_response()
        else:  # Request validated, create game
            ai_username = data.pop('computer_bot_username')




class RequestPlayerKeyView(APIView):
    """ API end-point for registering a player with a username and getting a player key uuid. """

    def post(self, request):
        request_data = JSONParser().parse(request)
        serializer = serializers.RequestPlayerSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.object
        username = data.pop('username_requested')
        player, v = ParklePlayer.objects.get_or_create(username=username)
        if not v:
            r = {"error": "The requested username is already taken."}
            return Response(r, status=status.HTTP_400_BAD_REQUEST)
        email_address = data.pop('email_address')
        player = account_utils.finalize_new_player(player, email_address)
        r = {
            "username": player.username,
            "email_address": player.email_address,
            "player_key": player.player_key,
            "secret_key": player.secret_key,
            "note": "Save this data off, you will not be able to retrieve it at this time!"
        }
        return Response(r, status=status.HTTP_201_CREATED)
