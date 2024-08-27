import streamlit as st
import requests
import json

# Configuración de las API keys
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# Función para obtener sugerencias de carrera usando la API de Together
def get_career_suggestions(user_responses):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""Basándote en la siguiente información sobre un estudiante, sugiere tres carreras que podrían ser adecuadas para él/ella y explica brevemente por qué:

{user_responses}

Proporciona tu respuesta en el siguiente formato:
1. [Nombre de la carrera]: [Breve explicación]
2. [Nombre de la carrera]: [Breve explicación]
3. [Nombre de la carrera]: [Breve explicación]"""

    data = {
        "model": "togethercomputer/llama-2-70b-chat",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()["output"]["choices"][0]["text"]

# Función para obtener información adicional sobre las carreras sugeridas usando la API de Serper
def get_career_info(career):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": f"{career} carrera información",
        "num": 3
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()["organic"][:3]

# Configuración de la aplicación Streamlit
st.title("Sugerencia de Carreras")
st.write("Selecciona las opciones que mejor te describan para obtener sugerencias de carreras.")

# Preguntas y opciones para el usuario
questions_and_options = {
    "¿En qué rango de edad te encuentras?": ["15-18", "19-22", "23-26", "27 o más"],
    "¿Cuáles son tus materias favoritas en la escuela?": ["Matemáticas", "Ciencias", "Literatura", "Historia", "Arte", "Educación Física"],
    "¿Cuáles son tus principales intereses?": ["Tecnología", "Naturaleza", "Arte y Cultura", "Negocios", "Ayudar a otros", "Deportes"],
    "¿Cómo describirías tu personalidad?": ["Extrovertido", "Introvertido", "Analítico", "Creativo", "Líder", "Colaborador"],
    "¿Cuáles consideras que son tus habilidades más fuertes?": ["Resolución de problemas", "Comunicación", "Creatividad", "Organización", "Trabajo en equipo", "Habilidades técnicas"],
    "¿Qué tipo de ambiente de trabajo prefieres?": ["Oficina tradicional", "Trabajo remoto", "Ambiente al aire libre", "Laboratorio", "Ambiente creativo", "Variado/Dinámico"],
    "¿Cuáles son tus expectativas salariales?": ["Menos de $30,000 al año", "$30,000 - $50,000 al año", "$50,000 - $80,000 al año", "Más de $80,000 al año"],
    "¿Prefieres trabajar en equipo o de forma independiente?": ["Principalmente en equipo", "Principalmente de forma independiente", "Una mezcla de ambos"],
    "¿Qué impacto te gustaría tener en el mundo a través de tu carrera?": ["Avance tecnológico", "Cuidado del medio ambiente", "Mejora de la salud", "Educación", "Justicia social", "Innovación empresarial"]
}

user_responses = {}
for question, options in questions_and_options.items():
    user_responses[question] = st.selectbox(question, options)

if st.button("Obtener sugerencias de carrera"):
    with st.spinner("Analizando tus respuestas..."):
        # Formatear las respuestas del usuario
        formatted_responses = "\n".join([f"{q}: {a}" for q, a in user_responses.items()])
        
        # Obtener sugerencias de carrera
        suggestions = get_career_suggestions(formatted_responses)
        st.subheader("Sugerencias de Carrera:")
        st.write(suggestions)
        
        # Extraer los nombres de las carreras sugeridas
        career_names = [line.split(":")[0].strip()[3:] for line in suggestions.split("\n") if line.strip().startswith(("1.", "2.", "3."))]
        
        # Obtener información adicional sobre cada carrera sugerida
        st.subheader("Información Adicional:")
        for career in career_names:
            st.write(f"### {career}")
            career_info = get_career_info(career)
            for info in career_info:
                st.write(f"- [{info['title']}]({info['link']})")
                st.write(info['snippet'])
            st.write("---")

st.sidebar.write("Esta aplicación utiliza las APIs de Together y Serper para proporcionar sugerencias de carrera e información adicional.")
