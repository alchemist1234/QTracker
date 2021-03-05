import math
import re
from typing import Set, Tuple


def split_indexes_text(text: str) -> Set[int]:
    """
    将索引字符串分割成索引集合
    ','和' '为分隔符
    索引支持'-'连续选择
    :param text: 索引字符串
    :return: 索引集合
    """
    arr = re.split('[, ]', text)
    indexes = set()
    for i in arr:
        pos = i.find('-')
        if pos > 0:
            left = i[:pos]
            right = i[pos + 1:]
            if left.isdecimal() and right.isdecimal():
                min_index = min(int(left), int(right))
                max_index = max(int(left), int(right))
                indexes.update(range(min_index, max_index + 1))
        else:
            if i.isdecimal():
                indexes.add(int(i))
    return indexes


def hsv2rgb(h: float, s: float, v: float) -> Tuple[float, float, float]:
    """
    HSV轨RGB
    :param h: Hue
    :param s: Saturation
    :param v: Value
    :return: (red, green, blue)
    """
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return b, g, r
