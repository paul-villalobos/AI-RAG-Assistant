import streamlit as st

import openai

st.title("Chatbot")

openai.api_key = st.secrets['OPENAI_API_KEY']

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Inicializar chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Reaccionar al user input
prompt = st.chat_input("Escribe tu mensaje")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agregar mensaje al chat history
    st.session_state.messages.append({"role":"user", "content":prompt})

    # Mostrar respuesta
    with st.chat_message("assistant"):
        stream = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["messages"]
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role":"assistant", "content":response})
