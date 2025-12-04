"""Interface"""
import streamlit as st
from data import create_comp_dict, read_data
from algoritm import check_request, add_component

# import pandas as pd
# import numpy as np

FILENAME = "data_test.txt"

def introduction():
    st.title('Збірка користувацьких замовлень.')
    name = st.text_input("Введіть своє ім'я:")
    if name:
        st.write(f"<span style='color: blue;'>Вітаємо, {name}!</span>", unsafe_allow_html=True)
        return name
    st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
    кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)
    

def final_button(name):
    if st.button("Зібрати замовлення"):
        if add_component():
            st.markdown(
                f"<div style='padding:50px; font-size:32px; color:green; text-align:center;'>"
                f"Вітання {name if name else 'користувач'}! Все добре, замовлення прийнято!"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='padding:50px; font-size:32px; color:red; text-align:center;'>"
                f"Шановний {name if name else 'користувач'}, на жаль, суміжність між компонентами відсутня. Замовлення не виконане."
            )
        
# all_txt1 = read_data(FILENAME)
# comp_dict = create_comp_dict(all_txt1)

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
    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)

    name = introduction()
    show_header_name(all_txt1)
    show_components_checkboxes(comp_dict)
    final_button(name)

if __name__ == "__main__":
    main()