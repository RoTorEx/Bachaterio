import math


def convert_size(size_bytes):
    size_name = ("b", "kb", "mb", "gb", "tb", "pb", "eb", "zb", "yb")

    if size_bytes == 0:
        return "0b"

    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return "%s%s" % (s, size_name[i])
