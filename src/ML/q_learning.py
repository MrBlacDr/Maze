import os
import sys
from random import choice

sys.path.insert(0, os.path.abspath('../'))
from src.convertions import *
from src.maze_genv3 import Place


def action_moves_agent_to_goal_state(col: int, state: Place, next_state: Place, end: Place) -> bool:
    """
    Если перемещение из текущего состояния в конечное приводит к цели, то возвращает True.

    :param col: ширина лабиринта
    :param state: текущее состояние
    :param next_state: следующее состояние
    :param end: конечная точка
    :return: True или False
    """
    if next_state.set == end.set:
        if abs(state.set - next_state.set) <= 1:
            if state.set > next_state.set:
                if not next_state.right_wall:
                    return True
            elif state.set < next_state.set:
                if not state.right_wall:
                    return True
            else:
                return True
        elif abs(state.set - next_state.set) == col:
            if state.set > next_state.set:
                if not next_state.down_wall:
                    return True
            else:
                if not state.down_wall:
                    return True
    return False


def action_is_valid(col: int, state: Place, next_state: Place) -> bool:
    """
    Если перемещение из текущего состояния в конечное возможно (нет стенок между ними), то возвращает True.

    :param col: ширина лабиринта
    :param state: текущее состояние
    :param next_state: следующее состояние
    :return: True или False
    """
    if abs(state.set - next_state.set) == 1:
        if state.set > next_state.set:
            if not next_state.right_wall:
                return True
        else:
            if not state.right_wall:
                return True
    elif abs(state.set - next_state.set) == col:
        if state.set > next_state.set:
            if not next_state.down_wall:
                return True
        else:
            if not state.down_wall:
                return True
    return False


def reward(r: list, col: int, state: Place, next_state: Place, end: Place) -> None:
    """
    Формирование матрицы R - матрица начальных наград.

    :param r: матрица R
    :param col: ширина лабиринта
    :param state: текущее состояние
    :param next_state: следующее состояние
    :param end: конечная точка
    """
    if action_moves_agent_to_goal_state(col, state, next_state, end):
        _reward = 1
    elif action_is_valid(col, state, next_state):
        _reward = 0
    else:
        _reward = -1
    r[state.set][next_state.set] = _reward


def connector(maze: list) -> dict:
    """
    Хэш-функция, соединябщая уникальные идентификаторы состояний с их координатами в матрице лабиринта.

    :param maze: матрица лабиринта
    :return: словарь-связка
    """
    d = {}
    _count = 0
    row, col = len(maze), len(maze[0])
    for i in range(row):
        for j in range(col):
            d[_count] = (i, j)
            _count += 1
    return d


def get_random_state(line: list) -> int:
    """
    Выбрать рандомное состояние из возможных.

    :param line: список состояний
    :return: выбранное состояние
    """
    return choice(line)


def get_valid_next_states(state: int, r: list) -> list:
    """
    Выбираются состояния в которые можно попопасть. Должны быть соседними и без стенок.

    :param state: состояние
    :param r: матрица R
    :return: список возможных состояний
    """
    list_for_choice = []
    # индекс совпадает с place.set, который определяет любое состояние
    for index, value in enumerate(r[state]):
        if value != -1:
            list_for_choice.append(index)
    return list_for_choice


def normalize(q: list) -> float:
    """
    Нормализация матрицы Q. (Т.е. чтобы значения ее элементов лежали в пределе от -1 до 1).
    Заодно считается сумма всех элементов. (Нужно для выявления сходимости матрицы)

    :param q: матрица Q
    :return: сумма всех элементов нормированной матрицы Q
    """
    max_elem = max([abs(q[i][j]) for j in range(len(q[0])) for i in range(len(q))])
    if max_elem == 0:
        max_elem = 1
    summa = 0.0
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] /= max_elem
            summa += q[i][j]
    return summa


def not_converged(eps: float, sum_prev: float, sum_cur: float) -> bool:
    """
    Проверяется, достигли ли мы сходимиости или нет.

    :param eps: невязка
    :param sum_prev: предыдущая сумма элементов
    :param sum_cur: текущая сумма элементов
    :return: True или False
    """
    if abs(sum_cur - sum_prev) <= eps:
        return False
    return True


