""" Desc """

# Only trash here
# Put here anything you want


import streamlit as st
# import pandas as pd
# import numpy as np

from data import create_comp_dict, read_data
# from algoritm import check_request

st.title('Збірка користувацьких замовлень.')
st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)

FILENAME = "data_test.txt"
all_txt1 = read_data(FILENAME)
comp_dict = create_comp_dict(all_txt1)

_order = []

def g(lst: list, val):
    return lst.append(val)


def show_components_checkboxes(components: dict, column_count: int = 4):
    """
    Виводить всі компоненти на екран як чекбокси і повертає обрані.
    """
    st.subheader("Виберіть компоненти для збірки замовлення:")


    column = st.columns(column_count)
    i = 0

    for component in components:
        column[i % column_count].checkbox(component, key = f"comp_{i}", on_change = g(_order, component))
        i += 1


def f():
    st.write(_order)


with st.form(key = "or"):
    show_components_checkboxes(comp_dict)
    st.form_submit_button("ASSEMBLE", on_click = f, key = "assemble")
