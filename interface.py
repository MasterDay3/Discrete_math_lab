"""Interface"""
import streamlit as st
# import pandas as pd
# import numpy as np

"""Імпортуєм інші модулі"""
from data import create_comp_dict, read_data
from algoritm import check_request

st.title('Збірка користувацьких замовлень.')
st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)

FILENAME = "data_test.txt"
all_txt1 = read_data(FILENAME)
comp_dict = create_comp_dict(all_txt1)

def show_header_name(all_text: list):
    for i in all_text:
        if '===== Назва =====' in i:
            st.title(i[1])


def show_components_checkboxes(components: dict, column_count: int = 4):
    """
    Виводить всі компоненти на екран з вибраною
    довжиною рядків(column_count) як чекбокси і повертає обрані.
    """
    st.subheader("Виберіть компоненти для збірки замовлення:")

    column = st.columns(column_count)
    i = 0

    for component in components:
        column[i % column_count].checkbox(component)
        i += 1

def main():
    """
    Основна функція виводу інтерфейсу
    """
    show_header_name(all_txt1)
    show_components_checkboxes(comp_dict)
    st.title('Збірка користувацьких замовлень.')
    st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
    кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)

    FILENAME = "data_test.txt"
    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)

show_header_name(all_txt1)
show_components_checkboxes(comp_dict)



