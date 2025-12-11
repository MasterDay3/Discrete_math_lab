"""Interface"""
import streamlit as st
from data import create_comp_dict, read_data, create_packets, get_necessary
from algoritm import add_component, check_request, user_list, checked

FILENAME = "big_data_test.txt"
# FILENAME = "data_test.txt"

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

def tick_boxes_from_packets(packets: dict):
    """
    Вибирає всі чекбокси компонентів коли натиснуто кнопку пакета.
    Пакет вміщає в собі декілька компонентів.
    """
    x = len(packets)
    cols = st.columns(x)
    for index, (but, val) in enumerate(packets.items()):
        with cols[index % x]:
            if st.button(but):
                for i in val:
                    st.session_state[f"item_{i}"] = True

                st.success(f"Пакет '{but}' активовано!")


def order(data: dict, num: int = 4):

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

    selected = [comp for comp in data if st.session_state[f"item_{comp}"]]
    incompatibe = [comp for comp in selected if not add_component(comp)]
    # incomplete = []
    # incomplete = get_necessary(selected)
    user_list.clear()

    if not selected:
        st.warning("Не вибрано нічого")
        return None

    # errors = []
    # for comp in selected:
    #     if not add_component(comp):
    #         errors.append(comp)

    # if incomplete:
    #     for comp, needed in incomplete.items():
    #         st.write(f"Компонента **{comp}** потребує: {needed}")

    if incompatibe:
        st.error("Замовлення неможливо зібрати через несумісність!")
        for err in incompatibe:
            st.write(f"Компонент **{err}** конфліктує з:")

            for other, compat in checked[err].items():
                if compat is False and other in selected:
                    st.write(f"**{other}**")
        return None

    # Якщо все норм
    st.success("Замовлення успішно зібране!")
    st.write("Ваші вибрані компоненти:")
    st.write(selected)
    # список обраних компонент
    return selected



def main():
    """
    Основна функція виводу інтерфейсу
    """
    st.set_page_config(layout="wide")
    all_txt1 = read_data(FILENAME)
    comp_dict = create_comp_dict(all_txt1)
    packets = create_packets(all_txt1)

    name = introduction()
    show_header_name(all_txt1)
    # show_components_checkboxes(comp_dict)
    # show_packets_checkboxes(packets)
    tick_boxes_from_packets(packets)
    order(comp_dict, 5)
    #final_button(name)

if __name__ == "__main__":
    main()
