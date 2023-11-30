# This file is not a main script
if __name__ == '__main__':
    print("[signo:error] -- Error --")
    exit(1)

class InsufficientPermissionsException(Exception):
    pass

class InvalidIndexException(Exception):
    pass

class MutuallyExclusiveParamtersException(Exception):
    pass