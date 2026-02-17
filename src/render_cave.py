from PIL import Image, ImageDraw, ImageFont
from cave_gen import make_cave


def gen_img_cave(row, col, my_cave) -> None:
    """
    Генерация изображения пещеры с использованием библиотеки PIL (Python Imaging Library).
    Отрисовка просиходит прямоуголниками черного (мертвые клетки) и белого цвета (живые клетки).
    Итоговое изображени сохраняется в image/cave.png

    :param row: высота пещеры
    :param col: ширина пещеоы
    :param my_cave: поле пещеры
    """
    img = Image.new("RGB", (500, 500), "white")
    # for line in my_cave:
    #     print(*line)
    i_draw = ImageDraw.Draw(img)
    for i in range(row):
        for j in range(col):
            color = "black" if my_cave[i][j] else 'white'
            i_draw.rectangle(
                (
                    j * (500 // col),
                    i * (500 // row),
                    (500 // col) * j + (500 // col),
                    (500 // row) * i + (500 // row)
                ),
                fill=color,
            )
    img.save(f"image/cave.png")


if __name__ == "__main__":
    lim_b, lim_d, row, col = 5, 3, 50, 50
    gen_img_cave(row, col, make_cave(lim_b, lim_d, row, col))
    image = Image.open("image/cave.png")
    image.show()
