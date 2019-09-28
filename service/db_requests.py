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


def get_picture_by_id(id_):
    df = pd.read_csv("../station_pictures_data.csv", sep=',')
    for index, stop_id in enumerate(list(df.stop_id)):
        if id_ == stop_id:
            return df.iloc[index].images


class Event:
    def __init__(self, stop_id, stop_name, event_name, description, categories, url):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.event_name = event_name
        self.description = description
        self.categories = categories
        self.url = url


def get_event_list_by_id(id_):
    df = pd.read_csv("../events_description_df.csv", sep=',')
    event_list = []
    stop_name = list(df.stop_name)
    event_name = list(df.event_name)
    description = list(df.description)
    categories = list(df.categories)
    url = list(df.url)

    for index, stop_id in enumerate(list(df.stop_id)):
        if id_ == stop_id:
            event_list.append(Event(stop_id, stop_name[index],
                                    event_name[index], description[index],
                                    categories[index], url[index]))
    return event_list


def select_random_cities(quantity=5, file_name="../train_stations_data.csv"):
    """
    :param quantity: number of cities
    :return: random ids of cities
    """
    result_id_list = []
    df = pd.read_csv(file_name, sep=',')
    for i in range(quantity):
        rand_number = randint(0, df.shape[0] - 1)
        result_id_list.append(df.iloc[rand_number].stop_id)
    return result_id_list

