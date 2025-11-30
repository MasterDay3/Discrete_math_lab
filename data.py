'''
Functions to get data from file
'''




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

# ============= Helping functions ==================== #

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

    parts = line.split('і')

    if len(parts) != 2:
        raise ValueError('Ви погано ввели дані в функцію remake')

    return parts[0].strip(), parts[1].strip()




# ========================== Testing ========================== #

# FILENAME = 'data.txt'

# all_txt1 = read_data(FILENAME)
# comp_dict1 = create_comp_dict(all_txt1)
# packets1 = create_packets(all_txt1)

# # print(all_txt1)
# print('-------------------')
# print(comp_dict1)
# print('-------------------')
# print(packets1)
