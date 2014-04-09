
# Test cases for the parkle utils

from random import randint

from parkle import utils as parkle_utils


def test_nested_dice_expected():
    """ Test that some statically defined dice lists that are
    passed in to the nested_dice() util return an expected nested result
    """
    dice_roll = [3, 5, 5, 6, 6, 6]
    nested_dice_roll = parkle_utils.nested_dice(dice_roll)
    assert (3, 1) in nested_dice_roll, "There should be tuple (3, 1) in the nested dice roll."
    assert (5, 2) in nested_dice_roll, "There should be tuple (5, 2) in the nested dice roll."
    assert (6, 3) in nested_dice_roll, "There should be tuple (6, 3) in the nested dice roll."

    dice_roll = [1, 2, 2, 2, 2, 2]
    nested_dice_roll = parkle_utils.nested_dice(dice_roll)
    assert (1, 1) in nested_dice_roll, "There should be tuple (1, 1) in the nested dice roll."
    assert (2, 5) in nested_dice_roll, "There should be tuple (2, 5) in the nested dice roll."
    assert (6, 3) not in nested_dice_roll, "There should not be tuple (6, 3) in the nested dice roll."


def test_nested_dice_randomized():
    """ Test that the list passed in to nested_dice() returns a resulting
    nested list that when deconstructed matches the list that was passed in.
    """
    for x in range(0, 10):  # Run this test 10 times
        dice = [randint(1, 6) for x in range(0, randint(0, 6))]
        nested_dice = parkle_utils.nested_dice(dice)
        # Deconstruct the nested list

        deconstructed_dice = parkle_utils.flatten_nested_dice(nested_dice)

        assert len(dice) == len(deconstructed_dice), \
            "Length of deconstructed dice list does not match original input"
        assert sorted(dice) == sorted(deconstructed_dice), \
            "Sorted dice lists should match equality"


def test_flatten_nested_dice():
    """ Test that the flatten nested dice utility function makes right
     for known values.
    """
    nested_dice = [(2, 4), (1, 1), (3, 1)]
    expected_value = [2, 2, 2, 2, 1, 3]

    actual_result = parkle_utils.flatten_nested_dice(nested_dice)

    assert len(expected_value) == len(actual_result), \
        "Length of deconstructed dice list does not match original input"
    assert sorted(expected_value) == sorted(actual_result), \
        "Sorted dice lists should match equality"


def test_nested_kept_set():
    """ Test that the nested_kept_set utility returns a proper
     nested dictionary based on the lists passed in.
    """
    kept_set = [1, 1, 2, 2, 5, 5]
    nested_kept_set = parkle_utils.nested_kept_set(kept_set)

    assert nested_kept_set[1] == 2, "Expected a count of (2) dice with face 1"
    assert nested_kept_set[2] == 2, "Expected a count of (2) dice with face 2"
    assert nested_kept_set[5] == 2, "Expected a count of (2) dice with face 5"

    kept_set = [2, 2, 2, 2, 5, 5]
    nested_kept_set = parkle_utils.nested_kept_set(kept_set)

    assert nested_kept_set[2] == 4, "Expected a count of (4) dice with face 2"
    assert nested_kept_set[5] == 2, "Expected a count of (2) dice with face 5"


def test_dice_roll():
    """ Test a randomized number of dice rolls match the number of
     dice requested in the roll, and that the values are each within [1, 6]
    """
    # note a random here causes problems for testing anything
    for x in range(0, 10):  # Run this 10 times
        dice_roll = parkle_utils.dice_roll(randint(1, 6))


        # assert len(dice) == len(deconstructed_dice), \
        #     "Length of deconstructed dice list does not match original input"


def test_validate_dice_in_range():
    """ Test that validate dice in range utility works.
    """
    dice_in_range = [1, 2, 3, 4, 5, 6]
    assert parkle_utils.validate_dice_in_range(dice_in_range), "Expected dice set are within range!"

    dice_out_of_range = [2, 3, 4, 5, 6, 7]
    try:
        parkle_utils.validate_dice_in_range(dice_out_of_range)
    except AssertionError:
        pass
    else:
        assert False, "Expected dice set are out of range!"


def test_is_three_pair():
    """ Test some known cases for the is_three_pair utility function.
    """
    kept_set_valid = [2, 2, 3, 3, 5, 5]
    nested_set = parkle_utils.nested_kept_set(kept_set_valid)
    unique_dice_count = len(nested_set)
    assert parkle_utils.is_three_pair(unique_dice_count, nested_set), "Expected set is three pairs!"

    kept_set_invalid = [1, 2, 3, 3, 5, 5]
    nested_set = parkle_utils.nested_kept_set(kept_set_invalid)
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_three_pair(unique_dice_count, nested_set), "Expected set is not three pairs!"


