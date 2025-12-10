"""Interface"""
import streamlit as st
from data import create_comp_dict, read_data, create_packets
from algoritm import check_request, add_component

# import pandas as pd
# import numpy as np

FILENAME = "data_test.txt"

st.set_page_config(layout="wide")

def introduction():
    st.title('Збірка користувацьких замовлень.')
    name = st.text_input("Введіть своє ім'я:")

    if name:
        st.markdown(f"<span style='color:blue;'>Вітаємо, {name}!</span>", unsafe_allow_html=True)

    st.markdown(
        "<span style='color:blue;'>Визначимо, чи можливо зібрати Ваше кастомне "
        "замовлення на основі залежностей між компонентами.</span>",
        unsafe_allow_html=True
    )
    return name

# def final_button(name):
#     if st.button("Зібрати замовлення"):
#         #success = add_component()  # тут я поміняю функцію
#         #st.session_state["order_success"] = success

#     if "order_success" in st.session_state:
#         if st.session_state["order_success"]:
#             st.markdown(
#                 f"<div style='padding:50px; font-size:32px; color:green; text-align:center;'>"
#                 f"Вітання {name if name else 'користувач'}! Все добре, замовлення прийнято!"
#                 "</div>",
#                 unsafe_allow_html=True
#             )
#         else:
#             st.markdown(
#                 f"<div style='padding:50px; font-size:32px; color:red; text-align:center;'>"
#                 f"{name if name else 'Кристувачу'}, на жаль, суміжність між \
#                 компонентами відсутня. Замовлення не виконане."
#             )

#             if st.button("Повернутися до вибору компонентів"):
#                 del st.session_state["order_success"]  #очистити стан
#                 st.rerun()

# all_txt1 = read_data(FILENAME)
# comp_dict = create_comp_dict(all_txt1)


def show_header_name(all_text: list):
    for i in all_text:
        if '===== Назва =====' in i:
            st.title(i[1])


def show_components_checkboxes(components: dict, column_count: int = 8):
    """
    Виводить всі компоненти як чекбокси.
    """
    st.subheader("Виберіть компоненти для збірки замовлення:")

    for component in components:
        if component not in st.session_state:
            st.session_state[component] = False

    columns = st.columns(column_count)
    i = 0

    for component in components:
        columns[i % column_count].checkbox(component, key=component)
        i += 1

def show_packets_buttons(packets: dict, column_count: int = 8):
    """
    Виводить кнопки пакетів.
    """
    st.subheader("Виберіть пакет:")
    columns = st.columns(column_count)
    i = 0

    chosen_packet = None

    for packet in packets:
        if columns[i % column_count].button(packet):
            chosen_packet = packet
        i += 1

    return chosen_packet


def tick_boxes_from_packets(packets, chosen_packet):
    """
    Якщо натиснута кнопка пакета —
    відмічає відповідні компоненти.
    """
    if not chosen_packet:
        return

    for comp in packets[chosen_packet]:
        st.session_state[comp] = True

    st.success(f"Пакет '{chosen_packet}' активовано!")

def main():

    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)
    packets = create_packets(all_txt1)

    name = introduction()
    show_header_name(all_txt1)

    chosen_packet = show_packets_buttons(packets)
    tick_boxes_from_packets(packets, chosen_packet)

    show_components_checkboxes(comp_dict)

    # final_button(name, comp_dict)


if __name__ == "__main__":
    main()