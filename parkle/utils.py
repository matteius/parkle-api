
from pprint import pprint
import random
rand = random.Random()


def nested_dice(flattened_dice):
    """ Nest the long list of dice into a "zipped" list of tuples,
        where the first value is the dice face and the second is the count.

    :param flattened_dice: :py:class:`list`

    :return:
        :py:class:`list` : list of tuples, such as [(dice face, count), ...]

    Return value is sorted by increasing value, and nested as a list of tuples.
        Any 0 count values are omitted from the list.
    Return:
        [(face value, quantity), ...]
        [(3, 2), (4, 4)] == Pair of 3s, four 4s
    """
    nested_dice = []
    for face_value in range(1, 7):
        count = flattened_dice.count(face_value)
        if count > 0:
            nested_dice.append((face_value, count))

    return nested_dice


def flatten_nested_dice(nested_dice):
    """ Utility for taking a nested dice list and flattening it to a list of dice.
    :param nested_dice: :py:class:`list` list of tuples, such as [(dice face, count), ...]

    :return:
        :py:class:`list` : flattened list of dice.
    """
    deconstructed_dice = []
    for (face_value, count) in nested_dice:
        for x in range(0, count):
            deconstructed_dice.append(face_value)

    return deconstructed_dice


def dice_roll(n):
    """ Perform a dice roll of n 6-sided dice.

    :param n: int
    :return:
        :py:class:`list` : list of tuples, such as [(dice_face, count), ...]

    Return: list of dice rolled
    """
    assert 1 <= n <= 6, "rolling {0} Dice is not within allowed range: [1,6].".format(n)

    dice = []
    for i in range(0, n):
        dice.append(rand.randint(1, 6))

    return dice


def points_possible(dice):
    """ Determines if there is a scoring option within the supplied dice list.

    :param dice: :py:class:`list` A nested dice list like the one from nested_dice
    :return:
        `boolean` : Returns truth value if points are possible from dice list.
    """
    num_pairs = 0
    for i in dice:
        if i[0] == 1 or i[0] == 5:
            return True

        if i[1] >= 3:
            return True

        if i[1] == 2:
            num_pairs += 1

        if num_pairs == 3:
            return True

    return False


def nested_kept_set(kept_set):
    """ Build a dictionary from kept_set where each key is a dice face
     and lookup resolves the count in the set.
    """
    nested_set = {}
    for die in kept_set:
        count = nested_set.get(die, 0)
        nested_set[die] = count + 1

    return nested_set


def validate_kept_set(dice):
    """ Ensure that all dice kept are scoring dice, otherwise return error.
    :return: `boolean` : True or asserts that dice must be in range D6.
    """
    try:
        validate_dice_in_range(dice)
        calculate_point_set(dice)
    except AssertionError as ae:
        return False
    else:
        return True


def validate_dice_in_range(dice_set):
    """ Helper function for validating dice are within range.
    Also Validates max set length of 6, and minimum of 1
    :return: `boolean` : True or asserts that dice must be in range D6.
    """
    set_length = 1 if type(dice_set) is int else len(dice_set)
    assert set_length <= 6, "Length of dice set {0} expected to be no more than 6!".format(set_length)
    assert set_length > 0, "Length of dice set {0} expected to be more than 0!".format(set_length)
    for face_value in dice_set:
        assert face_value in range(1, 7), "Dice face value {0} must be in range D6!".format(face_value)
    return True


def is_three_pair(unique_dice_count, nested_set):
    """ Validates if the nested set contains 3 pairs.
    Assumes dice are within range.
    """
    if unique_dice_count == 3:
        for face_value, count in nested_set.iteritems():
            if count != 2:
                return False
        return True  # (3) Unique dice and each as pairs
    return False


def is_three_of_a_kind(unique_dice_count, dice_counts):
    """ Was the dice roll a four of a kind?
    """
    if unique_dice_count == 1 and 3 in dice_counts:
        return True
    return False


def has_three_of_a_kind(dice_counts):
    """ Has three of a kind dice based on dice count list.
    """
    if 3 in dice_counts:
        return True
    return False


