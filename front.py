import streamlit as st
import pyperclip
import main as la
from io import BytesIO
import base64
from PIL import Image

st.title('Processador de Imagens')
st.caption('by Jarvis')



def load_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None


uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.session_state['uploaded_image'] = load_image(uploaded_file)

if 'uploaded_image' in st.session_state:
    image = st.session_state['uploaded_image']

    if image:
        st.image(image, caption='Imagem Original', use_column_width=True)

        if 'processed_image' not in st.session_state:
            processed_image, image_base64, image_base64_with_uuid = la.process_image(image)
            st.session_state['processed_image'] = processed_image
            st.session_state['image_base64'] = image_base64
            st.session_state['image_base64_with_uuid'] = image_base64_with_uuid
        else:
            processed_image = st.session_state['processed_image']
            image_base64 = st.session_state['image_base64']
            image_base64_with_uuid = st.session_state['image_base64_with_uuid']

        st.text_area("Base64 Original", value=str(image_base64), height=100)
        st.image(processed_image, caption='Imagem Processada', use_column_width=True)
        st.text_area("Base64 Alterado", value=str(image_base64_with_uuid), height=100)

        buffered = BytesIO()
        processed_image.save(buffered, format=image.format)
        buffered.seek(0)
        b64 = base64.b64encode(buffered.read()).decode()
        download_button_label = f'Baixar Imagem Processada ({image.format})'
        st.download_button(
            label=download_button_label,
            data=buffered,
            file_name=f'processed_image.{image.format.lower()}',
            mime=f'image/{image.format.lower()}'
        )

        if st.button('Recarregar'):
            processed_image, image_base64, image_base64_with_uuid = la.process_image(image)
            st.session_state['processed_image'] = processed_image
            st.session_state['image_base64'] = image_base64
            st.session_state['image_base64_with_uuid'] = image_base64_with_uuid
            st.rerun(),
