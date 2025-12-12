'''
Functions to get data from file
'''



import copy



def read_data(filepath: str) -> list:
    '''
    function to read data from file with certain order
    Приймає назву файлу і повертає списоск списків(секцій) з файлу для подальшої обробки

    Args:
        filepayth (str): path to file
    Returns:
        list: list of sections from file

    '''
    if not isinstance(filepath, str):
        raise ValueError('Неправильний ввід даних у функцію !')

    with open(filepath, 'r', encoding='utf-8') as file:
        all_txt = iter(el.strip() for el in file.readlines() if el.strip())
        # вся дата через генератор для оптиміщації

    whole_sorted = []
    section = []
    for el in all_txt:
        if el.startswith('===== '):
            if section:
                whole_sorted.append(section)
            section = []
        section.append(el)

    if section:
        whole_sorted.append(section)

    return whole_sorted

def create_comp_dict(content: list) -> dict:
    '''
    creates dict of dict with несумісність of components

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        dict: словник з сумісністю елементів(True - сумісні, False - не сумісні)
        (компоненти - ключі зовніщнього,
        наступний компонент - той який хочемо порівняти, і значення буде True/False)

    Приклад:
        dict[Компонент1][Компонент1]
        True
    '''
    if not isinstance(content, list):
        raise ValueError('Некоректний ввід в функцію, перевірте, що ви ввели (create_dict)')
    if not content:
        raise ValueError('Некоректний ввід в функцію, перевірте, що ви ввели (create_dict)')

    try:
        comp_dict = {}

        for el in content[2][1:]:
            # словник для всіх компонент
            comp_dict[el] = {}

            for el1 in content[2][1:]:
                comp_dict[el][el1] = True


        for key, dic in comp_dict.items():

            for el in content[3][1:]:
                # ті які не сумісні False
                comp1, comp2 = remake(el)
                if comp1 == key:
                    dic[comp2] = False
                if comp2 == key:
                    dic[comp1] = False

        return comp_dict
    except Exception:
        raise ValueError('Некоректний ввід в функцію, перевірте,\
що ви ввели у файлі, щось пішло не так')



def create_packets(content: list) -> dict:
    '''
    creates dict with necessary comps

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        dict: словник з пакетами(ключ - назва пакету, значення - список компонентів в пакеті)

    Приклад:
        dict[Пакет1] = [Компонент1, Компонент2, ...]
    '''
    if not isinstance(content, list):
        raise ValueError('Неправильний ввід create_packets()')
    if not content:
        raise ValueError('Неправильний ввід create_packets()')

    try:
        packets = {}
        itter = iter(content[5][1:])

        for el in itter:
            key, value = packet_remake(str(el))
            packets[key] = value

        return packets
    except Exception:
        raise ValueError('Некоректний ввід в функцію, перевірте, що ви ввели у файлі')






def get_uncompatable(content: list) -> dict:
    '''
    Створює словник з несумісністю компонентів

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        dict: словник з сумісністю елементів(True - сумісні, False - не сумісні)
    '''

    if not isinstance(content, list):
        raise ValueError('Неправильний ввід get_uncompatable()')
    if not content:
        raise ValueError('Неправильний ввід get_uncompatable()')

    txt = content[3][1:]

    uncompatable_dict = {}
    for el in txt:
        comp1, comp2 = remake(el)

        if comp1 not in uncompatable_dict:
            uncompatable_dict[comp1] = []

        if comp2 not in uncompatable_dict:
            uncompatable_dict[comp2] = []

        uncompatable_dict[comp1].append(comp2)
        uncompatable_dict[comp2].append(comp1)

    return uncompatable_dict














