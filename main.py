import streamlit as st
from streamlit_option_menu import option_menu
import hello_page, productos_page


def configurar_pagina():
    """Configura los parámetros iniciales de la página."""
    st.set_page_config(page_title="Productos - Laive IA")
    st.session_state.setdefault('useremail', None)


def obtener_estado_usuario():
    """Determina si el usuario está autenticado."""
    return bool(st.session_state['useremail'])


def mostrar_menu(is_logged_in):
    """Muestra el menú de navegación lateral basado en el estado del usuario."""
    with st.sidebar:
        opciones = ["Productos"] if is_logged_in else ["Hola"]
        iconos = ["check2-square"] if is_logged_in else ["house-fill"]
        return option_menu(menu_title="Asistente IA", options=opciones, icons=iconos, default_index=0)


def ejecutar_app():
    """Ejecuta la aplicación en función de la opción seleccionada."""
    configurar_pagina()
    is_logged_in = obtener_estado_usuario()
    app_seleccionada = mostrar_menu(is_logged_in)

    if app_seleccionada == "Hola":
        hello_page.app()
    elif app_seleccionada == "Productos":
        productos_page.app()


if __name__ == "__main__":
    ejecutar_app()
