from tkinter import *
from tkinter import ttk, filedialog, messagebox
from render_maze import gen_img_maze
from maze_genv3 import make_maze
from convertions import convert_from_file, convert_in_file
from render_cave import gen_img_cave
from cave_gen import *
from maze_solution import make_solution
from ML.q_solve import solve
import os


# Для создания исполняемого файла
# pyinstaller --onefile --windowed gui.py


def generate_maze() -> None:
    """
    Генерирует лабиринт с заданной шириной и высотой из спинбоксов.
    """
    w = int(spin_width.get())
    h = int(spin_depth.get())
    my_maze = make_maze(h, w)
    gen_img_maze(w, h, my_maze)  # тут генерируется новый лабиринт
    # print('change image in canvas')
    update_img()
    convert_in_file(my_maze, "mazes/current.txt")


def load_maze() -> None:
    """
    Загрузка лабиринта из файла.
    """
    file_path = filedialog.askopenfilename(initialdir="./mazes/",
                                           title="Выберите файл",
                                           filetypes=[("Текстовые файлы", "*.txt")])
    if file_path:
        rows, cols, matrix = convert_from_file(file_path)
        gen_img_maze(cols, rows, matrix)
        height_var.set(rows)
        weight_var.set(cols)
        update_img()
        convert_in_file(matrix, "mazes/current.txt")
    else:
        print("Какая-то ошибка (скорее всего отменили выбор)")


def load_maze_with_learnt_agent() -> None:
    """
    Загрузка оригинала лабиринта с обученным агентом из файла.
    """
    file_path = filedialog.askopenfilename(initialdir="./ML/",
                                           title="Выберите файл",
                                           filetypes=[("Текстовые файлы", "*.txt")])
    if file_path:
        global _origin_file
        _origin_file = file_path
        rows, cols, matrix = convert_from_file(file_path)
        gen_img_maze(cols, rows, matrix)
        height_var.set(rows)
        weight_var.set(cols)
        update_img()
        update_ml_img('image/maze.png')
        convert_in_file(matrix, "mazes/current.txt")
    else:
        print("Какая-то ошибка (скорее всего отменили выбор)")


def update_ml_img(filename: str) -> None:
    """
    Обновление картинки в GUI на третей вкладке с ML.

    :param filename: откуда брать фото для отображения на экране
    """
    global ml_img
    ml_img = PhotoImage(file=filename)
    canvas3.itemconfig(image_cont3, image=ml_img)


def show_agent_path() -> None:
    """
    Функция, отображающая путь агента к цели и рисующая его поверх нарисованного лабиринта.
    """
    start_x = int(spin_start_ml_x.get()) - 1
    start_y = int(spin_start_ml_y.get()) - 1
    try:
        solve(_origin_file, (start_x, start_y))
        update_ml_img('./image/modified_maze.png')
    except ValueError as e:
        messagebox.showwarning("Предупреждение", e)


def solution() -> None:
    """
    Функция поиска пути в последнем сохраненном лпбиринте.
    """
    start_x = int(spin_start_x.get()) - 1
    start_y = int(spin_start_y.get()) - 1
    end_x = int(spin_end_x.get()) - 1
    end_y = int(spin_end_y.get()) - 1
    if os.path.isfile('mazes/current.txt'):
        try:
            make_solution('mazes/current.txt', (start_x, start_y), (end_x, end_y),
                          './image/maze.png', './image/modified_maze.png')
            show_path()
        except ValueError as e:
            messagebox.showwarning("Предупреждение", e)
    else:
        messagebox.showwarning("Предупреждение", "Создайте новый лабиринт")


def on_close():
    """
    Вызывается при закрытии окна GUI. (нужно для удаления файла current.txt)
    """
    print("Окно было закрыто")
    if os.path.exists('mazes/current.txt'):
        os.remove('mazes/current.txt')
    window.destroy()


