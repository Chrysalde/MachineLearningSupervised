import os

def mkdir(path: str) -> bool:
    r"""Create a folder if it doesn't already exists.

    Parameters:
    -----------
    path : str
        The path to the folder to create.

    Returns:
    --------
    True if the folder has been successfully created.
    """
    if (not os.path.exists(path)):
        os.mkdir(path)
    return os.path.exists(path)

if __name__ == '__main__':
    exit(1)