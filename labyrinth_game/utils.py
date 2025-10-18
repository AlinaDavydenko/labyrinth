from constants import ROOMS


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


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
    current_room = game_state['current_room']
    puzzle = ROOMS[current_room]['puzzle']

    if puzzle is not None:
        answer = puzzle[1]  # Получаем ответ
        player_answer = input(f'{puzzle[0]}\n"Ваш ответ:')

        match answer:

            # Если попадается 10, то мы можем ввести её числом или текстом
            case '10':
                if player_answer.lower() in ['10', 'десять']:
                    ROOMS['current_room']['puzzle'] = None
                    game_state['prize'] += 1
                    return '^*^ Ваш ответ правильный! Так держать! ^*^\n*** Продолжайте исследовать пространство ***'
                else:
                    return 'Ваш ответ неправильный *_*'

            # Если другой ответ, то просто сравниваем в нижнем регистре
            case answer:
                if player_answer.lower() == answer:
                    ROOMS['current_room']['puzzle'] = None
                    game_state['prize'] += 1
                    return '=== Ваш ответ правильный! Так держать! ===\n*** Продолжайте исследовать пространство ***'
                else:
                    return 'Неверно. Попробуйте снова *_*'
    else:
        return 'Загадок здесь нет ^*^'


def attempt_open_treasure(game_state):
    """ Реализация логики победы """
    current_room = game_state['current_room']
    if current_room == 'treasure_room':
        if 'treasure_key' in game_state['player_inventory']:
            ROOMS['treasure_room']['items'].pop('treasure_key', 'Сокровище не найдено')
            game_state['game_over'] = True
            return 'Вы применяете ключ, и замок щёлкает. Сундук открыт!\nВ сундуке сокровище! Вы победили!'
        else:
            answer = input("Сундук заперт. ... Ввести код? (да/нет)")

            # Если ответ ДА
            if answer == 'да'.lower():
                puzzle = ROOMS['treasure_room']['puzzle']
                answer_puzzle = input(f'{puzzle[0]}\nВвод кода:')
                if answer_puzzle == puzzle[1]:
                    ROOMS['treasure_room']['items'].pop('treasure_key', 'Сокровище не найдено')
                    game_state['game_over'] = True
                    return 'Ура! Ответ верный :з'
                else:
                    return 'Код неверный!'

            # Если ответ TAKE
            elif answer == 'take':
                return 'Вы не можете поднять сундук, он слишком тяжелый'

            # Остальные варианты
            else:
                return "Вы отступаете от сундука."

    else:
        return 'Вы не в той комнате, чтобы использовать *** treasure_key ***'

