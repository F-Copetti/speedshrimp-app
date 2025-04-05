import streamlit as st
import torch
import os
import tempfile
import shutil
import time
import sys

# Adicionar o diretório do YOLOv5 ao path para importar o detect.py corretamente
if 'yolov5' not in sys.path:
    sys.path.append('yolov5')

from yolov5 import detect  # Agora importa detect corretamente

# Configuração inicial
st.set_page_config(page_title="Fish Speed Analyzer", page_icon="🐟")
st.title("Fish Speed Analyzer 🐟")
st.markdown("""
Envie um vídeo para calcular a velocidade média dos peixes.  
[Ver meu currículo →](/profile)
""")

# Upload do vídeo
uploaded_file = st.file_uploader("📂 Faça upload de um vídeo", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Salvar o vídeo temporariamente
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("✅ Vídeo enviado com sucesso!")

    # Barra de progresso
    st.info("🚀 Iniciando a detecção de camarões no vídeo...")
    progress_bar = st.progress(0)
    for percent_complete in range(0, 40, 5):
        time.sleep(0.1)
        progress_bar.progress(percent_complete)

    # Caminho para o modelo
    model_path = 'models/best.pt'  # Seu modelo customizado

    # Configurar argumentos para o detect.py
    opt = detect.parse_opt()
    opt.weights = model_path
    opt.source = video_path
    opt.imgsz = 416
    opt.conf_thres = 0.25
    opt.save_txt = True
    opt.save_conf = True
    opt.project = temp_dir
    opt.name = 'results'
    opt.exist_ok = True
    opt.save_crop = False  # (opcional) salva somente detecções cortadas

    # Executar a detecção
    detect.main(opt)

    # Atualizar barra de progresso
    progress_bar.progress(100)
    st.success("🎯 Detecção concluída!")

    # Localizar o vídeo processado
    result_folder = os.path.join(temp_dir, 'results')
    processed_files = os.listdir(result_folder)
    processed_videos = [f for f in processed_files if f.endswith(('.mp4', '.avi', '.mov'))]

    if processed_videos:
        result_video_path = os.path.join(result_folder, processed_videos[0])
        st.video(result_video_path)

        # Botão para download do vídeo
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

    # Limpeza automática da pasta temporária
    shutil.rmtree(temp_dir)