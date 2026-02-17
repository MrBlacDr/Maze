from PIL import Image, ImageDraw, ImageFont
from maze_genv3 import make_maze

board_width = 2


def gen_img_maze(w: int, h: int, maze: list) -> None:
    """
    Генерация изображения лабиринта с использованием библиотеки PIL (Python Imaging Library).
    Отрисовка просиходит прямоуголниками черного (границы и стенки) и белого цвета.
    Итоговое изображени сохраняется в image/maze.png

    :param w: ширина лабиринта
    :param h: высота лабиринта
    :param maze: матрица - сам лабиринт
    """
    img = Image.new("RGB", (500, 500), "white")
    row, col = h, w
    i_draw = ImageDraw.Draw(img)
    for i in range(row):
        for j in range(col):
            if maze[i][j].down_wall:
                i_draw.rectangle(
                    (
                        j * (500 // col),
                        (i + 1) * (500 // row) - maze[i][j].down_wall,
                        (j + 1) * (500 // col),
                        (i + 1) * (500 // row)
                    ),
                    fill="black",
                )
            if maze[i][j].right_wall:
                i_draw.rectangle(
                    (
                        (j + 1) * (500 // col) - maze[i][j].right_wall,
                        i * (500 // row),
                        (j + 1) * (500 // col),
                        (i + 1) * (500 // row)
                    ),
                    fill="black",
                )
    i_draw.rectangle(
        (0, 0, 500, board_width),
        fill="black")
    i_draw.rectangle(
        (500 - board_width, 0, 500, 500),
        fill="black")
    i_draw.rectangle(
        (0, 0, board_width, 500),
        fill="black")
    i_draw.rectangle(
        (0, 500 - board_width, 500, 500),
        fill="black")
    img.save(f"image/maze.png")


if __name__ == "__main__":
    gen_img_maze(10, 10, make_maze(10, 10))
    image = Image.open("image/maze.png")
    image.show()