def update_img(flag=True) -> None:
    """
    Обновление картинки в GUI.

    :param flag: True - если обновляем лабиринт, False - для пещеры
    """
    if flag:
        global new_maze
        new_maze = PhotoImage(file='image/maze.png')
        canvas.itemconfig(image_cont, image=new_maze)
    else:
        global new_cave
        new_cave = PhotoImage(file='image/cave.png')
        canvas2.itemconfig(image_cont2, image=new_cave)


def show_path() -> None:
    """
    Обновляет экран, загружая картирку с нарисованным путем.
    """
    global new_maze
    new_maze = PhotoImage(file='image/modified_maze.png')
    canvas.itemconfig(image_cont, image=new_maze)


def generate_new_cave() -> None:
    """
    Генерирует новую пещеру с заданной шириной и высотой из спинбоксов.
    """
    global _cave_matrix, _iteration
    w = int(spin_width_cave.get())
    h = int(spin_depth_cave.get())
    _cave_matrix = generate_cave(h, w)
    gen_img_cave(h, w, _cave_matrix)  # тут генерируется новая пещера
    _iteration = 0
    label_iteration.config(text=f"Итерация: {_iteration}")
    # print('change image in canvas')
    update_img(False)


def load_new_cave() -> None:
    """
    Загрузка пещеры из файла.
    """
    global _cave_matrix, _iteration
    file_path = filedialog.askopenfilename(initialdir="./caves/",
                                           title="Выберите файл",
                                           filetypes=[("Текстовые файлы", "*.txt")])
    if file_path:
        rows, cols, _cave_matrix = load_cave(file_path)
        gen_img_cave(rows, cols, _cave_matrix)
        height_var_cave.set(rows)
        width_var_cave.set(cols)
        _iteration = 0
        label_iteration.config(text=f"Итерация: {_iteration}")
        update_img(False)
    else:
        print("Какая-то ошибка (скорее всего отменили выбор)")


def generate_next_step_cave() -> None:
    """
    Обновляет пещеру. В случае смены размерности - предупреждение.
    Создается новая пещера и процесс начинается заново.
    """
    global _cave_matrix, _iteration
    w = int(spin_width_cave.get())
    h = int(spin_depth_cave.get())
    b = int(spin_live.get())
    d = int(spin_death.get())
    if h != len(_cave_matrix) or w != len(_cave_matrix[0]):
        _cave_matrix = generate_cave(h, w)
        _iteration = 0
        messagebox.showwarning("Предупреждение", "\n".join([
            "Размерность предыдущей пещеры не совпадает",
            "с введенными в спинбоксах.",
            "Будет сгенерирована новая пещера",
            "в соответствии с текущими параметрами,",
            "заданными вами."
        ]))
    else:
        _cave_matrix = make_iteration(_cave_matrix, b, d)
        _iteration += 1
    gen_img_cave(h, w, _cave_matrix)
    label_iteration.config(text=f"Итерация: {_iteration}")
    update_img(False)


def auto_generate() -> None:
    """
    Автогенерация пещеры (с шагом в N милисекунд) по созданной на нулевой итерации.
    """
    global _cave_matrix, _iteration
    if not _cave_matrix:
        messagebox.showwarning("Предупреждение", "Сперва создайте новую пещеру!")
        return
    if _iteration >= 15:
        messagebox.showwarning("Предупреждение", "Достигнуто максимальное число итераций!")
        return
    h = len(_cave_matrix)
    w = len(_cave_matrix[0])
    b = int(spin_live.get())
    d = int(spin_death.get())
    dt = int(spin_frequency.get())
    # while _iteration < 15:
    _cave_matrix = make_iteration(_cave_matrix, b, d)
    _iteration += 1
    gen_img_cave(h, w, _cave_matrix)
    label_iteration.config(text=f"Итерация: {_iteration}")
    update_img(False)
    window.after(dt, auto_generate)
    # sleep(dt / 1000)
    # auto_generate()


