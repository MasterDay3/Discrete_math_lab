"""   ### ONLY TRASH AND TESTS HERE ###   """

from data import create_comp_dict, read_data
# from algoritm import check_request

import streamlit as st
# import pandas as pd
# import numpy as np

# FILENAME = "data_test.txt"
FILENAME = "big_data_test.txt"
all_txt1 = read_data(FILENAME)
components = create_comp_dict(all_txt1)

# def show_components_checkboxes(components: dict, column_count: int = 4):
#     """
#     Виводить всі компоненти на екран як чекбокси і повертає обрані.
#     """
#     st.subheader("Виберіть компоненти для збірки замовлення:")

#     column = st.columns(column_count)
#     i = 0

#     for component in components:
#         column[i % column_count].checkbox(component, key = f"comp_{i}", on_change = g(_order, component))
#         i += 1

# with st.form(key = "or"):
#     show_components_checkboxes(comp_dict)
#     st.form_submit_button("ASSEMBLE", on_click = f, key = "assemble")


# components = {'ZZZ': {'PPP', 'AAA'}, 'PPP': {'ZZZ'}, 'AAA': {'ZZZ', 'WWW', 'FFF'}, 'WWW': {'AAA'}, 'FFF': {'AAA', 'XXX'}, 'XXX': {'FFF'}}

with st.form(key = "order"):
    for item in components:
        # проходить по кожній компоненті зі списку і створює сесію для неї, якщо не було
        if f"item_{item}" not in st.session_state:
            # закидує в сесію деякий ключ, який потім буде прив'язаний до галочки
            st.session_state.setdefault(f"item_{item}", False)

    for item in components:
        # створює галочки з ключем із сесії
        st.checkbox(item, key = f"item_{item}")

    if st.form_submit_button("SUBMIT", key = "ASSEMBLE"):
        # при кожній відправці форми закидаються компоненти з галочкою
        selected = {item for item in components if st.session_state[f"item_{item}"]}

        if selected: # відправка в функцію
            if "Турбінований V8 двигун" in selected and "Карбоновий дах" in selected: # прописати функцію перевірки
                st.error(f"CONFLICT ORDER: {selected}")
            else: # додати ще шось
                st.success(f"SUCCESS: {selected}")
