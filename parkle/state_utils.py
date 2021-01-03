import json
import redis
import uuid

from parkle import utils

"""
Game State in redis -- minimal information required to model a game

Ideally most keys in are based on game uuid, such as follows:

"<game_uuid>_state":  {
    "start_time": timestamp,
    "current_player":  "player_key",
    "current_dice_roll": "",
    # "kept_set": "1, 1, 1, 5, 5",  # Probably not needed to store in redis, it is a parameter for computation.
    "running_points: "",
    ...
}

# Player list can be derived from scores using HKEYS key to get all the fields
"<game_uuid>_scores":  {
    "player_key_A":  "score of A",
    "player_key_B":  "score of B",
    "player_key_C":  "score of C",
    "player_key_D":  "score of D",
    ...
}

# Will need to be able to identify if a player already has an active game
# Absence from table implies that the the player is not in an active game.
"player_table": {
    "player_key_A":  "game_uuid",
}

"""

# TODO Pull connection settings from settings
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)

def get_redis_connection():
    my_conn = redis.Redis(connection_pool=POOL)
    return my_conn


def fetch_dice_state(game_uuid):
    game_state = f"{game_uuid}_state"
    my_conn = get_redis_connection()
    dice = my_conn.hget(game_state, "dice_roll").decode('utf-8')
    dice = json.loads(dice)
    return dice


def perform_dice_roll(game_uuid, n):
    """ Utilize the parkle dice roll utility and roll n dice and save it to the game state.
    Does not validate current player, that should be done in conjunction with calling this.
    """
    game_state = f"{game_uuid}_state"
    my_conn = get_redis_connection()
    dice = utils.dice_roll(n)
    my_conn.hset(game_state, "dice_roll", json.dumps(dice))
    return dice



def check_player_for_existing_game(player_key):
    """ Checks for the game_uuid of a game player is currently engaged.
    For the purpose of joining a game, the atomic function `initiate_game`
    should be called which verifies in an atomic way for game creation.
    :param player_key: the player api key being checked
    :type player_key: `string`
    :return: False or the matching game uuid string
    :rtype: False or `string`
    """
    my_conn = get_redis_connection()
    current_game = my_conn.hget("player_table", player_key).decode('utf-8')
    if current_game:
        return current_game
    return False


def initiate_game(player_key, game_uuid=None):
    """ Atomic function for initializing a game for human player.
    Verification player is not a part of existing game is part of call.
    Player will join game specified in parameter, or will spawn a new game.
    :param player_key: player api key being initiated into game
    :param game_uuid: (optional) game uuid to join.
    :return: game_uuid `string` or False (player already in existing game)
    """
    new_game = False
    if game_uuid is None:  # Completely new game
        game_uuid = uuid.uuid4().hex
        new_game = True
    my_conn = get_redis_connection()
    my_conn.flushdb()
    r = my_conn.hsetnx("player_table", player_key, game_uuid)
    if r:  # If player is now added to game (success)
        scores_key = f"{game_uuid}_scores"
        my_conn.hset(scores_key, player_key, 0)
        if new_game:  # Initialize new game
            game_state = f"{game_uuid}_state"
            my_conn.hset(game_state, "current_player", player_key)
            perform_dice_roll(game_uuid, 6)

        return game_uuid
    return False


def current_player_check(game_uuid, player_key):
    """ Checks if the player key is the current player in game uuid,
    but only at that instance of time it checks.  Returns boolean.
    """
    my_conn = get_redis_connection()
    game_state = f"{game_uuid}_state"
    actual_current = my_conn.hget(game_state, 'current_player')
    if actual_current and actual_current.decode('utf-8') == player_key:
        return True
    return False


def perform_game_action(game_uuid, player_key):
    pass
