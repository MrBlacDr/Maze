from random import randint


def generate_cave(x: int, y: int) -> list:
    """
    Генерация стартовой пещеры. Рандомное заполенение 0 - живая клетка (белая), 1 - мертвая (черная).

    :param x: глубина
    :param y: ширина
    :return: поле пещеры
    """
    matrix = [[0 for _ in range(y)] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            matrix[i][j] = randint(0, 1)
    return matrix


def load_cave(file: str) -> tuple:
    """
    Загрузка пещеры из файла

    :param file: имя файла или полный путь до него
    :return: размеры и поле пещеры
    """
    matrix = []
    with open(file, "r") as f:
        for elem in f:
            matrix.append(list(map(int, elem.split())))
    rows, cols = matrix.pop(0)
    return rows, cols, matrix


def save_cave(filename: str, cave_matrix) -> None:
    """
    Сохранение пещеры в файл

    :param filename: имя файла или полный путь до него
    :param cave_matrix: поле пещеры
    """
    with open(filename, "w") as file:
        print(f"{len(cave_matrix)} {len(cave_matrix[0])}\n", file=file, end='')
        for line in cave_matrix:
            print(*line, file=file)


def check_boards(i: int, j: int, matrix: list) -> int:
    """
    Проверка клеток, которые на границы области, подсчет мертвых клеток вокруг них.

    :param i: индекс ячейки по глубине
    :param j: индекс ячецки по ширине
    :param matrix: поле пещеры
    :return: количество мертвых клеток вокруг
    """
    col = len(matrix[0])
    row = len(matrix)
    count_dead_cells = 0
    if i == 0 and j == 0:
        count_dead_cells += matrix[0][1] + matrix[1][0] + matrix[1][1]
    elif i == 0 and j == col - 1:
        count_dead_cells += matrix[0][col - 2] + matrix[1][col - 2] + matrix[1][col - 1]
    elif i == row - 1 and j == 0:
        count_dead_cells += matrix[row - 1][1] + matrix[row - 2][0] + matrix[row - 2][1]
    elif i == row - 1 and j == col - 1:
        count_dead_cells += matrix[row - 1][col - 2] + matrix[row - 2][col - 2] + matrix[row - 2][col - 1]
    else:
        if i == 0:
            count_dead_cells += matrix[0][j - 1] + matrix[0][j + 1]
            for k in range(j - 1, j + 2):
                count_dead_cells += matrix[0][k]
        elif j == 0:
            count_dead_cells += matrix[i - 1][0] + matrix[i + 1][0]
            for k in range(i - 1, i + 2):
                count_dead_cells += matrix[k][0]
        elif j == col - 1:
            count_dead_cells += matrix[i - 1][col - 1] + matrix[i + 1][col - 1]
            for k in range(i - 1, i + 2):
                count_dead_cells += matrix[k][col - 1]
        elif i == row - 1:
            count_dead_cells += matrix[row - 1][j - 1] + matrix[row - 1][j + 1]
            for k in range(j - 1, j + 2):
                count_dead_cells += matrix[row - 1][k]
    return count_dead_cells


def make_iteration(matrix: list, lim_b: int, lim_d: int) -> list:
    """
    Итерация клеточного автомата.
    Функция переписывает пещеру в соответсвии с заданными правилами и пределами жизни и смерти.

    :param matrix: входное поле пещеры
    :param lim_b: предел рождения
    :param lim_d: предел смерти
    :return: обновленное поле пещеры
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            around_d = 0
            if i == 0 or j == 0 or i == len(matrix) - 1 or j == len(matrix[0]) - 1:
                around_d += check_boards(i, j, matrix)
            else:
                if i > 0:
                    around_d += matrix[i - 1][j]
                if j > 0:
                    around_d += matrix[i][j - 1]
                if i < len(matrix) - 1:
                    around_d += matrix[i + 1][j]
                if j < len(matrix[0]) - 1:
                    around_d += matrix[i][j + 1]
                if i > 0 and j > 0:
                    around_d += matrix[i - 1][j - 1]
                if i > 0 and j < len(matrix[0]) - 1:
                    around_d += matrix[i - 1][j + 1]
                if i < len(matrix) - 1 and j > 0:
                    around_d += matrix[i + 1][j - 1]
                if i < len(matrix) - 1 and j < len(matrix[0]) - 1:
                    around_d += matrix[i + 1][j + 1]
            # around_d += check_boards(i, j, matrix)
            around_l = 8 - around_d
            if matrix[i][j] and around_l > lim_b:  # проверка для мертвой клетки
                matrix[i][j] = 0
            elif matrix[i][j] == 0 and around_l < lim_d:  # проверка для живой клетки
                matrix[i][j] = 1
    return matrix


def create_cave(matrix: list, lim_b: int, lim_d: int, iterations=20) -> list:
    """
    Создание пещеры, прошедшей заданное число итераций (обновлений).

    :param matrix: входное поле пещеры
    :param lim_b: предел рождения
    :param lim_d: предел смерти
    :param iterations: заданное количество итераций
    :return: обновленное поле пещеры
    """
    for i in range(iterations):
        matrix = make_iteration(matrix, lim_b, lim_d)
    return matrix


def make_cave(lim_b, lim_d, rows, cols) -> list:
    """
    Тестовая функция, создает пещеру сразу после 20 итераций.

    :param lim_b: предел рождения
    :param lim_d: предел смерти
    :param rows: глубина
    :param cols: ширина
    :return: поле пещеры
    """
    raw = generate_cave(rows, cols)
    cave = create_cave(raw, lim_b, lim_d)
    return cave


if __name__ == "__main__":
    cave = generate_cave(30, 30)
    # col, row, cave = load_cave("./caves/from_readme.txt")
    # print(col, row, cave)
    save_cave("./caves/cave3.txt", cave)
