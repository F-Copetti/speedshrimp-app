import streamlit as st
import tempfile
import cv2

#ESTA LINHA TEM QUE VIR PRIMEIRO
st.set_page_config(page_title="Fish Speed Analyzer", page_icon="🐟")
# Título e descrição
st.title("Fish Speed Analyzer 🐟")

st.markdown("""
    Envie um vídeo para calcular a velocidade média dos peixes.  
    [Ver meu currículo →](/profile)  # Link para a página Profile
""")

# Upload do vídeo
uploaded_file = st.file_uploader("Escolha um vídeo (MP4 ou AVI)...", type=["mp4", "avi"])

if uploaded_file:
    # Processamento (exemplo simplificado)
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    
    # Simulação de análise (substitua pelo seu código real)
    velocidade_media = 0.5  # Exemplo fictício
    st.success(f"Velocidade média detectada: {velocidade_media:.2f} m/s")
    
    # Mostrar um frame do vídeo
    cap = cv2.VideoCapture(tfile.name)
    ret, frame = cap.read()
    if ret:
        st.image(frame, channels="BGR", caption="Frame do vídeo")
