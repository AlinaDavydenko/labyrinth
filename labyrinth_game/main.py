import time
from constants import ROOMS
from utils import describe_current_room
from player_actions import show_inventory, get_input, take_item, move_player, use_item


game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
    }


def process_command(game_state: dict, command: str):
    """ Игровой процесс """
    play_command = command.split()  # Разделяем команду запятой
    main_command = play_command[0].lower()

    match main_command:
        case 'look':
            return describe_current_room(game_state)
        case 'use':  # ?
            if len(play_command) > 1:
                return use_item(game_state, play_command[1])
            else:
                return 'Введите правильную команду: use -- item --'
        case 'go':
            if len(play_command) > 1:
                return move_player(game_state, play_command[1])
            else:
                return 'Введите правильную команду. Пример:\n=== go east ==='
        case 'take':
            if len(play_command) > 1:
                return take_item(game_state, play_command[1])
            else:
                return 'Введите правильную команду из 2 слов: Что надо взять?'
        case 'inventory':
            return show_inventory(game_state)
        case 'quit':
            return get_input()


def main():
    """ Запуск игры """

    print("Добро пожаловать в Лабиринт сокровищ!")
    time.sleep(2)
    print(describe_current_room(game_state))

    while not game_state['game_over']:
        try:
            command = get_input('Введите команду:')  # Запрашиваем данные у пользователей, пока True
            if command.lower() == "quit":
                game_state['game_over'] = True
                print("Спасибо за игру!")
            else:
                print(f"Обрабатываем команду: {command}")  # Отладка
                print(process_command(game_state, command))
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    main()
