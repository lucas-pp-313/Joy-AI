from groq import Groq
import streamlit as st

# CONFIG
def configInicial():
    st.set_page_config(
        page_title="JOY AI",
        page_icon="🤖",
        layout="centered"
    )

    # --- ESTILOS CSS ---
    st.markdown("""
    <style>

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    /* Evita cortes raros en textos */
    h1, h2, h3 {
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }

    /* Título principal */
    h1 {
        text-align: center;
        color: #ffffff;
        font-size: 3rem !important;
        font-weight: 800;
        margin-bottom: 0;
    }

    /* Subtítulo */
    .subtitulo {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        width: 320px !important;
        background-color: #111827;
        border-right: 1px solid #374151;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Caja mensajes usuario */
    .stChatMessage[data-testid="chat-message-user"] {
        background-color: #2563eb20;
        border: 1px solid #3b82f6;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
    }

    /* Caja mensajes IA */
    .stChatMessage[data-testid="chat-message-assistant"] {
        background-color: #ffffff10;
        border: 1px solid #374151;
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 10px;
    }

    /* Input */
    .stChatInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b;
        border-radius: 10px;
    }

    /* Botones */
    .stButton button {
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.03);
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
    }

    </style>
    """, unsafe_allow_html=True)


# --- API ---
api_key = st.secrets.get("CLAVE_API")

def obtener_cliente():
    if api_key:
        st.success("✅ Conexión con Groq exitosa")
        return Groq(api_key=api_key)
    else:
        st.error("❌ No se encontró la API Key de Groq")
        st.stop()


# --- MODELOS ---
modelos = {
    "Groq": "groq/compound",
    "Llama": "llama-3.1-8b-instant",
    "Groq mini": "groq/compound-mini",
}


# --- ESTADO ---
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {
                "role": "assistant",
                "content": "Hola, soy un asistente IA, ¿en qué te puedo ayudar?"
            }
        ]


# --- IA ---
def obtener_respuesta(cliente, modelo, mensajes):
    response = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes
    )

    return response.choices[0].message.content


# --- MAIN ---
def main():
    configInicial()

    # --- HEADER ---
    st.markdown(
        "<h1>🤖 JOY AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitulo'>Soy un asistente con inteligencia artificial para ayudarte</p>",
        unsafe_allow_html=True
    )

    cliente = obtener_cliente()

    inicializar_estado()

    # --- SIDEBAR ---
    with st.sidebar:

        st.markdown("""
        <h2 style='
            text-align: center;
            font-size: 32px;
            margin-bottom: 10px;
            color: white;
        '>
        ⚙️ Configuración
        </h2>
        """, unsafe_allow_html=True)

        st.markdown("---")

        modelo_nombre = st.selectbox(
            "Elegí el modelo:",
            list(modelos.keys())
        )

        modelo = modelos[modelo_nombre]

        st.markdown("---")

        st.info("💡 Elegí el modelo que quieras usar")

        st.caption("Hecho por Lucas 😎")

    # --- HISTORIAL ---
    for mensaje in st.session_state.mensajes:

        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])

    # --- INPUT USUARIO ---
    if prompt := st.chat_input("Escribí tu mensaje..."):

        # Guarda mensaje usuario
        st.session_state.mensajes.append({
            "role": "user",
            "content": prompt
        })

        # Mostrar mensaje usuario
        with st.chat_message("user"):
            st.write(prompt)

        # Respuesta IA
        with st.chat_message("assistant"):

            with st.spinner("Elaborando respuesta..."):

                resp = obtener_respuesta(
                    cliente,
                    modelo,
                    st.session_state.mensajes
                )

                st.write(resp)

        # Guardar respuesta IA
        st.session_state.mensajes.append({
            "role": "assistant",
            "content": resp
        })


# --- EJECUTAR APP ---
if __name__ == "__main__":
    main()