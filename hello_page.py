import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def conectar_bd():
    """Establece la conexión con MongoDB usando la cadena de conexión de Streamlit secrets."""
    cnx_string = st.secrets["MONGODB-CNX"]
    return MongoClient(cnx_string, server_api=ServerApi('1'))


def guardar_usuario(nombre: str, email: str):
    """Guarda o actualiza la información del usuario en la base de datos."""
    client = conectar_bd()
    db = client["laive"]
    usuarios_clx = db["usuarios"]

    filtro = {"email": email}
    datos = {"$set": {"nombre": nombre, "email": email}}

    usuarios_clx.update_one(filtro, datos, upsert=True)


def app():
    """Interfaz de bienvenida para los usuarios."""
    st.title('¡Hola!')
    st.write(
        'Soy una IA especializada en información técnica y comercial de los productos de LAIVE')
    st.write('Mi objetivo es ayudar a la fuerza de ventas a absolver las dudas y consultas de productos que reciben de parte de sus clientes')

    # Inputs de usuario
    nombre = st.text_input('Nombre')
    email = st.text_input("Email", key="email_input")

    if st.button('Empezar a Conversar!'):
        with st.spinner('Procesando... Por favor, espera.'):
            guardar_usuario(nombre, email)

        # Actualizar valores de sesión
        st.session_state.update({
            'username': nombre,
            'useremail': email,
        })

        # Recargar la aplicación para reflejar los cambios
        st.rerun()
