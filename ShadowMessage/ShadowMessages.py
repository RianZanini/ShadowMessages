
from PIL import Image
import os


def texto_para_binario(texto):
    return ''.join(format(byte, '08b') for byte in texto.encode('utf-8'))


def esconder_mensagem(caminho_imagem, mensagem):
    imagem = Image.open(caminho_imagem).convert("RGB")
    pixels = list(imagem.getdata())

    dados = texto_para_binario(mensagem) + '0000000000000000'
    capacidade = len(pixels) * 3

    if len(dados) > capacidade:
        raise ValueError("A mensagem e grande demais para esta imagem.")

    novos_pixels = []
    indice = 0

    for pixel in pixels:
        novo_pixel = []

        for canal in pixel:
            if indice < len(dados):
                canal = (canal & 254) | int(dados[indice])
                indice += 1

            novo_pixel.append(canal)

        novos_pixels.append(tuple(novo_pixel))

    imagem_nova = Image.new("RGB", imagem.size)
    imagem_nova.putdata(novos_pixels)

    pasta = os.path.dirname(os.path.abspath(caminho_imagem))
    nome = os.path.splitext(os.path.basename(caminho_imagem))[0]
    caminho_saida = os.path.join(pasta, nome + "_esteganografia.png")

    imagem_nova.save(caminho_saida, format="PNG")

    print("\nMensagem escondida com sucesso!")
    print("Imagem salva em:", caminho_saida)


def main():
    print("=== ESTEGANOGRAFIA EM PNG ===")

    caminho_imagem = input("Caminho da imagem PNG: ").strip().strip('"')

    if not os.path.isfile(caminho_imagem):
        print("Erro: imagem nao encontrada.")
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
    print("2 - Esconder arquivo TXT")

    opcao = input("Opcao: ").strip()

    try:
        if opcao == "1":
            mensagem = input("\nDigite a mensagem: ")

        elif opcao == "2":
            caminho_txt = input("Caminho do arquivo TXT: ").strip().strip('"')

            if not os.path.isfile(caminho_txt):
                print("Erro: arquivo TXT nao encontrado.")
                return

            if not caminho_txt.lower().endswith(".txt"):
                print("Erro: selecione um arquivo com extensao .txt.")
                return

            with open(caminho_txt, "r", encoding="utf-8-sig") as arquivo:
                mensagem = arquivo.read()

        else:
            print("Opcao invalida.")
            return

        esconder_mensagem(caminho_imagem, mensagem)

    except UnicodeDecodeError:
        print("Erro: o arquivo TXT nao esta em uma codificacao de texto compativel.")
    except ValueError as erro:
        print("Erro:", erro)
    except Exception as erro:
        print("Falha ao realizar a esteganografia:", erro)


if __name__ == "__main__":
    main()
