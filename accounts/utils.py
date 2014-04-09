import uuid


def finalize_new_player(player, email_address):
    """ Utility for finishing the creation of a new game player.
    :param player: newly created ParklePlayer
    :type player: `ParklePlayer`
    :param email_address: requested player's E-mail address
    :type email_address: `string`
    :return: updated player with keys
    :rtype: `ParklePlayer`
    """
    player.email_address = email_address
    player.player_key = uuid.uuid4().hex
    player.secret_key = uuid.uuid4().hex
    player.save()
    return player
