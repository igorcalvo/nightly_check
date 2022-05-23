from PIL import Image, ImageFont, ImageDraw
import matplotlib.colors as clr

from utils import FlattenList, AlignRight
from ui import ApplyHueOffset

fontFamilies = {
    "consolas": r"assets\fonts\consola.ttf",
    "roboto": r"assets\fonts\Roboto-Bold.ttf",
    "liberation": r"assets\fonts\LiberationMono-Bold.ttf",
}

def SegmentUnitIntoList(n: int) -> list:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got {n}")
    length: float = (1 / n) if n > 1 else 0
    result = [length * i for i in range(n)]
    return result

def GetRGBColor(hue: float, saturation: float, value: float):
                                   # 0 to 1
    rgbFloat = clr.hsv_to_rgb((hue, saturation, value))
    result = tuple(int(v * 255) for v in rgbFloat)
    return result

def DrawLineOfSquares(image, position: tuple, squareSize: int, squareBorder: int, squares: int, skipped: list, squareColor: tuple, skippedColor: tuple):
    for squareIndex in range(squares):
        color = skippedColor if squareIndex in skipped else squareColor
        for squareXPixel in range(squareSize):
            for squareYPixel in range(squareSize):
                image.putpixel((position[0] + squareIndex * (squareSize + squareBorder) + squareXPixel, position[1] + squareYPixel), color)

def NewImage(sizeX: int, sizeY: int, backgroundColor=(255, 255, 255)):
    return Image.new('RGB', (sizeX, sizeY), backgroundColor)

# 6 pixels / char + 1 @ 12
def Write(image, position: tuple, text: str, color: tuple, fontFamily: str = "consolas", size: int = 12):
    draw = ImageDraw.Draw(image)
    draw.text(
        position,
        text,
        color,
        font=ImageFont.truetype(fontFamilies[fontFamily], size)
    )

def TextListMaxLenToPixels(textList: list, fontSizeLength: int = 6, fontSizeSpacing: int = 1) -> int:
    return max([len(text) for text in textList]) * (fontSizeLength + fontSizeSpacing)

def GenerateYPositions(initialPosition: tuple, length: int, spacing: int, number: int) -> tuple:
    positions = [(initialPosition[0], initialPosition[1] + (length + spacing) * n) for n in range(number)]
    return positions, positions[-1][1] + length + spacing - initialPosition[1]

def WriteFooter(image, position: tuple, squareSize: int, squareBorder: int, squares: int, latestDate: str):
    daysOfTheWeek = "SMTWTFS"
    # daysOfTheWeek = "日月火水木金土"

def WriteAll(image, categories: list, headerList: list, position: tuple, sqrSize: int, sqrBorder: int):
    flatHeaderList = FlattenList(headerList)
    maxXDelta = TextListMaxLenToPixels(flatHeaderList)
    maxHeaderLen = max([len(h) for h in flatHeaderList])
    maxCategoryLen = max([len(c) for c in categories])

    textSquaresXSpacing = int(0.5 * sqrSize)
    textSquaresYOffset = int(0.25 * sqrSize)

    categoryYSpacing = int(2 * sqrSize)
    categoryTextXOffset = int(0.3 * sqrSize)
    categoryTextYOffset = int(1.2 * sqrSize)

    initialPos = [position[0], position[1]]
    for categoryIndex, category in enumerate(categories):
        categoryPositions, nextCategoryPosition = GenerateYPositions((initialPos[0], initialPos[1]), sqrSize, 2, len(headerList[categoryIndex]))
        Write(image,
              (initialPos[0] + categoryTextXOffset, categoryPositions[0][1] - categoryTextYOffset),
              AlignRight(category.upper(), maxCategoryLen),
              (0, 0, 0),
              "liberation",
              12)
        for headerIndex, header in enumerate(headerList[categoryIndex]):
            Write(image,
                  categoryPositions[headerIndex],
                  AlignRight(header, maxHeaderLen),
                  (0, 0, 0))
            DrawLineOfSquares(image,
                              (initialPos[0] + maxXDelta + textSquaresXSpacing,
                               categoryPositions[headerIndex][1] - textSquaresYOffset),
                              sqrSize,
                              sqrBorder,
                              15,
                              [5, 10, 13],
                              GetRGBColor(0.5, 0.75, 1),
                              (150, 150, 150))
        initialPos[1] = initialPos[1] + nextCategoryPosition + categoryYSpacing

def Draw(categories: list, header: list):
    print("categories", categories)
    print("header", header)
    initialX = 200
    initialY = 500
    rows = 10
    rowsYSpacing = 2
    categoriesLength = 5
    categoriesYSpacing = 5

    sqrSize = 20
    sqrBorder = 1
    days = 15

    img = NewImage(days * (sqrSize + sqrBorder) + initialX, rows * (rowsYSpacing + sqrSize + sqrBorder) + (categoriesLength - 1) * (categoriesYSpacing - rowsYSpacing) + initialY)
    # DrawLineOfSquares(img, (2 * sqrSize, 2 * sqrSize), sqrSize, sqrBorder, days, [5, 10, 13], GetRGBColor(0.5, 0.75, 1), (150, 150, 150))
    WriteAll(img, categories, header, (50, 50), sqrSize, sqrBorder)
    img.show()
    img.save(r'assets\data\test.png')