import pandas as pd


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
            result_id = list(df.stop_id)[index]
    return result_id