def test_is_three_of_a_kind():
    """ Test some 3-kept set dice rolls for 3 of a kind.
    """
    kept_set_valid = [6, 6, 6]
    nested_set = parkle_utils.nested_kept_set(kept_set_valid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert parkle_utils.is_three_of_a_kind(unique_dice_count, dice_counts), "Expected set is three of a kind!"

    kept_set_invalid = [6, 5, 6]
    nested_set = parkle_utils.nested_kept_set(kept_set_invalid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_three_of_a_kind(unique_dice_count, dice_counts), "Expected set is not three of a kind!"


def test_is_four_of_a_kind():
    """ Test some 4-kept set dice rolls for 3 of a kind.
    """
    kept_set_valid = [2, 2, 2, 2]
    nested_set = parkle_utils.nested_kept_set(kept_set_valid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert parkle_utils.is_four_of_a_kind(unique_dice_count, dice_counts), "Expected set is four of a kind!"

    kept_set_invalid = [1, 2, 5, 6]
    nested_set = parkle_utils.nested_kept_set(kept_set_invalid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_four_of_a_kind(unique_dice_count, dice_counts), "Expected set is not four of a kind!"


def test_is_five_of_a_kind():
    """ Test some 5-kept set dice rolls for 3 of a kind.
    """
    kept_set_valid = [2, 2, 2, 2, 2]
    nested_set = parkle_utils.nested_kept_set(kept_set_valid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert parkle_utils.is_five_of_a_kind(unique_dice_count, dice_counts), "Expected set is five of a kind!"

    kept_set_invalid = [1, 2, 5, 6, 6]
    nested_set = parkle_utils.nested_kept_set(kept_set_invalid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_five_of_a_kind(unique_dice_count, dice_counts), "Expected set is not five of a kind!"


def test_is_six_of_a_kind():
    """ Test some 6-kept set dice rolls for 3 of a kind.
    """
    kept_set_valid = [4, 4, 4, 4, 4, 4]
    nested_set = parkle_utils.nested_kept_set(kept_set_valid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert parkle_utils.is_six_of_a_kind(unique_dice_count, dice_counts), "Expected set is six of a kind!"

    kept_set_invalid = [1, 2, 2, 5, 6, 6]
    nested_set = parkle_utils.nested_kept_set(kept_set_invalid)
    dice_counts = nested_set.itervalues()
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_six_of_a_kind(unique_dice_count, dice_counts), "Expected set is not six of a kind!"


def test_is_straight_six():
    """ Test some 6-kept-set matches a straight-six or not.
    """
    kept_valid_straight = [4, 5, 6, 1, 2, 3]
    nested_set = parkle_utils.nested_kept_set(kept_valid_straight)
    unique_dice_count = len(nested_set)

    assert parkle_utils.is_straight_six(unique_dice_count, nested_set), "Expected set is a straight 6 dice!"

    kept_invalid_straight = [1, 2, 3, 4, 5, 5]
    nested_set = parkle_utils.nested_kept_set(kept_invalid_straight)
    unique_dice_count = len(nested_set)
    assert not parkle_utils.is_straight_six(unique_dice_count, nested_set), "Expected set is not a straight 6 dice!"


def test_is_two_sets_of_three():
    """ Test some 6-kept-set matches for two sets of three.
    """
    kept_valid_double_set = [2, 3, 2, 3, 2, 3]
    nested_set = parkle_utils.nested_kept_set(kept_valid_double_set)
    unique_dice_count = len(nested_set)
    dice_counts = nested_set.itervalues()
    assert parkle_utils.is_two_sets_of_three(unique_dice_count, dice_counts), "Expected a double set of threes!"

    kept_invalid_double_set = [2, 1, 2, 3, 2, 3]
    nested_set = parkle_utils.nested_kept_set(kept_invalid_double_set)
    unique_dice_count = len(nested_set)
    dice_counts = nested_set.itervalues()
    assert not parkle_utils.is_two_sets_of_three(unique_dice_count, dice_counts), "Expected no double set of threes!"


def test_is_four_of_kind_and_pair():
    """ Test some 6-kept-set matches a four of a kind and a pair.
    """
    kept_valid_set = [2, 2, 2, 2, 5, 5]
    nested_set = parkle_utils.nested_kept_set(kept_valid_set)
    unique_dice_count = len(nested_set)
    dice_counts = nested_set.itervalues()
    assert parkle_utils.is_four_of_kind_and_pair(unique_dice_count, dice_counts), "Expected a 4-set and a double!"

    kept_valid_set = [1, 2, 2, 2, 5, 5]
    nested_set = parkle_utils.nested_kept_set(kept_valid_set)
    unique_dice_count = len(nested_set)
    dice_counts = nested_set.itervalues()
    assert not parkle_utils.is_four_of_kind_and_pair(unique_dice_count, dice_counts), "Expected invalid set!"


def test_scoring_six_of_kind():
    """ Test case of base scoring a set that is six of a kind.
    The points awarded for six of a kind are 3000.
    """
    kept_three_pair = [1, 1, 1, 1, 1, 1]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 3000, "Expected to be awarded 3000 points."


def test_scoring_two_sets_of_three():
    """ Test case of base scoring a set that is two sets of three.
    The points awarded for two 3-sets are 2500.
    """
    two_set_of_three = [2, 2, 2, 6, 6, 6]
    points = parkle_utils.calculate_point_set(two_set_of_three)
    assert points == 2500, "Expected to be awarded 2500 points."


def test_scoring_straight_six():
    """ Test case of base scoring a set that is straight six, 1-6.
    The points awarded for three pair are 1500.
    """
    kept_three_pair = [1, 2, 3, 4, 5, 6]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 1500, "Expected to be awarded 1500 points."


def test_scoring_set_three_pair():
    """ Test case of base scoring a set that is three pair.
    The points awarded for three pair are 1500.
    """
    kept_three_pair = [1, 1, 3, 3, 5, 5]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 1500, "Expected to be awarded 1500 points."


def test_scoring_four_of_kind_and_pair():
    """ Test case of base scoring a set that is four of a kind and a pair.
    The points awarded for this combo are 1500.
    """
    kept_set = [2, 2, 2, 2, 6, 6]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 1500, "Expected to be awarded 1500 points."

    kept_set = [1, 1, 1, 1, 5, 5]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 1500, "Expected to be awarded 1500 points."


def test_scoring_five_of_kind():
    """ Test case of base scoring a set that is five of a kind.
    The points awarded for five of a kind are 2000.
    """
    kept_three_pair = [5, 5, 5, 5, 5]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 2000, "Expected to be awarded 2000 points."

    # 2000 + 50 = 2050  #  Test the recursive 6 kept 5-set
    kept_three_pair = [3, 3, 3, 3, 3, 5]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 2050, "Expected to be awarded 2050 points."

    # 2000 + 100 = 2100  #  Test the recursive 6 kept 5-set
    kept_three_pair = [3, 3, 3, 3, 3, 1]
    points = parkle_utils.calculate_point_set(kept_three_pair)
    assert points == 2100, "Expected to be awarded 2100 points."


def test_scoring_four_of_kind():
    """ Test case of scoring four of a kind from various sized scoring sets.
    The points awarded for four of a kind are 1000.
    """
    kept_four_of_kind = [4, 4, 4, 4]
    points = parkle_utils.calculate_point_set(kept_four_of_kind)
    assert points == 1000, "Expected to be awarded 1000 points."

    # 1000 + 100 = 1100  # Test the recursive 5 kept 4-set
    kept_four_and_one = [4, 4, 4, 4, 1]
    points = parkle_utils.calculate_point_set(kept_four_and_one)
    assert points == 1100, "Expected to be awarded 1100 points."

    # 1000 + 100 + 50 = 1150  # Test the recursive 6 kept 4-set
    kept_four_and_too = [4, 4, 4, 4, 1, 5]
    points = parkle_utils.calculate_point_set(kept_four_and_too)
    assert points == 1150, "Expected to be awarded 1150 points."

    # 1000 + ??? = AssertionError  # Test the bogus set case
    kept_four_and_two = [4, 4, 4, 4, 2]
    try:
        points = parkle_utils.calculate_point_set(kept_four_and_two)
    except AssertionError:
        pass
    else:
        assert False, "Expected this to not be a scoring set Assertion."


def test_scoring_three_of_kind():
    """ Test cases of scoring three of a kind from various sized scoring sets.
    The points awarded for three of a kind are 300 for 1s, or 100*face_value.
    Additional points can be gained with conjunction of 1s and 5s.
    """
    kept_four_of_kind = [1, 1, 1]
    points = parkle_utils.calculate_point_set(kept_four_of_kind)
    assert points == 300, "Expected to be awarded 300 points."

    kept_four_of_kind = [4, 4, 4]
    points = parkle_utils.calculate_point_set(kept_four_of_kind)
    assert points == 400, "Expected to be awarded 400 points."

    # 400 + 100 = 500  # Test the recursive 4 kept 3-set
    kept_three_and_one = [4, 4, 4, 1]
    points = parkle_utils.calculate_point_set(kept_three_and_one)
    assert points == 500, "Expected to be awarded 500 points."

    # 400 + 100 + 50 = 550  # Test the recursive 5 kept 3-set
    kept_four_and_too = [4, 4, 4, 1, 5]
    points = parkle_utils.calculate_point_set(kept_four_and_too)
    assert points == 550, "Expected to be awarded 550 points."

    # 1000 + ??? = AssertionError  # Test the bogus set case
    kept_four_and_two = [4, 4, 4, 2, 2]
    try:
        points = parkle_utils.calculate_point_set(kept_four_and_two)
    except AssertionError:
        pass
    else:
        assert False, "Expected this to not be a scoring set Assertion."


def test_scoring_ones_and_fives():
    """ Test cases of scoring various combinations of 1s and 5s.
    """
    # 100 + 50 + 100 + 50 = 300
    kept_set = [1, 5, 1, 5]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 300, "Expected to be awarded 300 points."

    # 50 + 100 + 50 = 200
    kept_set = [5, 1, 5]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 200, "Expected to be awarded 200 points."

    # 100 + 50 = 150
    kept_set = [1, 5]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 150, "Expected to be awarded 150 points."

    # 100
    kept_set = [1]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 100, "Expected to be awarded 100 points."

    # 50
    kept_set = [5]
    points = parkle_utils.calculate_point_set(kept_set)
    assert points == 50, "Expected to be awarded 50 points."
