import random
import subprocess

# Размеры игрового поля
COLUMNS = 4
ROWS = 4

# Создание матриы
matrix = [[0 for _ in range(ROWS)] for _ in range(COLUMNS)]

# Генерация стратовых значений 
matrix[random.randint(0,3)][random.randint(0,3)] = 2
matrix[random.randint(0,3)][random.randint(0,3)] = 2

# Алгоритм суммирования массива, по правилам игры 2048
def sum_algorithm(array):
    i = 0
    while i<len(array)-1:
        if (array[i] == array[i+1]) and not (array[i] == 0):
            array[i], array[i+1] = array[i] + array[i+1], 0
        i +=1
        array = [x for x in array if x != 0]
    return array

# Суммирования массива, в зависимости от напрвления 
def sum_array(array, f):
    if f == '-d' or f == '-r':

        array = array[::-1]
        array = sum_algorithm(array)
        array = array[::-1]

        return array
    if f == '-u' or f == '-l':
        return sum_algorithm(array)

# Удаление 0 из массива 
def zeroes_cleaner(array):
    return [x for x in array if x != 0]

# Не помню зачем эта фунция
def array_recounter(column, f):
    ch = False
    while not ch:
        if column == sum_array(column, f):
            ch = True
        else:
            column = sum_array(column, f)
    return column, f

# Добавление 0, в зависимости от напрвления
def append_empty_space(array, f):
    if f == '-d' or f == '-r':
        while len(array) < COLUMNS:
            array = [0] + array
        return array
    if f == '-u' or f == '-l':
        while len(array) < COLUMNS:
            array.append(0)
        return array

# Функция перезаписи колонки в матрице
def rewrate_column(colmn, array, matrix):
    for i in range(COLUMNS):
        matrix[i][colmn] = array[i]
    return matrix

# Функция ряда колонки в матрице
def rewrate_row(row, array, matrix):
    matrix[row] = array
    return matrix

# Сложение матрице вверх или вниз
def move_matrix_y(matrix, f):
    for column in range(COLUMNS):
        arr = [matrix[i][column] for i in range(len(matrix))]
        if not zeroes_cleaner(arr) == []:
            arr = append_empty_space(
                        *array_recounter(
                            zeroes_cleaner(arr),
                            f
                        ),
                    )
            matrix = rewrate_column(column, arr, matrix)
    return matrix

# Сложение матрице вправо или влево
def move_matrix_x(matrix, f):
    for row in range(ROWS):
        arr = matrix[row] 
        if not zeroes_cleaner(arr) == []:
            arr = append_empty_space(
                        *array_recounter(
                            zeroes_cleaner(arr),
                            f
                        ),
                    )   
            matrix = rewrate_row(row, arr, matrix)
    return matrix

# Вывод матрици в консоль 
def print_matrix(matrix):
    game_zone = ''
    for i in range(len(matrix)):
        game_zone += '\n\n'
        for j in range(len(matrix[i])):
            # Это строчка нормализует расстояние между колонками  
            game_zone += f' {matrix[i][j]}' + f'{"".join([" " for _ in range(5 - len(str(matrix[i][j]) ))])}'
    print(game_zone)

# Нахождение пустых ячеек
def empty_cell(matrix):
    rand = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                rand.append([i,j])
    return rand

# Заполнение матрицы новыми элементами
def game_cycle(matrix):
    rand = empty_cell(matrix)
    random_cell = random.randint(0, len(rand)-1)
    cell = rand[random_cell]
    matrix[cell[0]][cell[1]] = 2
    return matrix

rand = empty_cell(matrix)

# Основной цикл игры
while not rand == []:
    subprocess.call("cls", shell=True)
    print("\n Type:  -l for left, -r for right, -u for up, -d for down \n")
    print_matrix(matrix)
    f = input()
    if f == '-r' or f == '-l':
        matrix = move_matrix_x(matrix, f)
        matrix = game_cycle(matrix)
        subprocess.call("cls", shell=True)
    elif f == '-u' or f == '-d':
        matrix = move_matrix_y(matrix, f)
        matrix = game_cycle(matrix)
        subprocess.call("cls", shell=True)