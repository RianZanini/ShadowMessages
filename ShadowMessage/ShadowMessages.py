from PIL import Image
import os
import struct


MAGIC = b"SHADOWMSG"
VERSION = 1
# Signature (9 bytes), version (1), type (1), filename length (2), payload size (8).
HEADER = struct.Struct(">9sBBHQ")


def _para_bits(dados):
    return ''.join(f'{byte:08b}' for byte in dados)


def esconder_dados(caminho_imagem, dados, tipo, nome_arquivo=""):
    with Image.open(caminho_imagem) as original:
        imagem = original.convert("RGB")
    pixels = list(imagem.getdata())

    nome_bytes = nome_arquivo.encode("utf-8")
    if len(nome_bytes) > 65535:
        raise ValueError("O nome do arquivo é grande demais.")
    cabecalho = HEADER.pack(MAGIC, VERSION, tipo, len(nome_bytes), len(dados))
    conteudo = cabecalho + nome_bytes + dados
    bits = _para_bits(conteudo)
    capacidade = len(pixels) * 3
    if len(bits) > capacidade:
        raise ValueError(
            f"Dados grandes demais para esta imagem. Necessário: {len(conteudo)} bytes; "
            f"capacidade: {capacidade // 8} bytes."
        )

    novos_pixels = []
    indice = 0
    for pixel in pixels:
        canais = []
        for canal in pixel:
            if indice < len(bits):
                canal = (canal & 0xFE) | int(bits[indice])
                indice += 1
            canais.append(canal)
        novos_pixels.append(tuple(canais))

    imagem_nova = Image.new("RGB", imagem.size)
    imagem_nova.putdata(novos_pixels)
    pasta = os.path.dirname(os.path.abspath(caminho_imagem))
    nome = os.path.splitext(os.path.basename(caminho_imagem))[0]
    caminho_saida = os.path.join(pasta, nome + "_oculto.png")
    imagem_nova.save(caminho_saida, format="PNG")
    print("\nDados ocultos com sucesso!")
    print("Imagem salva em:", caminho_saida)


def main():
    print("=== ESTEGANOGRAFIA EM PNG ===")
    caminho_imagem = input("Caminho da imagem PNG: ").strip().strip('"')
    if not os.path.isfile(caminho_imagem):
        print("Erro: imagem não encontrada.")
        return
    try:
        with Image.open(caminho_imagem) as imagem:
            if imagem.format != "PNG":
                print("Erro: o arquivo precisa estar no formato PNG.")
                return
    except Exception:
        print("Erro ao abrir a imagem.")
        return

    print("\nEscolha como deseja esconder os dados:")
    print("1 - Esconder texto digitado")
    print("2 - Esconder qualquer arquivo")
    opcao = input("Opção: ").strip()
    try:
        if opcao == "1":
            mensagem = input("\nDigite a mensagem: ")
            esconder_dados(caminho_imagem, mensagem.encode("utf-8"), 0)
        elif opcao == "2":
            caminho_arquivo = input("Caminho do arquivo: ").strip().strip('"')
            if not os.path.isfile(caminho_arquivo):
                print("Erro: arquivo não encontrado.")
                return
            with open(caminho_arquivo, "rb") as arquivo:
                dados = arquivo.read()
            esconder_dados(caminho_imagem, dados, 1, os.path.basename(caminho_arquivo))
        else:
            print("Opção inválida.")
    except ValueError as erro:
        print("Erro:", erro)
    except Exception as erro:
        print("Falha ao realizar a esteganografia:", erro)


if __name__ == "__main__":
    main()