def is_four_of_a_kind(unique_dice_count, dice_counts):
    """ Was the dice roll a four of a kind?
    """
    if unique_dice_count == 1 and 4 in dice_counts:
        return True
    return False


def has_four_of_a_kind(dice_counts):
    """ Has four of a kind dice based on dice count list.
    """
    if 4 in dice_counts:
        return True
    return False


def is_five_of_a_kind(unique_dice_count, dice_counts):
    """ Was the dice roll a five of a kind?
    """
    if unique_dice_count == 1 and 5 in dice_counts:
        return True
    return False


def has_five_of_a_kind(dice_counts):
    """ Has five of a kind dice based on dice count list.
    """
    if 5 in dice_counts:
        return True
    return False


def is_six_of_a_kind(unique_dice_count, dice_counts):
    """ Was the dice roll a six of a kind?
    """
    if unique_dice_count == 1 and 6 in dice_counts:
        return True
    return False


def is_straight_six(unique_dice_count, nested_set):
    """ Does the nested set of dice (and given unique_dice_count)
    make for a straight six roll?
    :return: `boolean` : If roll was a straight 1-6
    """
    if unique_dice_count == 6:
        for i in range(1, 7):
            if i not in nested_set:
                return False
            if nested_set[i] != 1:
                return False
        return True
    return False


def is_two_sets_of_three(unique_dice_count, dice_counts):
    """ Assumes there were 6 dice in the kept calling set.
    Given this, utility determines two sets of 3 matching dice based on
    unique dice count of 2; 3 and only 3 in the nested count set.
    Nested count set is a set based on the list of face value counts.k
    """
    dice_count_set = set(dice_counts)
    if unique_dice_count == 2 and 3 in dice_count_set and len(dice_count_set) == 1:
        return True
    return False


def is_four_of_kind_and_pair(unique_dice_count, dice_counts):
    """ Assumes there were 6 dice in the kept calling set.
    Given this, utility determines four of a kind plus a pair,
    matching dice based on unique dice count of 2; 3 and only 3 in the nested count set.
    Nested count set is a set based on the list of face value counts.k
    """
    dice_count_set = set(dice_counts)
    if unique_dice_count == 2:  # Only 2 numbers should be present
        if 4 in dice_count_set and 2 in dice_count_set and len(dice_count_set) == 2:
            return True
    return False


