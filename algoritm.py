'''ALGS'''

FILENAME = 'big_data_test.txt'


user_list = []
checked = {}


# ======================= НОВІ ФУНКЦІЇ ДЛЯ ПЕРЕВІРКИ НЕОБХІДНОСТІ =====================

def get_only_required(content: list) -> dict:
    '''
    Створює словник односторонніх необхідних компонентів.
    Ключ - компонент, який ВИМАГАЄ, значення - список компонентів, що ВИМАГАЮТЬСЯ.
    (Наприклад, "Турбінований V8 двигун" вимагає "Спортивна трансмісія").

    Args:
        content (list): повний ліст інфи від файлу(всі секції)

    Returns:
        dict: Словник вимог.
    '''
    if not content or len(content) < 5:
        return {}


    txt = content[4][1:]

    required_dict = {}
    for el in txt:
        # comp1 то comp2: comp1 вимагає comp2
        comp1, comp2 = remake_nesessary(el)

        if comp1 not in required_dict:
            required_dict[comp1] = []

        if isinstance(comp2, list):
            required_dict[comp1].extend(comp2)
        else:
            required_dict[comp1].append(comp2)

    return required_dict







def check_dependencies(selected_components: list, required_dict: dict) -> dict:
    """
    Перевіряє, чи всі обрані компоненти мають необхідні (залежні) компоненти.

    Args:
        selected_components (list): Список компонентів, обраних користувачем.
        required_dict (dict): Словник односторонніх вимог (ключ вимагає, значення вимагається).

    Returns:
        dict: Словник, де ключ - компонент, який потребує залежностей,
              а значення - список відсутніх необхідних компонентів.
    """
    incomplete_dependencies = {}
    selected_set = set(selected_components)

    for component in selected_components:
        # Перевіряємо, чи цей компонент вимагає щось
        if component in required_dict:
            missing = []

            for needed_comp in required_dict[component]:

                if needed_comp not in selected_set:
                    missing.append(needed_comp)

            if missing:
                incomplete_dependencies[component] = missing

    return incomplete_dependencies






def _dfs_recursive_helper(graph: dict, current_node: str, target_node: str, visited: set) -> bool:
    """
    Рекурсивна допоміжна функція для пошуку в глибину (DFS).

    Args:
        graph (dict): Словник суміжності.
        current_node (str): Поточна вершина.
        target_node (str): Цільова вершина (антивершина).
        visited (set): Набір вже відвіданих вершин.
    """
    if current_node == target_node:
        return True

    # Якщо вершина - антивершина, ми не продовжуємо пошук, бо антивершини є кінцевими точками в контексті несумісності.
    if current_node.startswith('@') and current_node != target_node:
        return False

    visited.add(current_node)

    if current_node in graph:
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                if _dfs_recursive_helper(graph, neighbor, target_node, visited):
                    return True

    return False



def if_possible_path_dfs(graph: dict, start_node: str, target_node: str) -> bool:
    """
    Перевіряє, чи існує шлях від start_node до target_node, використовуючи DFS.

    Args:
        graph (dict): Словник суміжності графа.
        start_node (str): Початкова вершина.
        target_node (str): Цільова вершина (або антивершина).

    Returns:
        bool: True, якщо шлях існує, інакше False.
    """
    # невідвідані
    visited = set()
    return _dfs_recursive_helper(graph, start_node, target_node, visited)







def parse_graph_to_dict(filename: str = 'main_graph.txt') -> tuple:
    """
    Допоміжна функція для парсингу вмісту файлу main_graph.txt в словник.
    """
    graph = {}
    anti_nodes = set()

    with open(filename, 'r', encoding='utf-8') as file:
        graph_content = file.read()

    lines = graph_content.strip().split('\n')

    for line in lines:
        cleaned_line = line.strip()

        if '->' in cleaned_line:
            parts = cleaned_line.split('->')
            source = parts[0].strip()
            target = parts[1].strip()

            if not source or not target:
                continue

            if source not in graph:
                graph[source] = []

            graph[source].append(target)

            if target.startswith('@'):
                anti_nodes.add(target)

    return graph, anti_nodes










def check_request(request: str, filepath: str = 'main_graph.txt') -> bool:
    '''
    Перевіряє, чи можна додати опцію.
    Якщо компонент несумісний сам із собою (є петля) або з чимось, повертає False.
    '''
    graph_dict, _ = parse_graph_to_dict(filepath)

    return not if_possible_path_dfs(graph_dict, request, f'@{request}')





def add_component(request: str, user_list: list, filename: str = 'main_graph.txt' ) -> bool:
    '''
    Додає компоненту до списку, перевіряючи її сумісність з УСІМА ІНШИМИ вже обраними.
    ПОВЕРТАЄ True, якщо сумісно і додано, інакше False.
    '''
    if request in user_list:
        return True


    temp_list = user_list + [request]


    for existing_comp in temp_list:
        for other_comp in temp_list:
            if existing_comp == other_comp:
                continue

            #  A -> @B
            if not check_full_compatibility([existing_comp], other_comp, filename):
                return False # Знайдено конфлікт!
            #  B -> @A
            if not check_full_compatibility([other_comp], existing_comp, filename):
                 return False


    user_list.append(request)
    return True


def check_full_compatibility(component_list: list, target_component: str, filename: str = 'main_graph.txt') -> bool:
    '''
    Перевіряє, чи кожен компонент у component_list сумісний з target_component
    (тобто, чи немає шляху від ComponentA до @ComponentB).

    target_component використовується для формування анти-вершини.

    Якщо є несумісність: (A і B) -> (A -> @B)
    '''
    graph_dict, anti_nodes = parse_graph_to_dict(filename)
    anti_target = f'@{target_component}'

    for component in component_list:
        # Перевіряємо, чи існує шлях від обраного компонента до анти-вершини цільового
        if if_possible_path_dfs(graph_dict, component, anti_target):
            # Шлях існує, отже, компонент несумісний із цільовим
            return False
    return True







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













def create_comp_dot(filename: str) -> None:
    '''
    makes main graph
    '''

    if not isinstance(filename, str):
        raise ValueError('Неправильний ввід create_comp_dot()')


    content = read_data(filename)


    with open('main_graph.txt', 'w', encoding='utf-8') as file:
        file.write('{\n')

        # необхідності
        for el in content[4][1:]:
            first, second = remake_nesessary(el)
            file.write(f'{first} -> {second}\n')

        # НЕСУМІСНОСТІʼ
        for el in content[3][1:]:
            first_un, second_un = remake(el)

            # Component1 -> @Component2
            file.write(f'{first_un} -> @{second_un}\n')

            #Component2 -> @Component1
            file.write(f'{second_un} -> @{first_un}\n') # <--- ВАЖЛИВО!

    return None







def get_user_graph(filename: str, choice: list, all_comps: set) -> None:
    '''
    lalala
    '''

    if not isinstance(filename, str) or not isinstance(choice, list) or \
            not isinstance(all_comps, set):
        return None

    with open(filename, '+a', encoding='utf-8') as file:
        itter = len(choice)
        used = set()

        for i in range(itter - 1):
            first = choice[i]
            second = choice[i+1]
            used.add(first)
            used.add(second)

            file.write(f'{first} -> {second}\n')

        for el in all_comps:
            if el not in choice:
                file.write(f'{second} -> @{el}\n')

        file.write('}')















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
