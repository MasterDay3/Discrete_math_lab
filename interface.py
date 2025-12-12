"""Interface"""
import streamlit as st

from algoritm import (
    read_data, create_packets,
    add_component, check_request,
    get_only_required, check_dependencies,
    create_comp_dot,
    check_full_compatibility # <--- ДОДАЙТЕ ТУТ
)
import argparse
import sys
import os

user_list = []
FILENAME = "big_data_test.txt"
# FILENAME = "data_test.txt"


def create_comp_dict(all_text: list) -> dict:
    """Створює словник компонентів з файлу."""
    if len(all_text) > 2 and all_text[2]:
        return {comp: False for comp in all_text[2][1:]}
    return {}






def introduction():
    '''
    ?????????????
    '''
    st.title('Збірка користувацьких замовлень.')
    name = st.text_input("Введіть своє ім'я:")
    if name:
        st.write(f"<span style='color: blue;'>Вітаємо, {name}!\n</span>", unsafe_allow_html=True)
    st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
    кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)
    return name





def show_header_name(all_text: list):
    '''
    ???????????
    '''
    for i in all_text:
        if '===== Назва =====' in i:
            st.title(i[1])










def tick_boxes_from_packets(packets: dict):
    """
    Вибирає всі чекбокси компонентів коли натиснуто кнопку пакета.
    Це забезпечує єдиний вигляд за рахунок групування.
    """
    x = len(packets)
    cols = st.columns(x)
    for index, (but, val) in enumerate(packets.items()):
        with cols[index % x]:
            if st.button(but):
                for i in val:
                    st.session_state[f"item_{i}"] = True

                st.success(f"Пакет '{but}' активовано!")















def order(data: dict, all_txt: list, num: int = 4):

    """Main Data"""

    with st.form(key = "OrderForm"):
        cols = st.columns(num)

        for index, component in enumerate(data):
            key = f"item_{component}"

            if key not in st.session_state:
                st.session_state[key] = False

            with cols[index % num]:
                st.checkbox(component, key=key)

        submited = st.form_submit_button("SUBMIT")


    if not submited:
        return

    # обрані компоненти
    selected = [comp for comp in data if st.session_state[f"item_{comp}"]]

    if not selected:
        st.warning("Не вибрано жодного компонента. Будь ласка, виберіть опції для збірки.")
        return None

    # чистимо userlist
    user_list.clear()

    # несумісності ?
    incompatibe = []

    # перевіряємо кожну пару
    for i in range(len(selected)):
        for j in range(i + 1, len(selected)):
            comp1 = selected[i]
            comp2 = selected[j]

            # A -> @B
            if not check_full_compatibility([comp1], comp2, FILENAME):
                incompatibe.append(f"{comp1} і {comp2}")

            # B -> @A
            if not check_full_compatibility([comp2], comp1, FILENAME):

                if f"{comp2} і {comp1}" not in incompatibe:
                    incompatibe.append(f"{comp2} і {comp1}")
                    # додаємо лише якщо конфлікт ще не зафіксовано у протилежному порядку

    if incompatibe:
        st.error("Замовлення неможливо зібрати через несумісність!")
        st.write("Виявлені конфлікти між компонентами:")
        for conflict in incompatibe:
            st.write(f"**{conflict}**")
        return None

    # необхідність
    required_dict = get_only_required(all_txt)
    incomplete = check_dependencies(selected, required_dict)


    # ================== РЕЗУЛЬТАТИ ==================

    if incomplete:
        st.warning("Необхідні компоненти відсутні:")
        for comp, needed in incomplete.items():
            # який і зо хоче
            st.write(f"Компонента **{comp}** потребує: **{', '.join(needed)}**")
        user_list.clear()
        return None

    # якщо все норм
    st.success(" Супер! Ваше замовлення можливе. Ви зробили своє замовлення!")
    st.write("Ваші вибрані компоненти:")
    st.code('\n'.join(selected))

    user_list.clear() # очищуємо для наступного замовлення
    return selected




