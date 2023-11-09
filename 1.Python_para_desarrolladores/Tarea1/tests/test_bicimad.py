from bicimad import *
import pytest


"""
Testing get_url from UrlEMT
"""

@pytest.mark.parametrize(
      "month, year, expected_url", [
          (2, 23, 'https://opendata.emtmadrid.es//getattachment/7a88cb04-9007-4520-88c5-a94c71a0b925/trips_23_02_February-csv.aspx'),
          (12, 22, 'https://opendata.emtmadrid.es//getattachment/34b933e4-4756-4fed-8d5b-2d44f7503ccc/trips_22_12_December-csv.aspx'),
          (10, 21, 'https://opendata.emtmadrid.es//getattachment/51ba4be6-596f-41d3-8bab-634c4be569c5/trips_21_10_October-csv.aspx'),
      ]
)

def test_get_url(month, year, expected_url):
    urlemt = UrlEMT()
    assert urlemt.get_url(month, year) == expected_url


@pytest.mark.parametrize(
      "month, year", [
          (2, 24),
          (13, 24),
          ]
)

def test_get_url_out_of_bounds(month, year):
    with pytest.raises(ValueError, match="""Month and year need to be integers
                between 1 and 12 and 21 and 23 respectively"""):   
        urlemt = UrlEMT()
        _ = urlemt.get_url(month, year)


@pytest.mark.parametrize(
      "month, year", [
          (5, 23),
          ]
)

def test_get_url_not_available(month, year):
    with pytest.raises(ValueError, match="No link available for this month-year combination"):   
        urlemt = UrlEMT()
        _ = urlemt.get_url(month, year)

"""
Testing most_popular_station from BiciMad
"""

@pytest.mark.parametrize(
      "month, year, expected_station", [
          (2, 23, {"'Plaza de la Cebada nº 16 '"}),
          (12, 22, {"'Calle Valencia nº 1'"})
      ]
)

def test_most_popular_station(month, year, expected_station):
    bicimad = BiciMad(month, year)
    bicimad.clean()
    assert bicimad.resume()['most_popular_station'] == expected_station


"""
Testing uses_from_most_popular from BiciMad
"""

@pytest.mark.parametrize(
      "month, year, expected_uses", [
          (2, 23, 2189),
          (12, 22, 3144)
      ]
)

def test_uses_from_most_popular(month, year, expected_uses):
    bicimad = BiciMad(month, year)
    bicimad.clean()
    assert bicimad.resume()['uses_from_most_popular'] == expected_uses


"""
Testing clean method from BiciMad
"""

@pytest.mark.parametrize(
      "month, year, expected_full_rows, expected_cleaned_rows", [
          (2, 23, 336988, 168491),
      ]
)
# ==== #
# Atención: hay 3 filas con trip_minutes < 0, las hemos eliminado en el método clean de la clase BiciMad
# No las eliminamos en el notebook original de la etapa 1 porque no estaba en las instrucciones
# Por tanto, en el notebook de la etapa 1 tenemos 168494 filas después del dropna, y aquí deberíamos tener 168491.

def test_clean(month, year, expected_full_rows, expected_cleaned_rows):
    bicimad = BiciMad(month, year)
    obtained_full_rows = bicimad.data.shape[0]
    bicimad.clean()
    obtained_cleaned_rows = bicimad.data.shape[0]
    assert obtained_full_rows == expected_full_rows and obtained_cleaned_rows == expected_cleaned_rows


"""
Testing datatypes from BiciMad
"""

@pytest.mark.parametrize(
      "month, year", [
          (2, 23),
      ]
)

def test_index_datetime(month, year):
    bicimad = BiciMad(month, year)
    bicimad.clean()
    assert bicimad.data.index.inferred_type == 'datetime64'


@pytest.mark.parametrize(
      "month, year, expected_datatypes", [
          (2, 23, {'idBike': 'object', 
                   'fleet': 'object', 
                   'trip_minutes': 'float64', 
                   'geolocation_unlock': 'object', 
                   'address_unlock': 'object', 
                   'unlock_date': 'object', 
                   'locktype': 'object', 
                   'unlocktype': 'object', 
                   'geolocation_lock': 'object', 
                   'address_lock': 'object', 
                   'lock_date': 'object', 
                   'station_unlock': 'object', 
                   'unlock_station_name': 'object', 
                   'station_lock': 'object', 
                   'lock_station_name': 'object'}),
      ]
)

def test_datatypes(month, year, expected_datatypes):
    bicimad = BiciMad(month, year)
    bicimad.clean()
    assert bicimad.data.dtypes.apply(lambda x: x.name).to_dict() == expected_datatypes

