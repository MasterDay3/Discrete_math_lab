'''ALGS'''
import data as d

FILENAME = 'big_data_test.txt'

text = d.read_data(FILENAME)
components = text[2][1:]
checked = d.create_comp_dict(text)
user_list = []


# print(components)
# print(checked)
#legit = d.create_packets(text)
#print(legit)


def check_request(request: str) -> bool:
    '''Перевіряє, чи можна додати опцію, якщо можна, повертає True
    Якщо не можна через не сумісніть, повертає False'''
    key = checked[request]
    for ch in key:
        if key[ch] is False and ch in user_list:
            return False
    return True



def add_component(request: str) -> bool:
    '''Додає компоненту до списку бажаних опцій користувача, у випадку
    якщо опцію додати неможливо через те, що вона не сумісна з якоюсь іншою - повертає False
    якщо опцію можна додати, додає опцію та повертає True'''
    if request in components and check_request(request) and request not in user_list:
        user_list.append(request)
        return True
    return False

#test commit

def delete_component(request: str) -> bool:
    '''Видаляє компоненту з обраних
    Повертає True, якщо компоненту видалено і False, якщо її не було в списку'''
    if request in user_list:
        user_list.remove(request)
        return True
    return False











from collections import defaultdict, deque
import re

def parse_dot_file(filename: str):
    """Парсить DOT файл та повертає список ребер"""
    edges = []

    with open(filename, 'r') as f:
        content = f.read()

    # Видаляємо коментарі та зайві пробіли
    content = re.sub(r'//.*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Знаходимо всі ребра
    pattern = r'(\w+)\s*->\s*(-?\w+)'
    matches = re.findall(pattern, content)

    for from_node, to_node in matches:
        edges.append((from_node.strip(), to_node.strip()))

    return edges

def build_adjacency_list(edges):
    """Побудова списку суміжності графа"""
    graph = defaultdict(list)

    for from_node, to_node in edges:
        graph[from_node].append(to_node)
        # Додаємо всі вершини в граф, навіть якщо вони не мають вихідних ребер
        if to_node not in graph:
            graph[to_node] = []

    return graph




# !!!!!!!!!!!!
def has_path(graph, start, target, visited=None):
    """Перевіряє чи існує шлях від start до target за допомогою DFS"""
    if visited is None:
        visited = set()

    if start == target:
        return True

    visited.add(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            if has_path(graph, neighbor, target, visited):
                return True

    return False



# !!!!!!!!!
def has_path_bfs(graph, start, target):
    """Перевіряє чи існує шлях від start до target за допомогою BFS"""
    if start == target:
        return True

    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor == target:
                return True
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False




# !!!!!!!!!!!!!
def check_negative_paths(filename: str):
    """
    Основна функція для перевірки чи можна потрапити
    з вершини v у вершину -v для всіх вершин
    """
    edges = parse_dot_file(filename)
    graph = build_adjacency_list(edges)

    # Знаходимо всі унікальні вершини
    all_vertices = set()
    for from_node, to_node in edges:
        all_vertices.add(from_node)
        all_vertices.add(to_node)

    results = []
    problematic_pairs = []

    # Для кожної вершини перевіряємо чи існує відповідна негативна
    for vertex in sorted(all_vertices):
        # Якщо вершина не починається з "-" і існує відповідна негативна
        # if not vertex.startswith('-'):
        #     negative_vertex = f"-{vertex}"

        #     if negative_vertex in all_vertices:
        # Перевіряємо чи є шлях від vertex до negative_vertex
        negative_vertex = f'-{vertex}'
        if has_path_bfs(graph, vertex, negative_vertex):
            problematic_pairs.append((vertex, negative_vertex))
            results.append(False)
        else:
            results.append(True)

    # Додатково: можна перевірити всі пари
    # print("=" * 50)
    # print("АНАЛІЗ ГРАФА З ФАЙЛУ:", filename)
    # print("=" * 50)
    # print(f"\nВсього вершин: {len(all_vertices)}")
    # print(f"Всього ребер: {len(edges)}")

    if problematic_pairs:
        print(f"\n⚠️  Знайдено проблемні пари ({len(problematic_pairs)}):")
        for v, neg_v in problematic_pairs:
            print(f"  • {v} -> {neg_v} : НЕДОПУСТИМО (є шлях)")

        print(f"\n❌ РЕЗУЛЬТАТ: False")
        print("   Можна потрапити з позитивної вершини до її заперечення")
        return False
    else:
        print(f"\n✅ РЕЗУЛЬТАТ: True")
        print("   Неможливо потрапити з позитивної вершини до її заперечення")
        return True

# def visualize_graph(filename: str):
#     """Візуалізація графа (опціонально)"""
#     try:
#         import networkx as nx
#         import matplotlib.pyplot as plt

#         edges = parse_dot_file(filename)
#         G = nx.DiGraph()

#         for from_node, to_node in edges:
#             G.add_edge(from_node, to_node)

#         plt.figure(figsize=(12, 8))

#         # Розфарбовуємо вершини
#         color_map = []
#         for node in G.nodes():
#             if node.startswith('-'):
#                 color_map.append('lightcoral')  # Червоний для негативних
#             else:
#                 color_map.append('lightblue')   # Синій для позитивних

#         pos = nx.spring_layout(G, k=2, iterations=50)
#         nx.draw(G, pos, with_labels=True, node_color=color_map,
#                 node_size=2000, font_size=10, font_weight='bold',
#                 arrows=True, arrowsize=20)

#         plt.title(f"Граф залежностей з файлу: {filename}", fontsize=14)
#         plt.tight_layout()
#         plt.show()

#     except ImportError:
#         print("\nДля візуалізації потрібно встановити:")
#         print("pip install networkx matplotlib")

# Приклад використання
# if __name__ == "__main__":
#     # Тестовий файл
#     test_content = """comp1 -> comp2
# comp2 -> comp3
# comp3 -> -comp1
# comp4 -> comp5
# comp5 -> -comp4
# comp6 -> comp7"""

#     # Створюємо тестовий файл
#     with open("test_graph.dot", "w") as f:
#         f.write(test_content)

#     # Аналізуємо граф
#     result = check_negative_paths("test_graph.dot")

#     print("\n" + "=" * 50)
#     print("ДОДАТКОВА ІНФОРМАЦІЯ:")
#     print("=" * 50)

#     # Показуємо граф
#     edges = parse_dot_file("test_graph.dot")
#     print("\nРебра графа:")
#     for from_node, to_node in edges:
#         print(f"  {from_node} -> {to_node}")

#     # Аналіз для кожної вершини
#     graph = build_adjacency_list(edges)
#     all_vertices = set()
#     for from_node, to_node in edges:
#         all_vertices.add(from_node)
#         all_vertices.add(to_node)

#     print("\nПеревірка для кожної вершини:")
#     for vertex in sorted(all_vertices):
#         if not vertex.startswith('-'):
#             negative_vertex = f"-{vertex}"
#             if negative_vertex in all_vertices:
#                 has_path = has_path_bfs(graph, vertex, negative_vertex)
#                 status = "НЕДОПУСТИМО" if has_path else "OK"
#                 print(f"  {vertex} -> {negative_vertex}: {status}")

    # Візуалізація (розкоментуйте якщо потрібно)
    # visualize_graph("test_graph.dot")










# TESTS
# if __name__ == '__main__':
#     add_component('Турбінований V8 двигун')
#     add_component('Лазерні фари')
#     #print(add_component('LED-матриця'))
#     delete_component('Лазерні фари')
#     print(user_list)
