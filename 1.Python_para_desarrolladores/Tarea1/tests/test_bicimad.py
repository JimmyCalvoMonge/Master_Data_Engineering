from bicimad import *
import pytest

"""
Testing resume from BiciMad
"""

# Continue ====> Add more tests


@pytest.mark.parametrize(
      "month, year, expected_uses", [
          (2, 23, 2189),
      ]
)

def test_uses_from_most_popular(month, year, expected_uses):
    bicimad = BiciMad(month, year)
    bicimad.clean()
    assert bicimad.resume()['uses_from_most_popular'] == expected_uses
