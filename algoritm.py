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




# TESTS
# if __name__ == '__main__':
#     add_component('Турбінований V8 двигун')
#     add_component('Лазерні фари')
#     #print(add_component('LED-матриця'))
#     delete_component('Лазерні фари')
#     print(user_list)
# wfdswvc