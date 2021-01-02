from rest_framework import serializers


class RequestPlayerSerializer(serializers.Serializer):
    username_requested = serializers.CharField()
    email_address = serializers.EmailField()


class InitiateGameSerializer(serializers.Serializer):
    player_api_key = serializers.CharField()
    player_secret_key = serializers.CharField()
    computer_bot_username = serializers.CharField(required=False)


class GameStateSerializer(serializers.Serializer):
    game_uuid = serializers.CharField()
    player_api_key = serializers.CharField()


class GameActionSerializer(serializers.Serializer):
    game_uuid = serializers.CharField()
    player_api_key = serializers.CharField()
    #kept_set = serializers.RelationsList()


