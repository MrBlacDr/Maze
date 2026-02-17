from maze_genv3 import make_maze, Place
from render_maze import gen_img_maze


def convert_in_file(matrix: list, filename: str) -> None:
    """
    Функция записи лабиринта в файл в соответсвии со стандартами задачи.

    :param matrix: сгенерированный лабиринт
    :param filename: имя файла для сохранения
    """
    with open(filename, "w", encoding='utf-8') as f:
        m, n = len(matrix), len(matrix[0])
        f.write(f"{m} {n}\n")
        for line in matrix:
            for cell in line:
                print(1 if cell.right_wall else 0, file=f, end=" ")
            print(file=f)
        print(file=f)
        for line in matrix:
            for cell in line:
                print(1 if cell.down_wall else 0, file=f, end=" ")
            print(file=f)


def convert_from_file(filename: str) -> tuple:
    """
    Получить матрицу лабиринта из файла

    :param filename: имя загружаемого файла в формате .txt
    :return: кортеж из 3 значений: высота, ширина и сам лабиринт
    """
    matrix = []
    with open(filename, "r", encoding='utf-8') as f:
        lines = f.readlines()
    row, col = map(int, lines[0].strip().split())
    lines.pop(0)
    for i, line in enumerate(lines):
        if i == row:
            break
        line = list(map(int, line.strip().split()))
        new = []
        for j in range(col):
            new.append(Place(0, 0, 0))
            if line[j]:
                new[-1].right_wall = 2
        matrix.append(new)
    for i, line in enumerate(lines[row+1:]):
        line = list(map(int, line.strip().split()))
        for j in range(col):
            if line[j]:
                matrix[i][j].down_wall = 2
    return row, col, matrix


if __name__ == "__main__":
    # convert_in_file(make_maze(10, 10), "mazes/maze10.txt")
    row, col, maze = convert_from_file("ML/origin_3x3.txt")
    gen_img_maze(col, row, maze)
