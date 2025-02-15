from dotenv import load_dotenv
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory


class ConsultorDeVentas:
    """
    Clase que representa un consultor de ventas basado en IA, diseñado para ayudar a las empresas
    a conocer mejor a sus clientes a través de encuestas personalizadas.
    """
    CNX_STRING = os.getenv("MONGODB-CNX")

    def __init__(self, session_id: str, username: str):
        load_dotenv()
        self.session_id = session_id
        self.username = username
        self.chat_model = ChatOpenAI(model="gpt-4o-mini")
        self.chain_with_history = self._configure_chat_chain()

    def _configure_chat_chain(self):
        """Configura el pipeline de chat con historial de mensajes."""
        system_message = f"""
        Eres el asistente virtual de Laive, diseñado para ayudar a los vendedores de Laive y a los vendedores de las distribuidoras de Laive. Tu propósito es brindar información precisa y útil sobre los productos de Laive, ayudando a resolver consultas técnicas y comerciales relacionadas con el portafolio de productos.

Usuarios Objetivo:
- Vendedores de Laive
- Vendedores de las distribuidoras de Laive

Los vendedores trabajan con el sector HORECA, atendiendo a:
- Restaurantes
- Pizzerías
- Hoteles
- Caterings
- Otros negocios gastronómicos


Dentro de estos negocios, los principales clientes finales son:
- Chefs
- Cocineros
- Técnicos de pastelería
- Otros profesionales gastronómicos


Tipos de Consultas que Responde el Chatbot:
1. Consultas Técnicas
- Características de los productos (composición, porcentaje de grasa, humedad, etc.).
- Usos recomendados (pizzas, postres, salsas, rellenos, etc.).
- Comparaciones entre productos (ejemplo: diferencias entre quesos mozzarella nacionales e importados).
- Condiciones de almacenamiento y conservación.
- Tiempos de vida útil y caducidad.

Estilo de Comunicación del Chatbot:
- Profesional, pero cercano y práctico.
- Responde con precisión y claridad.
- Utiliza ejemplos y recomendaciones basadas en el uso real de los productos en el sector HORECA.
- En caso de consultas fuera de su alcance, sugiere contactar a un asesor comercial o técnico de Laive.

Límites y Restricciones del Chatbot:
- No debe proporcionar precios específicos a clientes finales, solo a vendedores.
- No debe ofrecer información interna confidencial de Laive.
- No debe dar recomendaciones que contradigan las especificaciones técnicas de los productos.

Estás conversando con el usuario que se llama {self.username}
        """

        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template(template='{question}')
        ])

        chat_chain = prompt_template | self.chat_model | StrOutputParser()
        return RunnableWithMessageHistory(
            chat_chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )

    def get_session_history(self):
        """Obtiene el historial de chat desde MongoDB."""
        return MongoDBChatMessageHistory(
            session_id=self.session_id,
            connection_string=self.CNX_STRING,
            database_name="laive",
            collection_name="chat_history"
        )

    def invoke_answer(self, question: str):
        """Genera una respuesta a la consulta del usuario."""
        config = {"configurable": {"session_id": self.session_id}}
        return self.chain_with_history.invoke({"question": question}, config=config)

    def stream_answer(self, question: str):
        """Devuelve una respuesta en formato streaming."""
        config = {"configurable": {"session_id": self.session_id}}
        return self.chain_with_history.stream({"question": question}, config=config)
