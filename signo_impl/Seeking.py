# This file is not a main script
if __name__ == '__main__':
    print("[signo:Seeking] -- Error --")
    exit(1)

from enum import IntEnum

class Seeking(IntEnum):
    r"""Represents the different starting positions for seeking."""
    FileStart = 0
    CurrentPosition = 1
    FileEnd = 2