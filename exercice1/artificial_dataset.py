# This allows imports from the parent directory
import sys
sys.path.append('..')
from libs.utilities import mkdir
from time import time

def generate_dataset(*, folder: str = '.', filename: str = 'artificial_dataset.csv'):
    r"""Generates a brand new random dataset for us to play with.

    Explicit Parameters:
    --------------------
    folder : str = '.'
        The path to the folder that shall contain the file.

    filename : str = 'artificial_dataset.csv'
        The name of the file to create.

    Notes:
    -----
    The data within the dataset created will always be separated by semi-colon.
    """

    # Create the folder.
    mkdir(folder)

    # Create and open the file for writing
    file = open(f"{folder}/{filename}", "w")

    # Write to the file
    file.write("N/A;N/A")

    # Close the file
    file.close()

if __name__ == '__main__':
    print("[EX1] Generating dataset...")
    start = time()
    generate_dataset()
    print(f"[EX1] Done - {(time() - start):0.4f}s")
