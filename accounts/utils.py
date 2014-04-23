import logging
import uuid

from accounts.models import ParklePlayer

log = logging.getLogger(__name__)


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


def validate_player_key(player_key, data):
    """
    :param player_key: player key to validate
    :type player_key: `String`
    :param data:
    :type data:
    :return:
    :rtype:
    """
    try:
        player = ParklePlayer.objects.get(player_key=player_key)
        secret_key = data.pop(u'player_secret_key')
        if player.secret_key != secret_key:
            w = u"Security key mismatch for player key {0}".format(player_key)
            log.warning(w)
            return False
        return player
    except ParklePlayer.DoesNotExist:
        return False