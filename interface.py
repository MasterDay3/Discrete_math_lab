"""Interface"""
import streamlit as st
# import pandas as pd
# import numpy as np

st.title('Збірка користувацьких замовлень.')
st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)
# st.text('Визначимо, чи можливо зібрати Ваше кастомне замовлення на основі \
# залежностей між компонентами.')
name = st.text_input("Як можна до Вас звертатись?")

# choice = st.slider("Оберіть:")
