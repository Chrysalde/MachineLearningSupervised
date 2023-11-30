# This file is not a main script
if __name__ == '__main__':
    print("[signo:utilities] -- Error --")
    exit(1)

def parse_type(value: str, /) -> str | int | float:
    try:
        return int(value)
    except:
        pass
    try:
        return float(value)
    except:
        return value