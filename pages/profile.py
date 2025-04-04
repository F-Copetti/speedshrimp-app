import streamlit as st

st.set_page_config(page_title="profile", page_icon="👤")

st.title("Meu Currículo 👤")
st.write("---")

# Seção 1: Dados Pessoais
st.header("Informações Pessoais")
st.write("**Nome:** Fabrini Copetti")  
st.write("**Email:** [link](fabrini.copetti@unesp.br)fabrinicopetti@gmail.com / fabrinicopetti@outlook.com")

# Seção 2: Formação Acadêmica
st.header("Formação")
st.write("**Cursando Doutorado em Biodiversidade em Ambientes Costeiros** - Universidade Estadual Paulista (2023-   )")
st.write("**Graduação em Ciências do Mar** - Universidade Federal de São Paulo (2012-2014)")

# Seção 3: Habilidades
st.header("Habilidades")
st.markdown("""
- Visão Computacional (OpenCV, Python)  
- Aquicultura Sustentável  
- Análise de Dados  
""")

# Link de volta para a página principal
st.markdown("[Voltar para a análise →](/)")