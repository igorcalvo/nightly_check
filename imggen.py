from datetime import date, timedelta
from PIL import Image, ImageFont, ImageDraw
import matplotlib.colors as clr

from utils import FlattenList, AlignRight, CycleIndex
from core import GetHeaderData, GetDateArray, GetFailIndexesList, GetExpectedValue

fontFamilies = {
    "consolas": r"assets\fonts\consola.ttf",
    "roboto": r"assets\fonts\Roboto-Bold.ttf",
    "liberation": r"assets\fonts\LiberationMono-Bold.ttf",
    "noto": r"assets\fonts\NotoSansJP-Regular.otf",
}

def SegmentUnitIntoList(n: int, minOffset: float = 0, maxOffset: float = 1) -> list:
    if n <= 0:
        raise Exception(f"SegmentUnitIntoList: n can't be <= 0. Got: {n}")
    elif minOffset >= maxOffset or minOffset < 0 or maxOffset > 1:
        raise Exception(f"SegmentUnitIntoList: Offsets out of range. Got min: {minOffset} and max: {maxOffset}")
    length: float = ((maxOffset - minOffset) / n) if n > 1 else 0
    result = [minOffset + length * i for i in range(n)]
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
    latestDate = (date.today() + timedelta(days=-1)).isoformat()
    # daysOfTheWeek = "STQQSSD"
    # daysOfTheWeek = "MTWTFSS"
    daysOfTheWeek = "月火水木金土日"
    todaysIndex = date.fromisoformat(latestDate).weekday()
    for s in range(squares):
        Write(image,
              (position[0] + s * (squareSize + squareBorder), position[1]),
              CycleIndex(daysOfTheWeek, todaysIndex - squares + s + 1),
              (0, 0, 0),
              "noto")

def WriteAll(image, categories: list, headerList: list, frequencies: list, data, position: tuple, squares: int, sqrSize: int, sqrBorder: int, maxXDelta: int,
             textSquaresXSpacing: int, textSquaresYOffset: int, categoryYSpacing: int, categoryTextOffset: tuple):

    maxHeaderLen = max([len(h) for h in FlattenList(headerList)])
    maxCategoryLen = max([len(c) for c in categories])
    initialPos = [position[0], position[1]]
    footerTextOffset = (12, 6)
    hues = SegmentUnitIntoList(len(categories))
    dateArray = GetDateArray(data, squares)

    for categoryIndex, category in enumerate(categories):
        categoryPositions, nextCategoryPosition = GenerateYPositions((initialPos[0], initialPos[1]), sqrSize, 2, len(headerList[categoryIndex]))
        Write(image,
              (initialPos[0] + categoryTextOffset[0], categoryPositions[0][1] - categoryTextOffset[1]),
              AlignRight(category.upper(), maxCategoryLen),
              (0, 0, 0),
              "liberation",
              12)
        for headerIndex, header in enumerate(headerList[categoryIndex]):
            expectedValue = GetExpectedValue(header, headerList, frequencies)
            headerData = GetHeaderData(data, dateArray, squares, header)
            failList = GetFailIndexesList(headerData)
            # print(header, headerData)
            hueOffset = (hues[1] - hues[0]) / (len(headerList[categoryIndex]) + 1)
            Write(image,
                  categoryPositions[headerIndex],
                  AlignRight(header, maxHeaderLen),
                  (0, 0, 0))
            DrawLineOfSquares(image,
                              (initialPos[0] + maxXDelta + textSquaresXSpacing,
                               categoryPositions[headerIndex][1] - textSquaresYOffset),
                              sqrSize,
                              sqrBorder,
                              squares,
                              failList,
                              # GetRGBColor(0.5, 0.75, 1)
                              # GetRGBColor(hues[categoryIndex], saturations[headerIndex], 1),
                              GetRGBColor(hues[categoryIndex] + headerIndex * hueOffset, 0.85, 1),
                              GetRGBColor(0, 0, 0.75))
        initialPos[1] = initialPos[1] + nextCategoryPosition + categoryYSpacing
        WriteFooter(image,
                    (initialPos[0] + maxXDelta + textSquaresXSpacing + ((sqrSize - footerTextOffset[0]) // 2), initialPos[1] - categoryYSpacing - footerTextOffset[1]),
                    sqrSize,
                    sqrBorder,
                    squares,
                    '')

def GenerateImage(categories: list, header: list, frequencies: list, data):
    flatHeaderList = FlattenList(header)
    print("categories", categories)
    print("header", header)
    print("data len", len(data.index))
    initialX = 75
    initialY = 75
    rows = len(flatHeaderList)
    rowsYSpacing = 2
    categoriesLength = len(categories)

    sqrSize = 20
    sqrBorder = 1
    squares = min([20, len(data.index)])

    maxXDelta = TextListMaxLenToPixels(flatHeaderList)

    textSquaresXSpacing = int(0.5 * sqrSize)
    textSquaresYOffset = int(0.25 * sqrSize)

    categoryYSpacing = int(2 * sqrSize)
    categoryTextOffset = (int(0.3 * sqrSize), int(1.2 * sqrSize))

    img = NewImage(squares * (sqrSize + sqrBorder) + maxXDelta + textSquaresXSpacing + initialX,
                   # rows * (rowsYSpacing + sqrSize + sqrBorder) + (categoriesLength - 1) * (categoryYSpacing - rowsYSpacing) + initialY)
                   rows * (rowsYSpacing + sqrSize + sqrBorder) + (categoriesLength - 1) * (categoryYSpacing + rowsYSpacing) + initialY)
    # DrawLineOfSquares(img, (2 * sqrSize, 2 * sqrSize), sqrSize, sqrBorder, days, [5, 10, 13], GetRGBColor(0.5, 0.75, 1), (150, 150, 150))
    WriteAll(img, categories, header, frequencies, data, (50, 50), squares, sqrSize, sqrBorder,
             maxXDelta, textSquaresXSpacing, textSquaresYOffset, categoryYSpacing, categoryTextOffset)
    # img.show()
    # img.save(r'assets\data\test.png')
    return img