def main():
    """
    Основна функція виводу інтерфейсу
    """
    st.set_page_config(layout="wide")


    create_comp_dot(FILENAME)

    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)
    packets = create_packets(all_txt1)

    name = introduction()
    show_header_name(all_txt1)

    # ВИГЛЯД: Групуємо чекбокси за Пакетами
    st.subheader("Виберіть компоненти для збірки замовлення:")
    tick_boxes_from_packets(packets)

    # ФУНКЦІОНАЛЬНІСТЬ: Передаємо дані для перевірки сумісності та необхідності
    order(comp_dict, all_txt1, 5)





#  вирішити !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#  |
#  |
# \_/





# # ==============================================================================
# # ARGPARSE БЛОК
# # ==============================================================================

# # ==============================================================================
# #                      ПУЛЬТ КЕРУВАННЯ (ARGPARSE БЛОК)
# # ==============================================================================

# import argparse

# # Цей код запускається, ТІЛЬКИ якщо ви запускаєте файл algoritm.py напряму
# if __name__ == '__main__':

#     # 1. Створюємо наш "Пульт"
#     parser = argparse.ArgumentParser(
#         description="Утиліта для перевірки збірки. Обирай, що робити далі."
#     )

#     # 2. Створюємо "Кнопки" (команди)
#     # required=True означає, що користувач має натиснути хоча б одну кнопку
#     subparsers = parser.add_subparsers(
#         dest='command',
#         required=True,
#         help='Вибери одну з команд: create_graph, check_compatibility, check_deps.'
#     )


#     # --- КНОПКА 1: Створити Граф (create_graph) ---
#     parser_create = subparsers.add_parser(
#         'create_graph',
#         help='Створює файл main_graph.txt на основі big_data_test.txt.'
#     )
#     parser_create.add_argument(
#         '--filename',
#         type=str,
#         default=FILENAME,
#         help='Назва файлу з даними (за замовчуванням: big_data_test.txt).'
#     )


#     # --- КНОПКА 2: Перевірити Сумісність (check_compatibility) ---
#     parser_check_req = subparsers.add_parser(
#         'check_compatibility',
#         help='Перевіряє, чи не конфліктує ОДИН компонент.'
#     )
#     parser_check_req.add_argument(
#         'component',
#         type=str,
#         help='Назва компонента, який перевіряємо.'
#     )


#     # --- КНОПКА 3: Перевірити Залежності (check_deps) ---
#     parser_check_dep = subparsers.add_parser(
#         'check_deps',
#         help='Перевіряє, чи всі компоненти у списку мають необхідні для них деталі.'
#     )
#     # components_list - це список компонентів, розділених пробілами.
#     parser_check_dep.add_argument(
#         'components_list',
#         type=str,
#         nargs='+',  # Очікує одне або більше слів
#         help='Список компонентів через пробіл.'
#     )


#     # 3. Зчитуємо, що ти натиснув
#     args = parser.parse_args()


#     # 4. Виконуємо дію відповідно до натиснутої кнопки

#     if args.command == 'create_graph':
#         try:
#             create_comp_dot(args.filename)
#             print("Граф main_graph.txt успішно створено.")
#         except Exception as e:
#             print(f" Помилка: {e}")


#     elif args.command == 'check_compatibility':

#         graph_file = 'main_graph.txt'

#         try:
#             is_compatible = check_request(args.component, graph_file)

#             if is_compatible:
#                 print(f" Компонент '{args.component}' сумісний.")
#             else:
#                 print(f"Компонент '{args.component}' НЕСУМІСНИЙ.")
#         except Exception as e:
#             print(f"Помилка при перевірці: {e}")


#     elif args.command == 'check_deps':

#         try:
#             # 1. Читаємо всі дані
#             all_txt = read_data(FILENAME)
#             required_dict = get_only_required(all_txt)

#             # 2. Перевіряємо залежності для нашого списку
#             incomplete = check_dependencies(args.components_list, required_dict)

#             if not incomplete:
#                 print(" Залежності задоволені.")
#             else:
#                 print(" Виявлені відсутні залежності:")
#                 for comp, needed in incomplete.items():
#                     print(f" - Компонент '{comp}' потребує: {', '.join(needed)}")
#         except Exception as e:
#             print(f" Помилка при перевірці залежностей: {e}")

# # ==============================================================================



if __name__ == "__main__":
    main()