def calculate_point_set(kept_set):
    """  Utility for calculating a sets point value.
    Any kept set should be validated prior to calling this function.

    :param kept_set: :py:class:`list` A flat list of the dice set the
            Calculate number of points from a player's kept set.

    :return:
        `int` : a point value for the set
    """
    if type(kept_set) is int:
        kept_set = [kept_set]  # Ensure set is array for algorithm, regardless of calling pattern
    nested_set = nested_kept_set(kept_set)
    dice_values = list(nested_set.viewkeys())
    dice_counts = list(nested_set.itervalues())
    unique_dice_count = len(dice_values)
    kept_set_length = len(kept_set)
    # A kept set of 6 may signify:
    #  * Six of a Kind (3000 pts)
    #  * Two sets of three of a kind (2500 pts)
    #  * A straight 1-6 (1500 pts)
    #  * 3 Pairs (1500 pts)
    #  * Four of a kind + pair (1500 pts)
    #  * Or some combination of smaller point pairs ...
    if kept_set_length == 6:
        if is_six_of_a_kind(unique_dice_count, dice_counts):
            return 3000
        elif is_two_sets_of_three(unique_dice_count, dice_counts):
            return 2500
        elif is_straight_six(unique_dice_count, nested_set):
            return 1500
        elif is_three_pair(unique_dice_count, nested_set):
            return 1500
        elif is_four_of_kind_and_pair(unique_dice_count, dice_counts):
            return 1500
        else:  # other score combinations exist for 6 kept set ...
            score = 0  # result accumulator
            if has_five_of_a_kind(dice_counts):
                for face_value, count in nested_set.iteritems():
                    if count == 5:
                        score += calculate_point_set([face_value for n in range(0, 5)])
                    else:  # Only one remaining die
                        score += calculate_point_set(face_value)
                return score  # Accumulated recursively
            elif has_four_of_a_kind(dice_counts):
                alt_kept_set = []
                for face_value, count in nested_set.iteritems():
                    if count == 4:
                        score += calculate_point_set([face_value for n in range(0, 4)])
                    else:
                        for n in range(0, count):
                            alt_kept_set.append(face_value)
                score += calculate_point_set(alt_kept_set)
                return score  # Accumulated recursively
            elif has_three_of_a_kind(dice_counts):
                alt_kept_set = []
                for face_value, count in nested_set.iteritems():
                    if count == 3:
                        score += calculate_point_set([face_value for n in range(0, 3)])
                    else:
                        for n in range(0, count):
                            alt_kept_set.append(face_value)
                score += calculate_point_set(alt_kept_set)
                return score  # Accumulated recursively
            else:  # recursively figure out which dice don't score (3 x 3)
                return calculate_point_set(kept_set[:3]) + calculate_point_set(kept_set[3:])

    # A kept set of 5 may signify:
    #  * Five of a kind (2000 pts)
    elif kept_set_length == 5:
        if is_five_of_a_kind(unique_dice_count, dice_counts):
            return 2000
        else:  # other score combinations exist for 5 kept set ...
            if has_four_of_a_kind(dice_counts):
                score = 0  # result accumulator
                for face_value, count in nested_set.iteritems():
                    if count == 4:
                        score += calculate_point_set([face_value for n in range(0, 4)])
                    else:  # Only one remaining die
                        score += calculate_point_set(face_value)
                return score  # Accumulated recursively
            elif has_three_of_a_kind(dice_counts):
                score = 0
                alt_kept_set = []
                for face_value, count in nested_set.iteritems():
                    if count == 3:
                        score += calculate_point_set([face_value for n in range(0, 3)])
                    else:
                        for n in range(0, count):
                            alt_kept_set.append(face_value)
                score += calculate_point_set(alt_kept_set)
                return score  # Accumulated recursively
            else:  # recursively figure out which dice don't score (3 x 2)
                return calculate_point_set(kept_set[:3]) + calculate_point_set(kept_set[3:])

    # A kept set of 4 may signify:
    #  * Four of a kind (1000 pts)
    elif kept_set_length == 4:
        if is_four_of_a_kind(unique_dice_count, dice_counts):
            return 1000
        else:  # Other score combinations exist for a 4 kept set?
            if has_three_of_a_kind(dice_counts):  # 3 of a kind and (1|5)
                score = 0  # Accumulate the result
                for face_value, count in nested_set.iteritems():
                    if count == 3:
                        score += calculate_point_set([face_value for n in range(0, 3)])
                    else:
                        score += calculate_point_set([face_value])
                return score  # Accumulated recursively
            else:  # A set of [1, 1, 5, 5] perhaps
                return calculate_point_set(kept_set[0:2]) + calculate_point_set(kept_set[2:4])

    # A kept set of 3 may signify:
    #  * 3 of a kind (face_value * 100)
    #  * [1, 1, 5] or [5, 5, 1] could score
    elif kept_set_length == 3:
        if is_three_of_a_kind(unique_dice_count, dice_counts):
            points = dice_values[0] * 100  # 3 of a kind (face_value * 100)
            if points == 100:  # This is a special case for three ones
                return 300
            else:
                return points
        else:  # Recursively Check for [1, 1, 5] or [5, 5, 1]
            return (calculate_point_set(kept_set[0]) +
                    calculate_point_set(kept_set[1]) +
                    calculate_point_set(kept_set[2]))

    # A kept set of 2 may signify:
    #  * [1, 1]; [1, 5]; [5, 5] are scoring pairs
    elif kept_set_length == 2:  # Handle this case recursively
        return calculate_point_set(kept_set[0]) + calculate_point_set(kept_set[1])

    # A Kept set of 1 may signify either a 1 or a 5
    #  * 1 (100 pts)
    #  * 5 (50 pts)
    elif kept_set_length == 1:
        value = dice_values[0]
        if value == 1:
            return 100
        elif value == 5:
            return 50

    assert False, "Dice set contained non scoring values {0}!".format(kept_set)
