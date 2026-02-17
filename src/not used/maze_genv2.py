from random import choice


class Place:
    def __init__(self, set, r, d) -> None:
        self.set = set
        self.right_wall = r
        self.down_wall = d

    # def __repr__(self) -> str:
    #     return f"[{self.set}, {self.right_wall}, {self.down_wall}]"

    def __repr__(self):
        return "{}{}".format(self.set, "|" if self.right_wall else "")


"""
По алгоритму описанному в статье:
https://habr.com/ru/articles/667576/
делаем по шагам:
"""

yes_no = [0, 1]
_count = 1


def maze_fill_empty_value(columns: int) -> list:
    """
    Заполнение строчки лабиринта пустыми занчениями
    :param columns: ширина лабиринта
    :return: список объектов Place
    """
    line = [Place(0, 0, 0) for x in range(columns)]  # создаем пустые места
    return line


def maze_assign_unique_set(line: list) -> None:
    """
    Присваиваем каждой ячейке свое уникальное множество (по факту просто уникальное число)
    :param line: список объектов Place
    :param _counter: глобальная переменная, счетчик уникальных множеств
    """
    global _count
    for elem in line:  # заполняем пустые места уникальными множествами
        if elem.set == 0:
            elem.set = _count
            _count += 1


def maze_adding_vertical_walls(line: list) -> None:
    """
    Добавление вертикальных границ.
    :param line: список объектов Place
    """
    for i in range(len(line) - 1):
        # Решаем, ставим стенку или нет.
        # Вторым условием предотвращаем зацикливание.
        if choice(yes_no) or line[i + 1].set == line[i].set:
            line[i].right_wall = 2
    line[-1].right_wall = 2  # добавление правой стенки последней ячейки.


def maze_merge_set(line: list) -> None:
    """
    Объединение соседних ячеек в одно множество. Разделитель между множествами - правая стенка.
    :param line: список объектов Place
    """
    start = 0
    end = 0
    for i in range(len(line) - 1):
        if line[i].right_wall == 0:
            merged_val = line[i].set
            line[i + 1].set = merged_val


def maze_adding_horizontal_walls(line: list) -> None:
    """
    Добавление горизонтальной стенки.
    :param line: список объектов Place
    """
    start = 0
    end = 0
    for i in range(len(line) - 1):
        if choice(yes_no):
            line[i].down_wall = 2
        if line[i + 1].set != line[i].set:
            maze_make_gape_and_wall_in_subline(line, start, end)
            start = i + 1
            end = start
        else:
            end += 1
    maze_make_gape_and_wall_in_subline(line, start, end)


# def maze_is_not_unique_sell(line: list, index: int) -> bool:
#     if index - 1 >= 0 and line[index - 1].set == line[index].set:
#         return True
#     if index + 1 < len(line) and line[index + 1].set == line[index].set:
#         return True
#     return False


# def maze_check_for_necessary_wall(line: list, index: int):
#     set_of_same_sets = []
#     for i in range(index - 1, 0, -1):
#         if line[i - 1].set == line[i].set:
#             set_of_same_sets.append(i)
#             if line[i].down_wall:
#                 return
#         else:
#             break

def maze_make_gape_and_wall_in_subline(line: list, start, end) -> None:
    list_for_choice = [x for x in range(start, end + 1)]
    if not any(line[i].down_wall == 0 for i in range(start, end + 1)):
        line[choice(list_for_choice)].down_wall = 0
    if end - start > 0 and not any(line[i].down_wall == 2 for i in range(start, end + 1)):
        line[choice(list_for_choice)].down_wall = 2


def maze_adding_horizontal_walls_for_other(line: list, prev: list) -> None:
    for i in range(len(line) - 1):
        if choice(yes_no):
            if line[i + 1].set == line[i].set:
                line[i].down_wall = 2


def maze_make_first_line(col):
    new_line = maze_fill_empty_value(col)
    maze_assign_unique_set(new_line)
    maze_adding_vertical_walls(new_line)
    maze_merge_set(new_line)
    maze_adding_horizontal_walls(new_line)
    # print(*new_line)
    return new_line


def maze_make_other_line(prev: list):
    global _count
    new_line = [
        Place(prev[i].set, prev[i].right_wall, prev[i].down_wall)
        for i in range(len(prev))
    ]  # делаю копию предыдущей строки
    for elem in new_line:  # затираем правые границы, если была нижняя стена стираем ее и убираем элемент из множества
        elem.right_wall = 0
        if elem.down_wall:
            elem.set = _count
            _count += 1
        elem.down_wall = 0
    # maze_assign_unique_set(new_line)
    maze_adding_vertical_walls(new_line)
    maze_merge_set(new_line)
    # maze_adding_horizontal_walls_for_other(new_line, prev)
    maze_adding_horizontal_walls(new_line)
    # print(*new_line)
    return new_line


def maze_make_last_line(prev: list):
    global _count
    new_line = [
        Place(prev[i].set, prev[i].right_wall, prev[i].down_wall)
        for i in range(len(prev))
    ]  # делаю копию предыдущей строки
    for i in range(len(prev) - 1):
        if new_line[i].down_wall:
            new_line[i].set = _count
            _count += 1
        if new_line[i].set != new_line[i + 1].set:
            new_line[i].right_wall = 0
            new_line[i].set = new_line[i + 1].set
        new_line[i].down_wall = 2
    new_line[-1].down_wall = 2
    #     if elem.down_wall:
    #         elem.set = _count
    #         _count += 1
    #     elem.down_wall = 0
    # maze_assign_unique_set(new_line)
    # maze_adding_vertical_walls(new_line)
    # maze_merge_set(new_line)

    return new_line


def make_maze(row, col):
    matrix = []
    for i in range(row):
        if i == 0:
            matrix.append(maze_make_first_line(col))
        elif i == row - 1:
            matrix.append(maze_make_last_line(matrix[-1]))
        else:
            matrix.append(maze_make_other_line(matrix[-1]))
    return matrix
    # for elem in matrix:
    #     print(elem)
