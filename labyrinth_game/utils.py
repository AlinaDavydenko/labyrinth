import math
from constants import ROOMS


def show_help(commands):
    print("\nДоступные команды:")
    for command, description in commands.items():
        # Форматируем команду с отступом в 16 символов
        print(f"  {command:<16} - {description}")


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


def trigger_trap(game_state: dict):
    """ Эта функция имитирует срабатывание ловушки и должна приводить к негативным последствиям для игрока """
    print("Ловушка активирована! Пол стал дрожать...")
    if game_state['player_inventory']:
        inventory_size = len(game_state['player_inventory'])
        random_index = pseudo_random(game_state['steps_taken'], inventory_size)  # Находим рандомный индекс предмета
        lost_item = game_state['player_inventory'].pop(random_index)
        return f'*-* Вы потеряли предмет! == {lost_item} =='

    # Если инвентарь пуст
    else:
        damage = pseudo_random(game_state['steps_taken'], 10)
        if damage < 3:
            game_state['game_over'] = True
            return "Вы не смогли выдержать удар ловушки... Игра окончена!\n*-* Попытайте удачу снова! *-*"
        else:
            return "***** Вам повезло! Вы чудом уцелели! *****"


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
                    game_state['player_inventory'].append('treasure_key')
                    return '^*^ Ваш ответ правильный! Так держать! ^*^\n*** Продолжайте исследовать пространство ***'
                else:
                    return 'Ваш ответ неправильный *_*'

            # Если другой ответ, то просто сравниваем в нижнем регистре
            case answer:
                if player_answer.lower() == answer:
                    ROOMS['current_room']['puzzle'] = None
                    if len(ROOMS['current_room']['items']) > 1:
                        game_state['player_inventory'].append(ROOMS['current_room']['items'][0])
                    return '=== Ваш ответ правильный! Так держать! ===\n*** Продолжайте исследовать пространство ***'
                else:
                    if current_room == 'trap_room':
                        print('О нет! ответ неверный! *.*')
                        return trigger_trap(game_state)
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


def pseudo_random(seed: int, modulo: int) -> int:
    """ будет принимать в качестве параметров число шагов и целое число modulo,
    на выходе мы должны получить целое в диапазоне [0, modulo) """

    # Возьмите синус от seed, умноженного на большое число с дробной частью
    intermediate = seed * 12.9898
    sin_value = math.sin(intermediate)

    # Результат умножьте на другое большое число с дробной частью
    scaled_value = sin_value * 43758.5453
    fractional_part = scaled_value - math.floor(scaled_value)  # Вычесть из числа его целую часть
    scaled_to_modulo = fractional_part * modulo  # Умножьте эту дробную часть на modulo

    # Отбросьте дробную часть и верните целое число
    return int(scaled_to_modulo)


def random_event(game_state: dict):
    """ Создаем небольшие случайные события, которые происходят во время перемещения игрока """
    # Произойдет ли событие вообще
    EVENT_PROBABILITY = 10
    if pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY) == 0:
        event_type = pseudo_random(game_state['steps_taken'], 3)  # Определяем тип события
        match event_type:
            case 1:
                game_state['player_inventory'].append('coin')
                return 'Вы подобрали монетку!\n*** coin ***'
            case 2:
                print('Послышался шорох за спиной... О нет, что это может быть!\nВы тянетесь рукой в карман и...')
                if 'sword' in game_state['player_inventory']:
                    return 'Вы обнаружили мечь у себя и отпугнули враждебное существо!\nТак держать! *_*'
                else:
                    return """ В кармане ничего нет! Закройте глаза и досчитайте до 3, тогда шорох пройдёт...
                    Главное! Не двигайтесь """
            case 3:
                if 'trap_room' == game_state['current_room'] and 'torch' not in game_state['player_inventory']:
                    print('Вас преследует опасность...')
                    return trigger_trap(game_state)
