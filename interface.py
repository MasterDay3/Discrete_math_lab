"""Interface"""
import streamlit as st
from data import create_comp_dict, read_data, create_packets
from algoritm import check_request

FILENAME = "data_test.txt"

def introduction():
    """Вивід заголовку та привітання"""
    st.title('Збірка користувацьких замовлень.')
    name = st.text_input("Введіть своє ім'я:")
    if name:
        st.write(f"<span style='color: blue;'>Вітаємо, {name}!\n</span>", unsafe_allow_html=True)
    st.markdown("<span style='color: blue;'>Визначимо, чи можливо зібрати Ваше \
    кастомне замовлення на основі залежностей між компонентами.</span>", unsafe_allow_html=True)
    return name


# def final_button(name):
#     """
#     Кнопка для завершення замовлення з перевіркою залежностей.
#     """
#     if st.button("Зібрати замовлення"):
#         success =
#         st.session_state["order_success"] = success

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
#                 del st.session_state["order_success"]
#                 st.rerun()

def show_header_name(all_text: list):
    """Вивід назви із файлу"""
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


def order(data):

    """Main Data"""

    with st.form(key = "Order"):
        cols = st.columns(4)

        for index, item in enumerate(data):
            col_index = index % 4

            if f"item_{item}" not in st.session_state:
                st.session_state.setdefault(f"item_{item}", False)

            with cols[col_index]:
                st.checkbox(item, key = f"item_{item}")

        if st.form_submit_button("SUBMIT", key = "ASSEMBLE"):
            selected = {item for item in data if st.session_state[f"item_{item}"]}

            if selected:
                st.success(selected)
            else:
                st.error(selected)



def main():
    """
    Основна функція виводу інтерфейсу
    """
    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)
    packets = create_packets(all_txt1)

    name = introduction()
    show_header_name(all_txt1)
    show_components_checkboxes(comp_dict)
    show_packets_checkboxes(packets)
    tick_boxes_from_packets(comp_dict, packets)
    #final_button(name)

if __name__ == "__main__":
    main()
