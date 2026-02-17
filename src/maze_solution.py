from render_maze import gen_img_maze
from convertions import convert_from_file
from PIL import Image, ImageDraw


def add_path_to_image(image_to_read: str, row: int, col: int, line: list, image_to_save: str) -> None:
    """
    Функция, рисующая путь поверх имеющейся картинки лабиринта.

    :param image_to_read: путь к картинке с лабиринтом для чтения
    :param row: высота лабиринта
    :param col: ширина лабиринта
    :param line: список координат точек
    :param image_to_save: путь к картинке с нарисованным маршрутом
    """
    shift_x = 500 // col
    shift_y = 500 // row
    image = Image.open(image_to_read)
    draw = ImageDraw.Draw(image)
    for part in line:
        draw.line([part[0][1] * shift_y + shift_y // 2,
                   part[0][0] * shift_x + shift_x // 2,
                   part[1][1] * shift_y + shift_y // 2,
                   part[1][0] * shift_x + shift_x // 2, ],
                  fill='red', width=2)
    image.save(image_to_save)
    # image.save('./image/modified_maze.png')
    # image.show()


def visual(filename) -> None:
    """
    Функция, использованная для отладки алгоритма. Не участвует в поиске решения.

    :param filename: файл, содержащий лабиринт
    """
    h, w, matrix = convert_from_file(filename)
    gen_img_maze(h, w, matrix)
    image = Image.open("image/maze.png")
    image.show()
    flag, path = find_path(matrix, (4, 0), (4, 4), [(4, 0), (4, 0)])
    path = [[path[i], path[i + 1]] for i in range(1, len(path) - 1)]
    print(flag)
    add_path_to_image("image/maze.png", h, w, path, './image/modified_maze.png')


def find_path(maze: list, start: tuple, end: tuple, path: list, not_found=True) -> tuple:
    """
    Рекурсивная функция поиска пути.

    :param maze: матрица лабиринта
    :param start: координаты точки начала
    :param end: координаты конечной точки
    :param path: список координат, куда записывается маршрут
    :param not_found: флаг, сигнализирующий о завершении поиска
    :return: кортеж из флага, что найден путь, и список координат самого пути
    """
    if start == end:
        not_found = False
        return not_found, path + [end]
    i = start[0]
    j = start[1]
    # можно идти налево
    if j > 0 and not maze[i][j - 1].right_wall:
        coord = (i, j - 1)
        if path[-2] != coord and not_found:
            path.append(coord)
            not_found, path = find_path(maze, coord, end, path, not_found)
            if not not_found:
                return not_found, path
    # можно идти вверх
    if i > 0 and not maze[i - 1][j].down_wall:
        coord = (i - 1, j)
        if path[-2] != coord and not_found:
            path.append(coord)
            not_found, path = find_path(maze, coord, end, path, not_found)
            if not not_found:
                return not_found, path
    # можно идти направо
    if j < len(maze[0]) - 1 and not maze[i][j].right_wall:
        coord = (i, j + 1)
        if path[-2] != coord and not_found:
            path.append(coord)
            not_found, path = find_path(maze, coord, end, path, not_found)
            if not not_found:
                return not_found, path
    # можно идти вниз
    if i < len(maze) - 1 and not maze[i][j].down_wall:
        coord = (i + 1, j)
        if path[-2] != coord and not_found:
            path.append(coord)
            not_found, path = find_path(maze, coord, end, path, not_found)
            if not not_found:
                return not_found, path
    # зачистка ложных тупиковых маршрутов
    if not_found:
        path.pop()
    return not_found, path


def make_solution(maze_file: str, start: tuple, end: tuple, img_read: str, img_out: str):
    """
    Основная функция поиска пути.

    :param maze_file: название файла, содержащего лабиринт
    :param start: координаты точки начала
    :param end: координаты конечной точки
    :param img_read: название картинки для считывания лабиринта
    :param img_out: название картинки для сохранения нарисованного маршрута
    :return:
    """
    h, w, maze = convert_from_file(maze_file)
    if start[0] >= h or start[1] >= w or end[0] >= h or end[1] >= w:
        raise ValueError('Точки вне лабиринта')
    flag, path = find_path(maze, start, end, [start, start])
    path = [[path[i], path[i + 1]] for i in range(1, len(path) - 1)]
    # print(flag)
    add_path_to_image(img_read, h, w, path, img_out)


if __name__ == "__main__":
    visual("./mazes/maze5.txt")
    # image = Image.open("image/maze.png")
    # image.show()
    # add_path_to_image("image/maze.png")