def get_necessary(content: list) -> dict:
    '''
    Створює словник з необхідними компонентами для кожного компонента

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        dict: словник з необхідними компонентами(ключ - компонент, значення - список необхідних компонентів)
    '''

    if not isinstance(content, list):
        raise ValueError('Неправильний ввід get_necessary()')
    if not content:
        raise ValueError('Неправильний ввід get_necessary()')

    txt = content[4][1:]

    necessary_dict = {}
    for el in txt:
        # спліт за то
        comp1, comp2 = remake_nesessary(el)

        # робимо місце куда пхати
        if comp1 not in necessary_dict:
            necessary_dict[comp1] = []

        if comp2 not in necessary_dict:
            necessary_dict[comp2] = []

        if isinstance(comp2, list):
            # якщо ліст
            necessary_dict[comp1].extend(comp2)
            necessary_dict[comp2].append(comp1)

        else:
            # якщо стрінга
            necessary_dict[comp1].append(comp2)
            necessary_dict[comp2].append(comp1)




    return necessary_dict
















def check(filename: str) -> dict:
    '''
    Функція приймає повний список з файлу (всі дані), і перевіряє, якщо компонента 1 необхідна для комп2, але комп 2 не сумісна з комп3,
    то комп1 несумісна з комп3

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        tuple: кортеж з двох елементів:
            dict: новий словник з сумісністю елементів(True - сумісні, False - не сумісні)
            dict: новий словник з пакетами(ключ - назва пакету, значення - список компонентів в пакеті)
    '''

    if not isinstance(filename, str):
        raise ValueError('Неправильний ввід check()')

    if not filename:
        raise ValueError('Неправильний ввід check()')


    content = read_data(filename)

    necessary = get_necessary(content)
    uncom = get_uncompatable(content)

    new_uncom = copy.deepcopy(uncom)
    new_comp_dict = create_comp_dict(content)


    for comp1 in necessary:
        for comp2 in necessary[comp1]:
            # comp2 несумісний comp3
            if comp2 in uncom:
                for comp3 in uncom[comp2]:

                    #в дві сторони
                    if comp1 not in new_uncom:
                        new_uncom[comp1] = []
                    if comp3 not in new_uncom:
                        new_uncom[comp3] = []

                    if comp3 not in new_uncom[comp1]:
                        new_uncom[comp1].append(comp3)
                    if comp1 not in new_uncom[comp3]:
                        new_uncom[comp3].append(comp1)

                    new_comp_dict[comp1][comp3] = False
                    new_comp_dict[comp3][comp1] = False

    #  comp1 залежить від comp2, а comp2 несумісний з comp3
    reverse_necessary = {}
    for comp1, deps in necessary.items():
        for comp2 in deps:
            if comp2 not in reverse_necessary:
                reverse_necessary[comp2] = []
            reverse_necessary[comp2].append(comp1)


    for comp2 in reverse_necessary:

        for comp1 in reverse_necessary[comp2]:
            # comp1 залежить від comp2
            if comp2 in uncom:
                for comp3 in uncom[comp2]:

                    # comp2 несумісний з comp3
                    if comp1 not in new_uncom:
                        new_uncom[comp1] = []
                    if comp3 not in new_uncom:
                        new_uncom[comp3] = []

                    if comp3 not in new_uncom[comp1]:
                        new_uncom[comp1].append(comp3)
                    if comp1 not in new_uncom[comp3]:
                        new_uncom[comp3].append(comp1)

                    new_comp_dict[comp1][comp3] = False
                    new_comp_dict[comp3][comp1] = False

    return new_comp_dict











def create_comp_dot(filename: str) -> None:
    '''
    makes main graph
    '''

    if not isinstance(filename, str):
        raise ValueError('Неправильний ввід create_comp_dot()')


    content = read_data(filename)

    num = len(content[2])

    # @ не верш


    with open('main_graph.dot', 'w', encoding='utf-8') as file:
        # необхідності
        for el in content[4][1:]:
            first, second = remake_nesessary(el)
            file.write(f"{first} -> {second}\n")

        # несумісності
        for el in content[3][1:]:
            first_un, second_un = remake(el)
            file.write(f'{first_un} -> @{second_un}\n')
            file.write(f'{second_un} -> @{first_un}\n')





