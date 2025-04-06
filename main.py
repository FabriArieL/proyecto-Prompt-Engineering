import streamlit as st
import openai
import os
from dotenv import load_dotenv  # Importar dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configurar clave de API de OpenAI desde el .env
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    st.error("⚠️ No se encontró la clave de API de OpenAI. Verifica tu archivo .env.")

# Crear cliente de OpenAI
client = openai.OpenAI(api_key=api_key)

st.set_page_config(page_title="MindBloom - Apoyo emocional IA", page_icon="🌸")

# Estilos
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            background-color: #f5f5f5;
            border-radius: 12px;
            padding: 10px;
        }
        .chat-box {
            background-color: #e7f5ff;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌸 MindBloom - Apoyo emocional con IA")
st.markdown("Una app para reflexionar, desahogarte y recibir guía emocional con IA")

# Sección de "Cómo funciona"
with st.expander("🔍 ¿Cómo funciona MindBloom?"):
    st.markdown("""
    **MindBloom** está diseñado para ofrecerte un espacio seguro donde puedas expresarte y recibir orientación emocional. Aquí te explicamos cómo funciona:

    - ✍️ **Ingresá cómo te sentís** en el cuadro de texto.
    - 🤖 **MindBloom** analizará tu mensaje y responderá con empatía, comprensión y sugerencias útiles.
    - 💡 Podés usarlo para desahogarte, reflexionar o buscar afirmaciones positivas.
    - 🔐 Todo lo que compartas se mantiene de forma privada en tu sesión.

    ¡Sentite libre de usarlo tantas veces como lo necesites!
    """)

# Inicializar historial de conversación si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Actúa como un guía emocional amable, empático y comprensivo. Ayuda al usuario a reflexionar sobre su estado emocional y brindale contención, afirmaciones positivas y hábitos saludables si lo considerás útil."}
    ]

# Mostrar historial
def mostrar_historial():
    for msg in st.session_state.messages[1:]:
        role = "🤖 MindBloom" if msg["role"] == "assistant" else "🧠 Vos"
        st.markdown(f"<div class='chat-box'><strong>{role}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

mostrar_historial()

# Entrada del usuario
user_input = st.text_input("¿Cómo te sentís hoy o qué querés expresar?")

# Botón de acción para enviar mensaje
if st.button("Enviar a MindBloom"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Llamar al modelo de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Mostrar respuesta
        mostrar_historial()
    else:
        st.warning("Por favor, escribí algo antes de enviar.")
