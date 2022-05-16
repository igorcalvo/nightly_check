from ui import ApplyHueOffset
from PIL import Image

import matplotlib.colors as clr

def SegmentUnitIntoList(n: int) -> list:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got {n}")
    legth: float = (1 / n) if n > 1 else 0
    result = [legth * i for i in range(n)]
    return result

def GetColor(hue: float):
                                # 0 to 1
    value = clr.hsv_to_rgb((hue, 0.75, 1))
    result = tuple(int(v * 255) for v in value)
    return result

def newImg():
    img = Image.new('RGB', (500, 500), (255, 255, 255))
    sqr = 20
    sqrs = 10
    border = 1
    rows = 20
    distanceFromBorder = 3 * sqr
    colors = SegmentUnitIntoList(rows)
    for r in range(rows):
        borderYOffset = border * r
        nThYSquare = r * sqr
        for k in range(sqrs):
            borderXOffset = border * k
            nThXSquare = k * sqr
            for i in range(sqr):
                for j in range(sqr):
                    img.putpixel((distanceFromBorder + nThXSquare + borderXOffset + i, distanceFromBorder + borderYOffset + nThYSquare + j), GetColor(colors[r]))
    img.save(r'assets\data\test.png')
    return img

def Draw():
    img = newImg()
    img.show()