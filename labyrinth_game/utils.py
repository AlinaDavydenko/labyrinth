from constants import ROOMS


def describe_current_room(game_state: dict) -> str:
    """ Описание комнаты """
    current_room = game_state['current_room']  # Получение стартовой комнаты
    about_room = ROOMS[current_room]  # Поиск комнаты в словаре ROOMS
    items = ', '.join(about_room['items'])
    exits = ', '.join(about_room['exits'])
    room = current_room.upper()

    puzzle = about_room.get('puzzle')  # Вытаскиваем характеристики puzzle и проверяем на None
    puzzle_text = ''
    if puzzle:
        question, answer = puzzle
        puzzle_text = f'\nКажется, здесь есть загадка (используйте команду solve): \n{question}'

    return f'''== {room} ==\n{about_room['description']}\nЗаметные предметы: {items}\nВыходы: {exits}\n{puzzle_text}'''


def solve_puzzle(game_state):
    """ Функция решения загадок """
