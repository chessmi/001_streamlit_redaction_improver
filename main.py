import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI

# Plantilla de instrucciones
plantilla = """
    A continuación, se proporciona un borrador de texto que puede estar mal redactado.
    Tu objetivo es:
    - Redactar correctamente el texto.
    - Convertir el texto a un tono específico.
    - Convertir el texto a un dialecto específico.

    Aquí hay algunos ejemplos de diferentes tonos:
    - Formal: ¡Saludos! OpenAI ha anunciado que Sam Altman vuelve a la empresa como su Director Ejecutivo. Tras cinco días de conversaciones y deliberaciones, se ha decidido reincorporar a Altman, quien había sido previamente despedido. Estamos encantados de dar la bienvenida a Sam nuevamente a OpenAI.
    - Informal: ¡Hola a todos! Ha sido una semana intensa, pero tenemos noticias emocionantes: Sam Altman está de vuelta en OpenAI como CEO. Después de muchas conversaciones y debates, Altman regresa a la startup de IA que cofundó.

    Aquí hay algunos ejemplos de palabras en diferentes dialectos:
    - Español de España: coche, móvil, ordenador, patatas fritas, ascensor.
    - Español de Latinoamérica: carro, celular, computadora, papas fritas, elevador.

    Ejemplo de frases en cada dialecto:
    - Español de España: OpenAI ha anunciado hoy que Sam Altman regresará como Director Ejecutivo tras varios días de deliberación.
    - Español de Latinoamérica: OpenAI anunció hoy que Sam Altman volverá como Director Ejecutivo tras varios días de discusión.

    Por favor, comienza la redacción con una introducción cálida si es necesario.

    A continuación, el texto de borrador, tono y dialecto:
    BORRADOR: {borrador}
    TONO: {tono}
    DIALECTO: {dialecto}

    TU RESPUESTA EN {dialecto}:
"""

# Definir la plantilla de prompt
prompt = PromptTemplate(
    input_variables=["tono", "dialecto", "borrador"],
    template=plantilla,
)

# Función para cargar el modelo de OpenAI
def cargar_LLM(openai_api_key):
    """Carga el modelo de lenguaje de OpenAI usando la clave proporcionada."""
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    return llm

# Configuración de la página de Streamlit
st.set_page_config(page_title="Mejora tu Texto")
st.header("Mejora tu Texto con IA")

# Instrucciones
col1, col2 = st.columns(2)

with col1:
    st.markdown("Reescribe tu texto en diferentes estilos.")

with col2:
    st.write("Contacta con [AI Accelera](https://aiaccelera.com) para desarrollar tus proyectos de IA.")

# Entrada de la clave de OpenAI
st.markdown("## Introduce tu clave de OpenAI")

def obtener_openai_api_key():
    return st.text_input(label="Clave de OpenAI", placeholder="Ej: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")

openai_api_key = obtener_openai_api_key()

# Entrada del texto a mejorar
st.markdown("## Introduce el texto que deseas mejorar")

def obtener_borrador():
    return st.text_area(label="Texto", placeholder="Escribe aquí...", key="borrador_input")

borrador_input = obtener_borrador()

if len(borrador_input.split(" ")) > 700:
    st.write("Por favor, introduce un texto más corto. El límite es de 700 palabras.")
    st.stop()

# Opciones de tono y dialecto
col1, col2 = st.columns(2)
with col1:
    tono_elegido = st.selectbox(
        '¿Qué tono quieres que tenga el texto?',
        ('Formal', 'Informal')
    )
    
with col2:
    dialecto_elegido = st.selectbox(
        '¿Qué dialecto del español prefieres?',
        ('Español de España', 'Español de Latinoamérica')
    )

# Salida del texto mejorado
st.markdown("### Tu texto mejorado:")

if borrador_input:
    if not openai_api_key:
        st.warning('Por favor, introduce tu clave de OpenAI. \
            Instrucciones [aquí](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = cargar_LLM(openai_api_key=openai_api_key)

    prompt_con_borrador = prompt.format(
        tono=tono_elegido, 
        dialecto=dialecto_elegido, 
        borrador=borrador_input
    )

    texto_mejorado = llm(prompt_con_borrador)

    st.write(texto_mejorado)
