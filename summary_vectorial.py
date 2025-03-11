from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

def summaryVectorial(rephrase_prompt, llm, vector_store_page,question,  search_kwargs=None):
    """
    summaryVectrial crea un 'pipeline' (chain) al encadenar:
    rephrase_prompt | llm  | vector_store_page.as_retriever(search_kwargs=...)

    Parámetros
    ----------
    rephrase_prompt: objeto o función
        El rephrase_prompt que se desea usar.
    llm: objeto o función
        El modelo de lenguaje (Large Language Model) a encadenar.
    runnable_lambda: objeto o función
        La RunnableLambda (o cualquier callable) que procesa el contenido.
    vector_store_page: objeto
        El vector store o página que tenga el método 'as_retriever'.
    search_kwargs: dict, opcional
        Diccionario con parámetros para la búsqueda (por defecto {"k": 4}).
    question :question     

    Retorna
    -------
    chain : objeto
        La cadena resultante tras combinar todos los pasos.
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}

    chain = (
        rephrase_prompt
        | llm
        | RunnableLambda(lambda x: x.content)
        | vector_store_page.as_retriever(search_kwargs=search_kwargs)
    )    

    
    answer = generate_anwser(llm, rephrase_prompt,vector_store_page,question, )
    return answer

def combine_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def generate_anwser (llm, rephrase_prompt, vector_store_page,question):
    SYSTEM_PROMPT = """
        <PERSONA>
        Eres un especialista experto en quesos laive
        </PERSONA>

        <TAREA>
        Tu tarea es responder la pregunta del usuario.
        </TAREA>

        <RESTRICCIONES>
        - Solo responde la pregunta del usuario tomando como contexto lo provisto en <CONTEXTO>.
        </RESTRICCIONES>

        <CONTEXTO 1>
        {context}
        </CONTEXTO 1>


        """

    USER_PROMPT = """
        user question: {user_request}
        rephrased user question: {rephrased_request}
        """   
    qa_prompt = ChatPromptTemplate([
    ("ai", SYSTEM_PROMPT),
    ("user", USER_PROMPT)
    ])
    simple_chatbot = (
        {
            "user_request": itemgetter("user_request"),
            "rephrased_request": rephrase_prompt | llm | RunnableLambda(lambda x: x.content)
        } 
        | RunnablePassthrough() 
        | {
            "user_request": itemgetter("user_request"),
            "rephrased_request": itemgetter("rephrased_request"),
            "context": itemgetter("rephrased_request") 
                    | vector_store_page.as_retriever(search_kwargs={"k": 4})
                    | RunnableLambda(combine_documents),
        }
        | qa_prompt 
        | llm
        | RunnableLambda(lambda x: x.content)
    )

    return  simple_chatbot.invoke({"user_request": question})