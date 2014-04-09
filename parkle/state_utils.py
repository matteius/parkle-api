import redis
import uuid
import datetime

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
POOL = redis.ConnectionPool(host='10.0.0.1', port=6379, db=0)


def perform_dice_roll(n):
    """ Will use the parkle util to perform the roll, but
    returns the result as a string as for saving in a redis key.
    :param n: number of dice to roll
    :type n: `int`
    :return: the comma seperated string of dice
    :rtype: `string`
    """
    dice = utils.dice_roll(n)



def check_player_for_existing_game(player_key):
    """ Checks for the game_uuid of a game player is currently engaged.
    :param player_key: the player api ley being checked
    :type player_key: `string`
    :return: False or the matching game uuid string
    :rtype: False or `string`
    """
    my_conn = redis.Redis(connection_pool=POOL)
    current_game = my_conn.hget(u"player_table", player_key)
    if current_game:
        return current_game
    return False


def initiate_game(player_key, ai_bot_key=None):
    """ Is called to initiate a new game for the player,
    verification no game exists is done prior to calling.
    :param player_key:
    :type player_key:
    :return:
    :rtype:
    """
    my_conn = redis.Redis(connection_pool=POOL)
    game_uuid = uuid.uuid4()
    my_conn.hset(u"player_table", player_key, game_uuid)
    scores_key = u"{0}_scores".format(game_uuid)
    my_conn.hset(scores_key, player_key, 0)
    if ai_bot_key:
        my_conn.hset(scores_key, ai_bot_key, 0)
    state_key = u"{0}_state".format(game_uuid)
    my_conn.hset(state_key, u"start_time", datetime.datetime.now())
    my_conn.hset(state_key, u"current_player", player_key)
    my_conn.hset(state_key, u"dice_roll", [])


    return game_uuid
