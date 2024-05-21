from PIL import Image
import uuid
import numpy as np
import base64
from io import BytesIO

def imagem_para_binario(imagem):
    # Converte a imagem em bytes
    img_bytes = imagem.tobytes()
    # Converte os bytes em uma string binária
    binario_string = ''.join(format(byte, '08b') for byte in img_bytes)
    return binario_string

def adicionar_uuid(binario_string):
    # Gera um UUID
    novo_uuid = uuid.uuid4()
    # Converte o UUID em binário
    uuid_binario = ''.join(format(byte, '08b') for byte in novo_uuid.bytes)
    # Adiciona o UUID binário ao final da string binária da imagem
    binario_com_uuid = binario_string + uuid_binario
    return binario_com_uuid, novo_uuid

def binario_para_imagem(binario_string, tamanho_imagem, modo_imagem):
    # Calcula o número de bytes na string binária da imagem original (sem o UUID)
    num_bytes_imagem = tamanho_imagem[0] * tamanho_imagem[1] * len(modo_imagem)
    binario_imagem = binario_string[:num_bytes_imagem * 8]

    # Converte a string binária em bytes
    byte_data = int(binario_imagem, 2).to_bytes(len(binario_imagem) // 8, byteorder='big')

    # Converte os bytes em um array NumPy
    img_array = np.frombuffer(byte_data, dtype=np.uint8)

    # Redimensiona o array para corresponder ao tamanho da imagem original
    if modo_imagem == 'RGB':
        img_array = img_array.reshape((tamanho_imagem[1], tamanho_imagem[0], 3))
    else:
        img_array = img_array.reshape((tamanho_imagem[1], tamanho_imagem[0]))

    # Cria uma imagem a partir do array NumPy
    img = Image.fromarray(img_array, mode=modo_imagem)
    return img

def process_image(imagem):
    # Converte a imagem para uma string binária
    binario_string = imagem_para_binario(imagem)
    # Adiciona o UUID ao final da string binária
    binario_com_uuid, novo_uuid = adicionar_uuid(binario_string)
    # Converte de volta para uma imagem
    imagem_processada = binario_para_imagem(binario_com_uuid, imagem.size, imagem.mode)

    # Converte a imagem original e a imagem processada para Base64
    buffered = BytesIO()
    imagem.save(buffered, format=imagem.format)
    image_base64 = base64.b64encode(buffered.getvalue()).decode()

    buffered = BytesIO()
    imagem_processada.save(buffered, format=imagem.format)
    image_base64_with_uuid = base64.b64encode(buffered.getvalue()).decode()

    return imagem_processada, image_base64, image_base64_with_uuid
