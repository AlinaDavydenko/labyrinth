from constants import ROOMS


def show_inventory(game_state):
    """ Вывод содержимого инвентаря """
    message = 'Ваш инвентарь пуст'
    inventory = game_state['player_inventory']

    # Преобразование объектов листа инвентаря
    if len(inventory) > 0:
        message = ', '.join(str(item) for item in inventory)

    return message


def get_input(prompt="> "):
    """ Запрос данных у пользователя """
    try:
        command = input(f"{prompt} ").strip()
        return command
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: dict, direction: str):
    """ Функция перемещения """
    current_room = game_state['current_room']  # Получаем текущую комнату
    exits = ROOMS[current_room]['exits']  # Получаем список выходов

    # Проверяем существование выхода в направлении direction
    if direction in exits:
        game_state['steps_taken'] += 1
        game_state['current_room'] = exits[direction]
        return ROOMS[current_room]['description']
    else:
        return "Нельзя пойти в этом направлении."


def take_item(game_state: dict, item_name: str):
    """ Функция взятия предмета """
    current_room = game_state['current_room']  # Получаем текущую комнату
    items_list = ROOMS[current_room]['items']  # Получаем список предметов в текущей комнате
    if item_name in items_list:
        game_state['player_inventory'].append(item_name)  # Добавляем предмет в инвентарь игрока
        items_list.remove(item_name)  # Удаляем предмет из списка предметов в комнате
        return f'Вы подняли: {item_name}'
    else:
        return "Такого предмета здесь нет."


def use_item(game_state: dict, item_name: str) -> str:
    """ Используем предметы """

    # Проверяем, есть ли предмет у игрока
    if item_name in game_state['player_inventory']:
        match item_name:
            case 'torch':
                return 'Вокруг вас стало светлее!'
            case 'sword':
                return 'Вам добавились очки уверенности'

    elif item_name == 'bronze box':
        game_state['player_inventory'].append('rusty_key')
        return 'О чудо! Шкатулка открыта!'

    if item_name != ['torch', 'sword']:
        return 'Игрок не знает, как использовать эти предметы'

    else:
        return 'У вас нет такого предмета.'

