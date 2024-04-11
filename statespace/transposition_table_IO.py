import pickle
import json


def save_transposition_table_to_pickle(table, filename):
    with open(filename, 'wb') as file:
        pickle.dump(table, file)


def save_transposition_table_to_json(table, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(table, file)
    except TypeError as e:
        print(e)
        print(f"Could not serialize the transposition table to {filename}.")
    except FileNotFoundError as e:
        print(e)
        print(f"File {filename} not found. Could not save the transposition table.")


def load_transposition_table_from_pickle(filename):
    try:
        with open(filename, 'rb') as file:
            table = pickle.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if file not found
    return table


def load_transposition_table_from_json(filename):
    try:
        with open(filename, 'r') as file:
            serializable_table = json.load(file)
    except FileNotFoundError as e:
        print(e)
        print(f"File {filename} not found. Returning an empty dict.")
        return {}  # Return an empty dict if file not found
    except json.JSONDecodeError as e:
        print(e)
        print(f"File {filename} is empty or cannot be decoded. Returning an empty dict.")
        return {}
    return serializable_table
