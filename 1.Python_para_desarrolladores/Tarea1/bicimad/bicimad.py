from .urlemt import UrlEMT
import pandas as pd

class BiciMad():

    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year
        self.data_ = BiciMad.get_data(self.month, self.year)


    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:

        # Llamamos a UrlEMT para obtener el fichero csv
        urlemt_ = UrlEMT()
        csvfile = urlemt_.get_csv(month, year)

        # Este es el mismo código de la función get_data del notebook en etapa 1
        data = pd.read_csv(csvfile, sep=";", index_col=['fecha'], parse_dates=True)
        cols_to_keep = ['idBike', 'fleet', 'trip_minutes', 'geolocation_unlock',
                        'address_unlock', 'unlock_date', 'locktype', 'unlocktype',
                        'geolocation_lock', 'address_lock', 'lock_date', 'station_unlock',
                        'unlock_station_name', 'station_lock', 'lock_station_name']
        data = data[cols_to_keep]
        return data


    @property
    def data(self) -> pd.DataFrame:
        return self.data_


    def __str__(self) -> None:
        return f"""
        month: {self.month}
        year: {self.year}
        data: {self.data_.__str__()}
        """
    

    @staticmethod
    def delete_nan_rows(data: pd.DataFrame) -> None:
        data.dropna(how='all', inplace=True)


    @staticmethod
    def float_to_str(data: pd.DataFrame, column: str) -> None:
        if column in data.columns:
            data[column] = data[column].map(lambda x: str(x).split('.')[0])


    def clean(self) -> None:
        """
        Método de instancia que se encarga de realizar la limpieza y 
        transformación del dataframe que representa los datos:
        Modifica el dataframe y no devuelve nada. Realiza las siguientes tareas:
        - Borrado de valores NaN. Borrar las filas con todos sus valores NaN.
        - Cambiar el tipo de datos de las siguientes columnas del dataframe: 
        fleet, idBike, station_lock, station_unlock. Dichas columnas han de ser de tipo str.
        """
        BiciMad.delete_nan_rows(self.data_)
        cols_to_clean = ['fleet', 'idBike', 'station_lock', 'station_unlock']
        for col in cols_to_clean:
            BiciMad.float_to_str(self.data_, col)

        # Remove negative values in trip_minutes column
        self.data_ = self.data_[self.data_['trip_minutes'] >= 0]


    @staticmethod
    def most_popular_stations(data: pd.DataFrame) -> set:
        station_uses = data.groupby("station_unlock").size().sort_values(ascending=False)
        station_uses = station_uses[station_uses == station_uses.max()]
        # Esto nos da el conjunto de indices en donde se alcanza el máximo
        return set(station_uses.index)


    @staticmethod
    def usage_from_most_popular_station(data: pd.DataFrame) -> int:
        station_uses = data.groupby("station_unlock").size().sort_values(ascending=False)
        return station_uses.max()


    def resume(self) -> pd.Series:

        resumedata_ = [self.year, self.month,
                       self.data_.shape[0],
                       sum(self.data_['trip_minutes'])/60,
                       BiciMad.most_popular_stations(self.data_),
                       BiciMad.usage_from_most_popular_station(self.data_)]
        resume_ = pd.Series(resumedata_, index=['year', 
                                         'month', 
                                         'total_uses', 
                                         'total_time', 
                                         'most_popular_station', 
                                         'uses_from_most_popular'])

        return resume_
    

# if __name__ == '__main__':

#     # Ejemplo del notebook de etapa 1:
#     bicimad = BiciMad(2, 23)
#     bicimad.clean()
#     print(bicimad.data.info())
#     print(bicimad.resume())