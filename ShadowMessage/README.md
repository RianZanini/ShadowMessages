# ShadowMessages

Projeto educacional em Python que demonstra esteganografia LSB em imagens PNG. O programa pode ocultar uma mensagem de texto ou os bytes de um arquivo dentro de uma imagem e depois recuperar o conteúdo com o decodificador.

## Funcionalidades

- Oculta texto digitado em UTF-8.
- Oculta arquivos de qualquer tipo, inclusive arquivos binários e arquivos com bytes nulos.
- Salva uma nova imagem PNG sem sobrescrever a imagem portadora original.
- Identifica o tipo e o tamanho do conteúdo por meio de um cabeçalho com assinatura e versão.
- Ao decodificar, exibe o texto ou informa o nome do arquivo e salva o arquivo extraído na pasta da imagem.
- Evita sobrescrever arquivos já existentes durante a extração, acrescentando `_extraido_N` ao nome.
- Informa quando os dados não cabem na capacidade disponível da imagem.

## Requisitos

- Python 3.10 ou superior.
- Pillow.
- Uma imagem portadora no formato PNG.

Instale a dependência:

```bash
python -m pip install Pillow
```

## Ocultar texto ou arquivo

Na pasta `ShadowMessage`, execute:

```bash
python ShadowMessages.py
```

Informe o caminho de uma imagem PNG e escolha uma opção:

```text
1 - Esconder texto digitado
2 - Esconder qualquer arquivo
```

Para a opção 2, informe o caminho do arquivo. O programa lê o arquivo em modo binário, preservando seu conteúdo original e seu nome. O resultado é gravado como `<nome_da_imagem>_oculto.png` no mesmo diretório da imagem selecionada. A imagem original não é alterada.

## Decodificar

Execute:

```bash
python ShadowMessagesDecod.py
```

Informe o caminho da imagem PNG produzida pelo codificador. Se o conteúdo for texto, ele será exibido no terminal. Se for um arquivo, o decodificador mostrará seu nome e o salvará na pasta da imagem. Caso já exista um arquivo com esse nome, será criado um nome alternativo, por exemplo `relatorio_extraido_1.txt`.

## Como funciona

O codificador converte os dados em bytes e grava cada bit no bit menos significativo (LSB) dos canais RGB dos pixels. O cabeçalho armazenado antes do conteúdo inclui uma assinatura, a versão do formato, o tipo (texto ou arquivo), o tamanho do nome e o tamanho do conteúdo. Os tamanhos permitem recuperar arquivos binários sem depender de um terminador que poderia aparecer dentro dos próprios dados.

A capacidade teórica de uma imagem RGB é de três bits por pixel, ou `largura × altura × 3 ÷ 8` bytes, antes de descontar o cabeçalho e o nome do arquivo. A capacidade prática depende, portanto, das dimensões da imagem e do tamanho dos metadados.

## Compatibilidade e limitações

- O decodificador atual reconhece imagens gravadas com o formato versionado usado pelo codificador atual. Imagens criadas por versões anteriores, que usavam um terminador de texto, não têm esse cabeçalho e não são decodificadas por esta versão.
- A conversão para JPEG, redimensionamento, edição ou qualquer processamento que altere os pixels pode corromper ou remover os dados. Mantenha e transmita o PNG original. Aplicativos de mensagens podem recomprimir fotos; se preservar os dados for importante, envie o PNG como documento/arquivo e confira o resultado depois de baixá-lo.
- Esteganografia LSB não criptografa o conteúdo nem impede sua detecção. Não use para armazenar informações confidenciais sem criptografia independente.
- O decodificador salva o arquivo extraído, mas não executa arquivos extraídos.

## Arquivos do projeto

| Arquivo | Finalidade |
|---|---|
| `ShadowMessages.py` | Codifica texto ou arquivos em uma imagem PNG. |
| `ShadowMessagesDecod.py` | Decodifica texto ou extrai arquivos de uma imagem PNG. |
| `requirements.txt` | Dependências Python do projeto. |

## Uso responsável

Este projeto destina-se ao aprendizado de processamento de imagens, representação binária e esteganografia. Só compartilhe arquivos com o conhecimento e consentimento de quem os receberá.
