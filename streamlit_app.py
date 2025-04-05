import streamlit as st
import os
import tempfile
import shutil
import time
import subprocess

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

    # Caminho para o repositório do YOLOv5
    yolov5_path = os.path.join(os.getcwd(), "yolov5")
    detect_script = os.path.join(yolov5_path, "detect.py")

    st.write(f"🔎 Caminho detect.py calculado: {detect_script}")
    st.write(f"📂 Conteúdo da pasta atual: {os.listdir(os.getcwd())}")
    st.write(f"📂 Conteúdo da pasta yolov5: {os.listdir(os.path.join(os.getcwd(), 'yolov5'))}")


    if not os.path.exists(detect_script):
        st.error("❌ Script detect.py não encontrado! Verifique se o YOLOv5 foi clonado corretamente.")
    else:
        # Barra de progresso
        st.info("🚀 Iniciando a detecção...")
        progress_bar = st.progress(0)
        
        # Simular carregamento
        for percent_complete in range(0, 40, 5):
            time.sleep(0.1)
            progress_bar.progress(percent_complete)

        # Definir o diretório de resultados
        results_dir = os.path.join(temp_dir, "results")
        
        # Construir o comando para rodar detect.py
        command = [
            "python", detect_script,
            "--weights", "models/best.pt",
            "--source", video_path,
            "--imgsz", "416",
            "--conf-thres", "0.25",
            "--save-txt",
            "--save-conf",
            "--project", temp_dir,
            "--name", "results",
            "--exist-ok"
        ]
        
        try:
            subprocess.run(command, check=True)
            st.success("🎯 Detecção concluída!")
        except subprocess.CalledProcessError as e:
            st.error(f"Erro durante detecção: {e}")
        
        progress_bar.progress(100)

        # Procurar vídeo detectado
        result_folder = os.path.join(temp_dir, 'results')
        processed_files = os.listdir(result_folder)
        processed_videos = [f for f in processed_files if f.endswith(('.mp4', '.avi', '.mov'))]

        if processed_videos:
            result_video_path = os.path.join(result_folder, processed_videos[0])
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

    # Limpeza temporária (opcional)
    shutil.rmtree(temp_dir)