window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
window.title('Генератор лабиринта v1.0')
window.geometry('512x668')

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Лабиринты')
tab_control.add(tab2, text='Пещеры')
tab_control.add(tab3, text='ML agent')
# tab_control.pack(expand=1, fill=BOTH)
tab_control.grid()

# Создание холста
canvas = Canvas(tab1, width=500, height=500)
canvas.grid(row=0, column=0, sticky=N + S + E + W)

# Загрузка изображения
maze_img = PhotoImage(file='image/start.png')
new_maze = PhotoImage(file='image/maze.png')
image_cont = canvas.create_image(0, 0, anchor=NW, image=maze_img)

# Создание блоков для ввода данных
left_frame = Frame(tab1)
right_frame = Frame(tab1)
left_frame.grid(row=1, column=0, sticky=N + S + W)

# Добавление меток и спин-боксов
weight_var = IntVar(value=10)
Label(left_frame, text='Введите ширину лабиринта').grid(row=0, column=0, padx=5, pady=5, sticky=W + E)
spin_width = Spinbox(left_frame, textvariable=weight_var, from_=2, to=50, width=4)
spin_width.grid(row=0, column=1, padx=5, pady=5, sticky=W + E)

height_var = IntVar(value=10)
Label(left_frame, text='Введите глубину лабиринта').grid(row=1, column=0, padx=5, pady=5, sticky=W + E)
spin_depth = Spinbox(left_frame, textvariable=height_var, from_=2, to=50, width=4)
spin_depth.grid(row=1, column=1, padx=5, pady=5, sticky=W + E)

# Кнопка для генерации нового лабиринта
btn_generate = Button(left_frame, text='Новый лабиринт', command=generate_maze)
btn_generate.grid(row=0, column=2, padx=5, pady=5, sticky=W + E)

# Кнопка для загрузки лабиринта
btn_load = Button(left_frame, text='Загрузить лабиринт', command=load_maze)
btn_load.grid(row=1, column=2, padx=5, pady=5, sticky=W + E)

Label(left_frame, text='Начало').grid(row=0, column=3, padx=5, pady=5, sticky=W + E)
spin_start_x = Spinbox(left_frame, from_=1, to=50, width=4)
spin_start_x.grid(row=0, column=4, padx=5, pady=5, sticky=W + E)
spin_start_y = Spinbox(left_frame, from_=1, to=50, width=4)
spin_start_y.grid(row=0, column=5, padx=5, pady=5, sticky=W + E)
Label(left_frame, text='Конец').grid(row=1, column=3, padx=5, pady=5, sticky=W + E)
spin_end_x = Spinbox(left_frame, from_=1, to=50, width=4)
spin_end_x.grid(row=1, column=4, padx=5, pady=5, sticky=W + E)
spin_end_y = Spinbox(left_frame, from_=1, to=50, width=4)
spin_end_y.grid(row=1, column=5, padx=5, pady=5, sticky=W + E)

btn_solve = Button(left_frame, text='Показать путь', command=solution)
btn_solve.grid(row=2, column=3, columnspan=3, padx=5, pady=5, sticky=W + E)

# Холст на вкладке пещеры
canvas2 = Canvas(tab2, width=500, height=500)
canvas2.grid(row=0, column=0, sticky=N + S + E + W)

# Загрузка стартового изображения пещеры
cave_img = PhotoImage(file='image/start2.png')
new_cave = PhotoImage(file='image/cave.png')
image_cont2 = canvas2.create_image(0, 0, anchor=NW, image=cave_img)

single_frame = Frame(tab2)
single_frame.grid(row=1, column=0, sticky=N + S + W + E)

width_var_cave = IntVar(value=50)
Label(single_frame, text='Введите ширину пещеры').grid(row=0, column=0, padx=5, pady=5, sticky=W + E)
spin_width_cave = Spinbox(single_frame, textvariable=width_var_cave, from_=2, to=50, width=4)
spin_width_cave.grid(row=0, column=1, padx=5, pady=5, sticky=W + E)

