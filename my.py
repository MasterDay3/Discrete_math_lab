"""   ### ONLY TRASH AND TESTS HERE ###   """

import streamlit as st
from data import create_comp_dict, read_data, create_packets
from algoritm import check_request, add_component

# FILENAME = "data_test.txt"

# ===========================================


def introduction():

    """
    Docstring for introduction
    """

    st.title('Збірка користувацьких замовлень.')
    name = st.text_input("Введіть своє ім'я:")
    if name:
        st.write(f"<span style='color: blue;'>Вітаємо, {name}!\n</span>", unsafe_allow_html=True)
    st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
    кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)
    return name


def show_header_name(all_text: list):

    """
    Docstring for show_header_name

    :param all_text: Description
    :type all_text: list
    """

    for i in all_text:
        if '===== Назва =====' in i:
            st.title(i[1])



def show_packets_checkboxes(packets: dict, column_count: int = 4):
    """
    Виводить всі пакети на екран з вибраною
    довжиною рядків(column_count) як чекбокси і повертає обрані.
    """

    st.subheader("Виберіть пакети:")
    column = st.columns(column_count)
    i = 0

    for packet in packets:
        column[i % column_count].button(packet)
        i += 1


def tick_boxes_from_packets(components: dict, packets: dict):
    """
    Вибирає всі чекбокси компонентів коли натиснуто кнопку пакета.
    Пакет вміщає в собі декілька компонентів.
    """

    for packet, comp_list in packets.items():

        # КНОПКА ПАКЕТА
        if st.button(packet):

            for comp in comp_list:
                st.session_state[comp] = True

            st.success(f"Пакет '{packet}' активовано!")


# def main():

#     """
#     Основна функція виводу інтерфейсу
#     """

#     all_txt1 = read_data(FILENAME)
#     comp_dict = create_comp_dict(all_txt1)
#     packets = create_packets(all_txt1)

#     name = introduction()
#     show_header_name(all_txt1)
#     # show_components_checkboxes(comp_dict)
#     show_packets_checkboxes(packets)
#     tick_boxes_from_packets(comp_dict, packets)
    # order()
    # package()
    #final_button(name)


# FILENAME = "data_test.txt"
# FILENAME = "big_data_test.txt"
# all_txt = read_data(FILENAME)
# components = create_comp_dict(all_txt)

def order(data, num: int = 4):

    """Main Data"""

    with st.form(key = "Order"):
        cols = st.columns(num)

        for index, k in enumerate(data):
            col_index = index % num

            if f"item_{k}" not in st.session_state:
                st.session_state[f"item_{k}"] = False

            with cols[col_index]:
                st.checkbox(k, key = f"item_{k}")

        if st.form_submit_button("SUBMIT", key = "ASSEMBLE"):
            selected = [item for item in data if st.session_state[f"item_{item}"]]

            if selected:
                st.success(selected) # функції миколи
            else:
                st.error(selected)

def package(data: dict):

    """ dfghf """

    for but, val in data.items():
        if st.button(but):
            for i in val:
                st.session_state[f"item_{i}"] = True

    # for packet, comp_list in packets.items():

    #     # КНОПКА ПАКЕТА
    #     if st.button(packet):

            # for comp in comp_list:
            #     st.session_state[comp] = True

    #         st.success(f"Пакет '{packet}' активовано!")

d = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n']
b = {"A": {"b", "c", "d"}, "B": {"f", "h"}, "C": {"a", "k"}}


package(b)
order(d, 5)


# if __name__ == "__main__":
#     main()