def train(q: list, r: list, end: Place, eps=0.001, gamma=0.9) -> None:
    """
    Основной модуль, в котором происходит обучение, согласно алгоритму Q-обучения.

    :param q: матрица Q
    :param r: матрица R
    :param end: конечная точка (задается нами и не меняется в процессе обучения)
    :param eps: невязка
    :param gamma: параметр, отвечающий за учет будущих наград
    """
    goal_state = end.set
    sum_prev = 2 * eps
    sum_cur = 0
    considered_first_steps = [i for i in range(len(r))]
    points_picked = 0
    goal_reached = 0
    while not_converged(eps, sum_prev, sum_cur) or points_picked < len(r) - 1:
        sum_prev = sum_cur

        # Start in random state
        state = get_random_state(considered_first_steps)
        considered_first_steps.remove(state)
        start_state = state

        # Keep going until the goal state is reached
        while state != goal_state or goal_reached < 10:
            if state == goal_state:
                goal_reached += 1
                state = start_state
            # Pick a random next state
            possible_next_states = get_valid_next_states(state, r)
            next_state = choice(possible_next_states)

            # Get the best Q Value over all valid actions from the next state
            next_next_states = get_valid_next_states(next_state, r)
            max_q_next_states = max([q[next_state][s] for s in next_next_states])

            # Update the Q matrix
            q[state][next_state] = r[state][next_state] + (gamma * max_q_next_states)

            # Move to the new state
            state = next_state
        points_picked += 1

        sum_cur = normalize(q)


def prepare_result(q: list, r: list) -> None:
    """
    Подготовка результата к сохранению.

    :param q: матрица Q
    :param r: матрица R
    """
    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i][j] += r[i][j]


def save_result(filename, q: list, end_point: int) -> None:
    """
    Сохранение обученного агента в файл.

    :param filename: имя файла
    :param q: матрица Q
    :param end_point: конечная точка
    """
    with open(filename, "w", encoding='utf-8') as f:
        print(end_point, file=f)
        for i in range(len(q)):
            for j in range(len(q[0])):
                print("{:.2f}".format(q[i][j]), file=f, end=' ')
            print(file=f)


def load_result(filename: str) -> tuple:
    """
    Загрузка обученного агента.

    :param filename: имя файла
    :return: 2 значения. Первое - конечная точка, Второе - матрица Q
    """
    with open(filename, "r", encoding='utf-8') as f:
        s = f.readlines()
        q = []
        point = int(s.pop(0).strip())
        for line in s:
            line = list(map(float, line.strip().split()))
            q.append(line)
        return point, q


def learn(origin_file: str, end_state: int) -> None:
    """
    Главная функция. Выполняет сбор, обработку данных лабиринта, обучает агента и сохраняет результат.
    :param origin_file: имя файла
    :param end_state: конечная точка
    """
    # row, col, maze = convert_from_file("../mazes/3x3.txt")
    row, col, maze = convert_from_file(origin_file)
    name_to_save = origin_file.split('/').pop()
    convert_in_file(maze, "origin_" + name_to_save)
    d = connector(maze)
    end_ij = d[end_state]
    _count = 0
    for line in maze:
        for elem in line:
            elem.set = _count
            _count += 1
    end = maze[end_ij[0]][end_ij[1]]
    maze_v = [elem for line in maze for elem in line]
    # print(maze_v)
    r = [[0 for _ in range(len(maze_v))] for _ in range(len(maze_v))]
    for s in range(len(maze_v)):
        for s_prime in range(len(maze_v)):
            reward(r, col, maze_v[s], maze_v[s_prime], end)
    #         print("{:.2f}".format(r[s][s_prime]), end=' ')
    #     print()
    # print('\n\n')

    q = [[0 for _ in range(len(maze_v))] for _ in range(len(maze_v))]
    train(q, r, end)

    prepare_result(q, r)
    normalize(q)
    # for s in range(len(maze_v)):
    #     for s_prime in range(len(maze_v)):
    #         print("{:.2f}".format(q[s][s_prime]), end=' ')
    #     print()

    # save_result("4x4.txt", q, end.set)
    save_result("./Learned_agent/learned_" + name_to_save, q, end.set)


if __name__ == "__main__":
    learn("../mazes/maze10.txt", 63)
    # p, q = load_result("./Learned_agent/learned_3x3.txt")
    # print(p)
    # for line in q:
    #     print(line)
