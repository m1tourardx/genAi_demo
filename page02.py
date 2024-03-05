import os
import streamlit as st
import base64
import os

dir_docs = os.path.join(os.getcwd(), 'docs')


def get_icon_path(file):
    # Retorna o caminho do ícone com base na extensão do arquivo
    if file.lower().endswith('.pdf'):
        path = os.path.join(os.getcwd(), 'imgs', 'pdf.png')
        return path
    elif file.lower().endswith('.docx'):
        path = os.path.join(os.getcwd(), 'imgs', 'docx.png')
        return path
    return None


def convert_image_to_base64(icon_path):
    # Converte a imagem do ícone para base64 para incorporar no HTML
    with open(icon_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def list_files_in_folder(folder_path, col):
    col.empty()  # Limpa a coluna para evitar duplicação de widgets
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(
        folder_path, f)) and (f.lower().endswith('.pdf') or f.lower().endswith('.docx'))]

    for idx, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        icon_path = get_icon_path(file)

        if icon_path:
            icon_base64 = convert_image_to_base64(icon_path)
            icon_html = f'<img src="data:image/png;base64,{icon_base64}" width="20" style="vertical-align:middle; margin-right:5px;">'
        else:
            icon_html = ''

        with open(file_path, "rb") as f:
            file_data = f.read()
            b64 = base64.b64encode(file_data).decode()
            href = f'<a href="data:file/octet-stream;base64,{b64}" download="{file}" style="text-decoration:none; color:inherit;">{icon_html}<span style="vertical-align:middle;">{file}</span></a>'
            col.markdown(href, unsafe_allow_html=True)


def second_page():
    folder_path = dir_docs
    col1, col2 = st.columns(2)

    with col1:
        st.write("Information known by the model:")
        list_files_in_folder(folder_path, col1)

    with col2:
        st.write(
            "Here you can add new information to the database known by the model:")
        uploaded_file = st.file_uploader(
            "Choose a new file:", key="file_uploader")

        if uploaded_file is not None:
            file_path = os.path.join(folder_path, uploaded_file.name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")

        if st.button("Train Model"):
            st.write("Training model...")
            st.success("Model trained successfully!")
