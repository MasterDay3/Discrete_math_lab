'''
Create data from file
'''


# example
FILENAME = 'data.txt'

def read_data(filepath: str) -> list:
    '''
    function to read data from file with certain order
    '''

    if not isinstance(filepath, str):
        raise ValueError('Неправильний ввід даних у функцію !')


    with open(filepath, 'r', encoding='utf-8') as file:
        all_txt = [el.strip() for el in file.readlines() if el.strip()]

    whole_sorted = []
    section = []
    for el in all_txt:
        if el.startswith('===== '):
            if section:
                whole_sorted.append(section)
            section = []

        section.append(el)

    return whole_sorted



def create_comp_dict(content: list) -> dict:
    '''
    creates dict of dict with сумісність of components
    '''

    if not isinstance(content, list):
        raise ValueError('Некоректний ввід в функцію, перевірте, що ви ввели (create_dict)')

    if not content:
        raise ValueError('Некоректний ввід в функцію, перевірте, що ви ввели (create_dict)')

    comp_dict = {}
    for el in content[2][1:]:
        comp_dict[el] = dict()

        for el1 in content[2][1:]:
            comp_dict[el][el1] = False


    for key, dic in comp_dict.items():

        for el in content[3][1:]:
            comp1, comp2 = remake(el)

            if comp1 == key:
                dic[comp2] = True

            if comp2 == key:
                dic[comp1] = True

    return comp_dict





def create_necessary(content: list) -> dict:
    '''
    creates dict with necessary comps
    '''

    if not isinstance(content, list):
        raise ValueError('Направильний ввід create_necessary()')

    if not content:
        raise ValueError('Направильний ввід create_necessary()')







def remake(line: str) -> list:
    '''
    devides line into parts
    '''
    if not isinstance(line,str):
        raise ValueError('Ви погано ввели дані в функцію remake')

    parts = line.split('і')

    if len(parts) != 2:
        raise ValueError('Ви погано ввели дані в функцію remake')

    return parts[0].strip(), parts[1].strip()







all_text = read_data(FILENAME)
diction = create_comp_dict(all_text)
