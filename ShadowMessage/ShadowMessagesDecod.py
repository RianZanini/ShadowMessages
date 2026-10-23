from PIL import Image
import os
import struct


MAGIC = b"SHADOWMSG"
HEADER = struct.Struct(">9sBBHQ")


def _ler_bytes(imagem, quantidade):
    resultado = bytearray()
    valor = 0
    bits_no_byte = 0
    for pixel in imagem.getdata():
        for canal in pixel:
            valor = (valor << 1) | (canal & 1)
            bits_no_byte += 1
            if bits_no_byte == 8:
                resultado.append(valor)
                if len(resultado) == quantidade:
                    return bytes(resultado)
                valor = 0
                bits_no_byte = 0
    raise ValueError("A imagem não contém dados suficientes ou está corrompida.")


def extrair_dados(caminho_imagem):
    with Image.open(caminho_imagem) as original:
        imagem = original.convert("RGB")
    cabecalho = _ler_bytes(imagem, HEADER.size)
    assinatura, versao, tipo, tamanho_nome, tamanho_dados = HEADER.unpack(cabecalho)
    if assinatura != MAGIC:
        raise ValueError("Nenhum conteúdo ShadowMessages compatível foi encontrado.")
    if versao != 1:
        raise ValueError(f"Versão do formato não suportada: {versao}.")
    if tipo not in (0, 1):
        raise ValueError("Tipo de conteúdo desconhecido.")

    metadados = _ler_bytes(imagem, HEADER.size + tamanho_nome)
    nome = metadados[HEADER.size:].decode("utf-8")
    tamanho_total = HEADER.size + tamanho_nome + tamanho_dados
    if tamanho_total * 8 > imagem.width * imagem.height * 3:
        raise ValueError("O tamanho informado excede a capacidade da imagem.")
    conteudo = _ler_bytes(imagem, tamanho_total)[HEADER.size + tamanho_nome:]
    return tipo, nome, conteudo


def extrair_mensagem(caminho_imagem):
    """Compatibilidade para chamadas antigas que esperam apenas uma string."""
    tipo, _, conteudo = extrair_dados(caminho_imagem)
    if tipo != 0:
        raise ValueError("O conteúdo oculto é um arquivo, não uma mensagem de texto.")
    return conteudo.decode("utf-8")


def main():
    print("=== SHADOW MESSAGES DECODER ===")
    caminho = input("Caminho da imagem PNG: ").strip().strip('"')
    if not os.path.isfile(caminho):
        print("Erro: imagem não encontrada.")
        return
    try:
        with Image.open(caminho) as imagem:
            if imagem.format != "PNG":
                print("Erro: o arquivo precisa estar no formato PNG.")
        tipo, nome, conteudo = extrair_dados(caminho)
        if tipo == 0:
            print("\n=== MENSAGEM EXTRAÍDA ===")
            print(conteudo.decode("utf-8"))
        else:
            nome_seguro = os.path.basename(nome) or "arquivo_extraido"
            pasta = os.path.dirname(os.path.abspath(caminho))
            caminho_saida = os.path.join(pasta, nome_seguro)
            # Avoid overwriting an existing file during extraction.
            base, extensao = os.path.splitext(caminho_saida)
            contador = 1
            while os.path.exists(caminho_saida):
                caminho_saida = f"{base}_extraido_{contador}{extensao}"
                contador += 1
            with open(caminho_saida, "wb") as arquivo:
                arquivo.write(conteudo)
            print("\n=== ARQUIVO EXTRAÍDO ===")
            print("Nome do arquivo:", nome_seguro)
            print("Salvo em:", caminho_saida)
    except UnicodeDecodeError:
        print("Erro: o texto oculto não está em UTF-8 válido.")
    except Exception as erro:
        print("Erro ao decodificar a imagem:", erro)


if __name__ == "__main__":
    main()
