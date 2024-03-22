import os.path

from statespace.external import process_folder


if __name__ == "__main__":
    # import os
    # print(os.listdir(os.path.curdir))
    print("Running...")
    process_folder(os.path.join(os.path.abspath(os.path.curdir), "tests"))