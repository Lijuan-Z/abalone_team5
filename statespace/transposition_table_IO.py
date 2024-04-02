import pickle
import json


def save_transposition_table_to_pickle(table, filename):
    with open(filename, 'wb') as file:
        pickle.dump(table, file)


def load_transposition_table_from_pickle(filename):
    with open(filename, 'rb') as file:
        table = pickle.load(file)
    return table


def save_transposition_table_to_json(table, filename):
    # Convert keys or values if necessary (e.g., converting tuple keys to strings)
    serializable_table = {str(key): value for key, value in table.items()}
    with open(filename, 'w') as file:
        json.dump(serializable_table, file)


def load_transposition_table_from_json(filename):
    with open(filename, 'r') as file:
        serializable_table = json.load(file)
    # Convert keys or values back if necessary
    table = {eval(key): value for key, value in serializable_table.items()}
    return table

