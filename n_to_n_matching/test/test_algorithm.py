"""Tests for the Hospital-Resident algorithm."""

from hypothesis import given
import numpy as np
import pytest

from n_to_n_matching.util import Util
from n_to_n_matching.matching import VolunteerAllocation

@pytest.fixture
def input_guardians():
    return Util.read_yaml_to_dict(base_url, "test_guardians.yaml")

@pytest.fixture
def input_dates():
    return Util.read_yaml_to_dict(base_url, "test_volunteer-dates.yaml")

def test_volunteer_april(input_guardians, input_dates):
    """Test the algorithm produces a valid solution."""
    game = VolunteerAllocation.create_from_dictionaries(
        resident_preferences, hospital_preferences, hospital_capacities
        )    

    matching_table = VolunteerAllocation.solve(input_guardians, input_dates)
    matched_dates = set(matching_table.keys())

    # Assert all input dates are listed in the result.
    assert set(input_dates) == matched_dates
    for date in matched_dates.dates:
        # assert each day 'required_personnel' is met.
        date_input = input_dates["date"]
        assert len(date.assignees) >= date_input

        for assignee in date.assignees:
        # TODO Assert in each date there's no duplicate players.        
            
    matched_guardians = {r for guardians_matched in matching_table.values() for r in guardians_matched}
    for guardian in input_guardians:
        # Assert all input guardians are in the result.
        if guardian.matching:
            assert guardian in matched_guardians
        # Assert non-matched guardian is NOT in the result.            
        else:
            assert guardian not in matched_guardians

        # Assert no guardian is missing in the result.
        # Testing this way is kind of like a duplicate of checking `guardian.matching` but for now do it so..
        assert guardian in matched_guardians

        # TODO Assert guardian is assigned to 1 or more dates.
        assert guardian.dates