height_var_cave = IntVar(value=50)
Label(single_frame, text='Введите глубину пещеры').grid(row=1, column=0, padx=5, pady=5, sticky=W + E)
spin_depth_cave = Spinbox(single_frame, textvariable=height_var_cave, from_=2, to=50, width=4)
spin_depth_cave.grid(row=1, column=1, padx=5, pady=5, sticky=W + E)

live_var = IntVar(value=5)
Label(single_frame, text='Введите предел рождения').grid(row=2, column=0, padx=5, pady=5, sticky=W + E)
spin_live = Spinbox(single_frame, textvariable=live_var, from_=0, to=7, width=4)
spin_live.grid(row=2, column=1, padx=5, pady=5, sticky=W + E)

death_var = IntVar(value=3)
Label(single_frame, text='Введите предел смерти').grid(row=3, column=0, padx=5, pady=5, sticky=W + E)
spin_death = Spinbox(single_frame, textvariable=death_var, from_=0, to=7, width=4)
spin_death.grid(row=3, column=1, padx=5, pady=5, sticky=W + E)

btn_generate_cave = Button(single_frame, text='Новая пещера', command=generate_new_cave)
btn_generate_cave.grid(row=0, column=2, pady=5, sticky=W + E)
btn_load_cave = Button(single_frame, text='Загрузить пещеру', command=load_new_cave)
btn_load_cave.grid(row=1, column=2, pady=5, sticky=W + E)

_iteration = 0
_cave_matrix = []

btn_update_cave = Button(single_frame, text='Следующий шаг', command=generate_next_step_cave)
btn_update_cave.grid(row=2, column=2, pady=5, sticky=W + E)
label_iteration = Label(single_frame, text='Итерация:')
label_iteration.grid(row=3, column=2, padx=5, pady=5, sticky=W + E)

Label(single_frame, text='Ведите N в мс:').grid(row=0, column=3, padx=5, pady=5, sticky=W + E)
spin_frequency = Spinbox(single_frame, from_=100, to=2000, width=4, increment=100)
spin_frequency.grid(row=0, column=4, padx=5, pady=5, sticky=W + E)
Button(single_frame, text='Автогенерация', command=auto_generate).grid(row=1, column=3, columnspan=2, padx=5, pady=5,
                                                                       sticky=W + E)

# ML-часть
canvas3 = Canvas(tab3, width=500, height=500)
canvas3.grid(row=0, column=0, sticky=N + S + E + W)

_origin_file = ''
ml_img = PhotoImage(file='image/start.png')
image_cont3 = canvas3.create_image(0, 0, anchor=NW, image=ml_img)

extra_frame = Frame(tab3)
extra_frame.grid(row=1, column=0, sticky=N + S + W + E)
btn_load_learned_maze = Button(extra_frame, text='Загрузить лабиринт', command=load_maze_with_learnt_agent)
btn_load_learned_maze.grid(row=1, column=0, columnspan=2, pady=5, sticky=W + E)

Label(extra_frame, text='Введите начальную точку x:').grid(row=2, column=0, padx=5, pady=5, sticky=W + E)
spin_start_ml_x = Spinbox(extra_frame, from_=1, to=50, width=4)
spin_start_ml_x.grid(row=2, column=1, padx=5, pady=5, sticky=W + E)
Label(extra_frame, text='Введите начальную точку y:').grid(row=3, column=0, padx=5, pady=5, sticky=W + E)
spin_start_ml_y = Spinbox(extra_frame, from_=1, to=50, width=4)
spin_start_ml_y.grid(row=3, column=1, padx=5, pady=5, sticky=W + E)

btn_show_path = Button(extra_frame, text='Показать путь', command=show_agent_path)
btn_show_path.grid(row=4, column=0, columnspan=2, pady=5, sticky=W + E)

window.mainloop()
