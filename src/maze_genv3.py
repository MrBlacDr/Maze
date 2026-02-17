from random import choice


class Place:
    """
    Представляет ячейку лабиринта с возможностью установки правой и нижней стены.

    Атрибуты:
        set (int): Уникальный индентификатор принадлежности к множеству.

        right_wall (int): Толщина правой стены.

        down_wall (int): Толщина нижней стены.

    Методы:
        __str__: Возвращает строковое представление объекта Place.

        __repr__: Возвращает строковое представление объекта Place для отладки.
    """

    def __init__(self, set, r=2, d=2) -> None:
        """
        Инициализирует экземпляр класса Place.

        Параметры:
            set (int): Набор, идентифицирующий место.

            r (int, optional): Толщина правой стены. По умолчанию равно 2.

            d (int, optional): Толщина нижней стены. По умолчанию равно 2.
        """
        self.set = set
        self.right_wall = r
        self.down_wall = d

    def __eq__(self, other):
        """
        Функция сравнения 2 объектов Place
        :param other: другой объект Place
        :return: True или False
        """
        if isinstance(other, Place):
            return self.set == other.set and self.right_wall == other.right_wall and self.down_wall == other.down_wall
        return NotImplemented

    def __ne__(self, other):
        """
        Функция сравнения 2 объектов Place (not equal)
        :param other: другой объект Place
        :return: True или False
        """
        if isinstance(other, Place):
            return self.set != other.set or self.right_wall != other.right_wall or self.down_wall != other.down_wall
        return NotImplemented

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Place.
        """
        return f"[{self.set}, {self.right_wall}, {self.down_wall}]"

    def __repr__(self):
        """
        Возвращает строковое представление объекта Place для отладки.
        """
        return "{}{}".format(self.set, "|" if self.right_wall else "")


"""
По алгоритму описанному в статье:
https://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm
делаем по шагам:
"""

yes_no = [0, 1]
_count = 1  # глобальная переменная, счетчик уникальных множеств


def maze_fill_empty_value(columns: int) -> list:
    """
    Заполнение строчки лабиринта пустыми занчениями

    :param columns: ширина лабиринта
    :return: список объектов Place
    """
    line = [Place(0) for _ in range(columns)]  # создаем пустые места
    return line


def maze_assign_unique_set(line: list) -> None:
    """
    Присваиваем каждой ячейке свое уникальное множество (по факту просто уникальное число)

    :param line: список объектов Place
    """
    global _count
    for elem in line:  # заполняем пустые места уникальными множествами
        if elem.set == 0:
            elem.set = _count
            _count += 1


def maze_dropping_vertical_walls(line: list, hash: dict) -> None:
    """
    Удаление вертикальных границ.

    :param line: список объектов Place
    :param hash: словарь: ключ - цифра множества, значение - список индексов ячеек, принадлежащих этому множеству
    """
    for i in range(len(line) - 1):
        # Решаем, убирать стенку или нет.
        # Убираем стенку только между разными множествами и сливаем их.
        if choice(yes_no) and line[i + 1].set != line[i].set:
            line[i].right_wall = 0
            maze_merge_set(line, hash, i)


def maze_hash_for_mutable_sets(line: list) -> dict:
    """
    Ячейки, принадлежащие одному множеству могут быть разбросаны по всей строке.
    Данная функция помогает собрать индексы ячеек в список и хранить эти списки в ключах словаря
    (ключ - уникальное число, принадлежащее кокнретному множеству).

    :param line: список объектов Place
    :return: словарь: ключ - цифра множества, значение - список индексов ячеек, принадлежащих этому множеству
    """
    d = {}
    for i in range(len(line)):
        if line[i].set in d.keys():
            d[line[i].set].append(i)
        else:
            d[line[i].set] = [i]
    return d


def maze_merge_set(line: list, hash: dict, index: int) -> None:
    """
    Объединение соседних ячеек в одно множество. Если с сливаемой ячейкой связаны другие, то и их значение меняем.

    :param line: список объектов Place
    :param hash: словарь: ключ - цифра множества, значение - список индексов ячеек, принадлежащих этому множеству
    :param index: индекс ячейки, с которой сливаются все остальные
    """
    old_key = line[index + 1].set
    mutable_key = line[index].set
    for i in hash[old_key]:
        line[i].set = mutable_key
        hash[mutable_key].append(i)
    del hash[old_key]


def maze_get_list_of_unique(line: list) -> list:
    """
    Получить список уникальных значений (по факту - список всех множеств)

    :param line: список объектов Place
    :return: список
    """
    return list(set([elem.set for elem in line]))


def maze_list_indices_for_choice(line: list, elem) -> list:
    """
    Выбирает индексы ячеек, принадлежащих одному множеству.

    :param line: список объектов Place
    :param elem: опорный элемент, содержащий информацию о множестве
    :return: список
    """
    result = []
    for i in range(len(line)):
        if line[i].set == elem.set:
            result.append(i)
    return result


def maze_dropping_horizontal_walls(line: list) -> None:
    """
    Удаление хотя бы горизонтальной стенки в каждом множестве.
    После этого происходит рандомное удаление горизонтальное стенки.

    :param line: список объектов Place
    """
    # создаем список уникальных множеств
    unique = maze_get_list_of_unique(line)
    for i in range(len(line)):
        # обязательное удаление стенки для каждого из наборов множеств
        if line[i].set in unique:
            list_indices_for_choice = maze_list_indices_for_choice(line, line[i])
            unique.remove(line[i].set)
            line[choice(list_indices_for_choice)].down_wall = 0
        # случайное удаление
        if choice(yes_no):
            line[i].down_wall = 0


def maze_make_first_line(col) -> list:
    """
    Генерируем первую строчку лабиринта.

    :param col: ширина лабиринта
    :return: список ячеек
    """
    new_line = maze_fill_empty_value(col)
    maze_assign_unique_set(new_line)
    d = maze_hash_for_mutable_sets(new_line)
    maze_dropping_vertical_walls(new_line, d)
    maze_dropping_horizontal_walls(new_line)
    return new_line


def maze_make_other_line(col: int, prev: list) -> list:
    """
    Функция для генерации строк лабиринта, начиная со второй, заканчивая предпоследней.

    :param col: ширина лабиринта
    :param prev: предыдущая строка лабиринта
    :return: список ячеек
    """
    new_line = maze_fill_empty_value(col)
    for i in range(len(prev)):
        if prev[i].down_wall == 0:
            new_line[i].set = prev[i].set
    maze_assign_unique_set(new_line)
    d = maze_hash_for_mutable_sets(new_line)
    maze_dropping_vertical_walls(new_line, d)
    maze_dropping_horizontal_walls(new_line)
    return new_line


def maze_make_last_line(col: int, prev: list) -> list:
    """
    Функция для генерации последней строки лабиринта.

    :param col: ширина лабиринта
    :param prev: предыдущая строка лабиринта
    :return: список ячеек
    """
    new_line = maze_fill_empty_value(col)
    for i in range(len(prev)):
        if prev[i].down_wall == 0:
            new_line[i].set = prev[i].set
    maze_assign_unique_set(new_line)
    d = maze_hash_for_mutable_sets(new_line)
    # убрать стенки между разными множествами и объединить множества
    for i in range(len(prev) - 1):
        if new_line[i].set != new_line[i + 1].set:
            new_line[i].right_wall = 0
            maze_merge_set(new_line, d, i)
    return new_line


def make_maze(row, col) -> list:
    """
    Главная функция, генерируюшая весь лабиринт с заданными параметрами.

    :param row: высота лабиринта.
    :param col: ширина лабиринта.
    :return: матрица с записанным лабиринтом
    """
    matrix = []
    for i in range(row):
        if i == 0:
            matrix.append(maze_make_first_line(col))
        elif i == row - 1:
            matrix.append(maze_make_last_line(col, matrix[-1]))
        else:
            matrix.append(maze_make_other_line(col, matrix[-1]))
    return matrix
