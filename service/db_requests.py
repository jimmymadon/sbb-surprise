import pandas as pd
from random import randint


def get_id_by_location(location):
    """
    :param location: name of the location
    :return: result_id
    -1 == location is not found

    """
    result_id = -1
    df = pd.read_csv("../train_stations_data.csv", sep=',')
    for index, stop_name in enumerate(list(df.stop_name)):
        if location == stop_name:
            result_id = df.iloc[index].stop_id
    return result_id


def get_location_by_id(id_):
    """
    :param id_:
    :return: result_location
    "" == id is not found
    """
    result_location = ""
    df = pd.read_csv("../train_stations_data.csv", sep=',')
    for index, stop_id in enumerate(list(df.stop_id)):
        if id_ == stop_id:
            result_location = df.iloc[index].stop_name
    return result_location


def get_coordinates_by_id(id_):
    df = pd.read_csv("../train_stations_data.csv", sep=',')
    for index, stop_id in enumerate(list(df.stop_id)):
        if id_ == stop_id:
            return df.iloc[index].stop_lat, df.iloc[index].stop_lon


def select_random_cities(quantity=5):
    """
    :param quantity: number of cities
    :return: random ids of cities
    """
    result_id_list = []
    df = pd.read_csv("../train_stations_data.csv", sep=',')
    for i in range(quantity):
        rand_number = randint(0, df.shape[0] - 1)
        result_id_list.append(df.iloc[rand_number].stop_id)
    return result_id_list
