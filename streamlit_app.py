import streamlit as st
import os
import sys
import tempfile
import shutil
import time

# Configuração inicial
st.set_page_config(page_title="Fish Speed Analyzer", page_icon="🐟")
st.title("Fish Speed Analyzer 🐟")
st.markdown("""
Envie um vídeo para calcular a velocidade média dos peixes.  
[Ver meu currículo →](/profile)
""")

# Ajustar caminho para importar yolov5
sys.path.append(os.path.join(os.getcwd(), "yolov5"))

# Importar função run do detect.py
try:
    from detect import run as yolo_detect
except ImportError:
    st.error("❌ Não foi possível importar o módulo 'detect.py'. Verifique se a pasta 'yolov5/' está no diretório principal.")
    st.stop()

# Validar se o modelo existe
if not os.path.exists("models/best.pt"):
    st.error("❌ Modelo 'models/best.pt' não encontrado! Faça o upload correto do seu modelo.")
    st.stop()

# Upload do vídeo
uploaded_file = st.file_uploader("📂 Faça upload de um vídeo", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Salvar o vídeo temporariamente
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("✅ Vídeo enviado com sucesso!")

    # Barra de progresso (para simular carregamento inicial)
    st.info("🚀 Preparando para detectar...")
    progress_bar = st.progress(0)
    
    for percent_complete in range(0, 40, 5):
        time.sleep(0.1)
        progress_bar.progress(percent_complete)

    # Definir pasta de resultados
    results_dir = os.path.join(temp_dir, "results")

    # Rodar detecção
    try:
        yolo_detect(
            weights="models/best.pt",
            source=video_path,
            imgsz=416,
            conf_thres=0.25,
            save_txt=True,
            save_conf=True,
            project=temp_dir,
            name="results",
            exist_ok=True
        )
        st.success("🎯 Detecção concluída!")
    except Exception as e:
        st.error(f"❌ Erro durante detecção: {e}")
        shutil.rmtree(temp_dir)
        st.stop()

    progress_bar.progress(100)

    # Procurar vídeo processado
    processed_videos = []
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                processed_videos.append(os.path.join(root, file))

    if processed_videos:
        result_video_path = processed_videos[0]
        st.video(result_video_path)

        # Botão para download
        with open(result_video_path, "rb") as file:
            video_bytes = file.read()
            st.download_button(
                label="📥 Baixar vídeo processado",
                data=video_bytes,
                file_name="video_detectado.mp4",
                mime="video/mp4"
            )
    else:
        st.warning("⚠️ Não foi possível localizar o vídeo processado.")

    # Limpar os arquivos temporários
    shutil.rmtree(temp_dir)