def user_graph(filename: str, selected: list, comps: set) -> None:
    '''
    lalala
    '''

    if not isinstance(filename, str):
        raise  ValueError('Неправильний ввід user_graph()')

    with open(filename, 'a', encoding='utf-8') as file:
        itter = len(selected)
        used = set()

        anti_dict = {}

        for el in comps:
            anti_dict[el] = f'-{el}'

        # вибір
        for i in range(0, itter - 1):
            first = selected[i]
            second = selected[i+1]

            file.write(f'{first} -> {second}\n')
            used.add(first)
            used.add(second)

        anti_comps = comps.intersection(used)

        for el in comps:
            for vert in anti_comps:
                if vert not in anti_comps:
                    raise ValueError('нема компоненти в user_graph()')

                if f'{el} -> {vert}':
                    ...


















# ============= Helping functions ==================== #



def remake_nesessary(line: str) -> list:
    '''
    helping function that divides line into parts for necessary components for better handling
    Допоміжна функція, яка ділить рядок на частини для необхідних компонент для кращої обробки

    Args:
        line (str): рядок з необхідними компонентами(Компонент1 необхідний для Компонент2)
    Returns:
        list: список з двох компонентів
    '''

    if not line:
        raise ValueError('Ви погано ввели дані в функцію remake_necessary (пуста)')

    if 'то' not in line:
        raise ValueError('Ви погано ввели дані в функцію remake_necessary (нема "то")')

    parts = line.split(' то ')
    comp1 = parts[0].strip()
    comp2 = parts[1].strip()

    if ',' in comp2:
        comp2 = [el.strip() for el in comp2.split(',')]

    return comp1, comp2






def packet_remake(line: str) -> list:
    '''
    helping function that divides line into parts for packets for better handling
    Допоміжна функція, яка ділить рядок на частини для пакетів для кращої обробки

    Args:
        line (str): рядок з пакетом(назва пакету: компонент1, компонент2,...)

    Returns:
        list: список з назвою пакету і списком компонентів в ньому
    '''
    if not isinstance(line, str):
        raise ValueError('Ви погано ввели дані в функцію packet_remake')
    if not line:
        raise ValueError('Ви погано ввели дані в функцію packet_remake')

    parts = line.split(':')
    if len(parts) != 2:
        raise ValueError('Ви погано ввели дані в функцію packet_remake')

    key = parts[0].strip()
    value = [el.strip() for el in parts[1].strip().split(',')]

    return key, value










def remake(line: str) -> list:
    '''
    divides line into parts
    Допоміжна функція, яка ділить рядок на частини за словом "і"

    Args:
        line (str): рядок з двома компонентами(Компонент1 і Компонент2)

    Returns:
        list: список з двох компонентів
    '''
    if not isinstance(line, str):
        raise ValueError('Ви погано ввели дані в функцію remake')

    parts = line.split(' і ')

    if len(parts) != 2:
        raise ValueError('Ви погано ввели дані в функцію remake')

    return parts[0].strip(), parts[1].strip()






# ========================== Testing ========================== #

# FILENAME = 'big_data_test.txt'
# FILENAME = 'data.txt'
FILENAME = 'big_data_test.txt'
all_txt1 = read_data(FILENAME)
comp_dict1 = create_comp_dict(all_txt1)
packets1 = create_packets(all_txt1)

new_comp = check(FILENAME)

# print(all_txt1)
create_comp_dot(FILENAME)
# print('-------------------')
# print(comp_dict1)
# print('-------------------')
# print(packets1)
# print('-------------------')
# print(get_necessary(all_txt1))
# print('-------------------')
# print(get_uncompatable(all_txt1))
# print('-------------------')
# print(new_comp)
# print('-------------------')







# # ========== лютий тестінг ========== #
# # a = {'w': 2, 'x': 3, 'y': 4}
# # i = 4

# # if i in a.values():
# #     print('yes')
