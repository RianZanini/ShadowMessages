
from PIL import Image
import os


def extrair_mensagem(caminho_imagem):
    imagem = Image.open(caminho_imagem).convert("RGB")
    bits = []

    for pixel in imagem.getdata():
        for canal in pixel:
            bits.append(str(canal & 1))

    binario = ''.join(bits)
    bytes_mensagem = bytearray()

    for i in range(0, len(binario) - 7, 8):
        byte = binario[i:i + 8]
        valor = int(byte, 2)

        bytes_mensagem.append(valor)

        if len(bytes_mensagem) >= 2 and bytes_mensagem[-2:] == b'\x00\x00':
            bytes_mensagem = bytes_mensagem[:-2]
            break

    try:
        mensagem = bytes_mensagem.decode("utf-8")
        return mensagem
    except UnicodeDecodeError:
        return "Erro: nao foi possivel decodificar a mensagem como UTF-8."


def main():
    print("=== SHADOW MESSAGES DECODER ===")

    caminho = input("Caminho da imagem PNG: ").strip().strip('"')

    if not os.path.isfile(caminho):
        print("Erro: imagem nao encontrada.")
        return

    try:
        with Image.open(caminho) as imagem:
            if imagem.format != "PNG":
                print("Erro: o arquivo precisa estar no formato PNG.")
                return

        mensagem = extrair_mensagem(caminho)

        print("\n=== MENSAGEM EXTRAIDA ===")
        print(mensagem)

    except Exception as erro:
        print("Erro ao decodificar a imagem:", erro)


if __name__ == "__main__":
    main()
