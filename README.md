# AI-RAG-Assistant
brindar respuestas instantáneas y precisas a las consultas de los clientes, además de ofrecer recomendaciones personalizadas sobre productos o servicios.

### Paso 1:
Instalar entorno virtual
python -m venv .venv  

### Paso 2:
Activar virtual
.\.venv\Scripts\activate  

### Paso 3:
Instalar paquetes
pip install -r .\requirements.txt

### Paso 4:
Crear archivo ./.streamlit/secrets.toml
Poner API KEYs: 
- OPENAI_API_KEY="abc"

### Paso 5:
Ejecutar app
streamlit run main.py