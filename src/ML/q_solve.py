import os
import sys

sys.path.insert(0, os.path.abspath('../'))

from src.ML.q_learning import load_result, convert_from_file, connector
from src.maze_solution import add_path_to_image

def get_best_next_state(line: list) -> int:
    """
    Получить следующее состояние с наибольшей наградой.

    :param line: строка возможных переходов
    :return индекс лучшего состояния
    """
    max_val = -1
    max_ind = -1
    for i, val in enumerate(line):
        if val > max_val and val >= 0:
            max_val = val
            max_ind = i
    return max_ind


def solve(filename: str, start: tuple) -> list:
    """
    Функция, которая находит путь, используя обученного агента.

    :param filename: имя файла, в котором содержится исходный лабиринт, по которому происходило обучение
    :param start: начальная точка
    :return: список координат для достижения конечной точки
    """
    row, col, maze = convert_from_file(filename)
    if start[0] >= row or start[1] >= col:
        raise ValueError('Точки вне лабиринта')
    name_to_load_learnt_model = filename.split('_').pop()
    current_dir = os.getcwd()
    dir_to_learnt_maze = current_dir
    dir_to_analyse = current_dir.split('\\')
    if dir_to_analyse[-1] == 'src':
        dir_to_learnt_maze += '/ML'
    elif dir_to_analyse[-1] == 'test':
        dir_to_learnt_maze = '/'.join(dir_to_analyse[:-1]) + '/ML/'
    # print(current_dir)
    goal_state, q = load_result(dir_to_learnt_maze + "/Learned_agent/learned_" + name_to_load_learnt_model)
    d = connector(maze)
    state = 0
    for k, v in d.items():
        if v == start:
            state = k

    # Initialize path
    path = [d[state]]

    # add_state_to_path(state)

    # Keep going until goal state is reached
    while state != goal_state:
        # Get all possible next states
        # possible_next_states = get_valid_next_states(state)

        # Pick the state that maximizes Q[state][next_state]
        best_next_state = get_best_next_state(q[state])

        # Move to that state and add it to the path
        state = best_next_state
        path.append(d[state])
    reshaped_path = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
    if dir_to_analyse[-1] == 'src':
        add_path_to_image("image/maze.png", row, col, reshaped_path, "image/modified_maze.png")
    elif dir_to_analyse[-1] == 'ML':
        add_path_to_image("../image/maze.png", row, col, reshaped_path, "../image/modified_maze.png")
    return path


if __name__ == "__main__":
    _path = solve("origin_maze10.txt", (9, 0))
    print(_path)
