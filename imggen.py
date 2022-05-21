from ui import ApplyHueOffset
from PIL import Image
import matplotlib.colors as clr

def SegmentUnitIntoList(n: int) -> list:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got {n}")
    legth: float = (1 / n) if n > 1 else 0
    result = [legth * i for i in range(n)]
    return result

def GetRGBColor(hue: float, saturation: float, value: float):
                                   # 0 to 1
    rgbFloat = clr.hsv_to_rgb((hue, saturation, value))
    result = tuple(int(v * 255) for v in rgbFloat)
    return result

def DrawLineOfSquares(image, x: int, y: int, squareSize: int, squareBorder: int, squares: int, skipped: list, squareColor: tuple, skippedColor: tuple):
    for squareIndex in range(squares):
        color = skippedColor if squareIndex in skipped else squareColor
        for squareXPixel in range(squareSize):
            for squareYPixel in range(squareSize):
                image.putpixel((x + squareIndex * (squareSize + squareBorder) + squareXPixel, y + squareYPixel), color)

def NewImage(sizeX: int, sizeY: int, backgroundColor=(255, 255, 255)):
    return Image.new('RGB', (sizeX, sizeY), backgroundColor)

def Draw():
    # img = Image.new('RGB', (500, 500), (255, 255, 255))
    initialX = 200
    initialY = 150
    rows = 10
    rowsYSpacing = 2
    categories = 5
    categoriesYSpacing = 5

    sqrSize = 20
    sqrBorder = 1
    days = 15

    img = NewImage(days * (sqrSize + sqrBorder) + initialX, rows * (rowsYSpacing + sqrSize + sqrBorder) + (categories - 1) * (categoriesYSpacing - rowsYSpacing) + initialY)
    DrawLineOfSquares(img, 2 * sqrSize, 2 * sqrSize, sqrSize, sqrBorder, days, [5, 10, 13], GetRGBColor(0.5, 0.75, 1), (150, 150, 150))
    img.show()
    img.save(r'assets\data\test.png')

# def NewImg():
#     img = Image.new('RGB', (500, 500), (255, 255, 255))
#     sqr = 20
#     sqrs = 10
#     border = 1
#     rows = 20
#     distanceFromBorder = 3 * sqr
#     colors = SegmentUnitIntoList(rows)
#     for r in range(rows):
#         borderYOffset = border * r
#         nThYSquare = r * sqr
#         for k in range(sqrs):
#             borderXOffset = border * k
#             nThXSquare = k * sqr
#             for i in range(sqr):
#                 for j in range(sqr):
#                     img.putpixel((distanceFromBorder + nThXSquare + borderXOffset + i, distanceFromBorder + borderYOffset + nThYSquare + j), GetRGBColor(colors[r]))
#     img.save(r'assets\data\test.png')
#     return img