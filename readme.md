# ShadowMessages

**ShadowMessages** é um projeto desenvolvido em Python para demonstrar a aplicação da esteganografia digital em imagens PNG. O sistema permite ocultar mensagens de texto dentro de imagens e recuperar posteriormente o conteúdo utilizando um decodificador próprio.

O projeto utiliza a técnica **LSB (Least Significant Bit)**, que modifica o bit menos significativo dos canais de cor dos pixels para armazenar informações sem provocar alterações visuais normalmente perceptíveis.

## Funcionalidades

- **Codificação de mensagens:** oculta textos digitados pelo usuário em imagens PNG.
- **Ocultação de arquivos TXT:** permite armazenar o conteúdo de arquivos de texto dentro de imagens.
- **Decodificação de mensagens:** recupera o texto oculto em imagens compatíveis.
- **Preservação da imagem original:** gera um novo arquivo PNG sem sobrescrever a imagem de entrada.
- **Verificação de capacidade:** permite calcular a capacidade teórica de armazenamento de uma imagem.
- **Interface via terminal:** interação simples por meio de entradas e saídas no console.

## Tecnologias utilizadas

- Python 3
- Pillow — processamento e manipulação de imagens
- Esteganografia digital
- Técnica LSB (Least Significant Bit)

## Estrutura do projeto

```text
ShadowMessages/
├── ShadowMessages.py
├── ShadowMessagesDecoder.py
├── README.md
└── requirements.txt
```

**Descrição dos arquivos:**

| Arquivo | Descrição |
|---|---|
| `ShadowMessages.py` | Programa responsável por ocultar mensagens em imagens PNG. |
| `ShadowMessagesDecoder.py` | Programa responsável por extrair mensagens de imagens compatíveis. |
| `README.md` | Documentação do projeto. |
| `requirements.txt` | Lista de dependências necessárias. | python -m pip install -r requirements.txt

## Requisitos

- Python 3.10 ou superior.
- Biblioteca Pillow.
- Uma imagem no formato PNG.

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/RianZanini/ShadowMessages.git
```

### 2. Acesse a pasta do projeto

```bash
cd ShadowMessages
```

### 3. Instale as dependências

Crie o arquivo `requirements.txt` com o seguinte conteúdo:

```text
Pillow
```

Em seguida, execute:

```bash
python -m pip install -r requirements.txt
```

## Como utilizar

### 1. Ocultar uma mensagem

Execute o programa de codificação:

```bash
python ShadowMessages.py
```

Informe o caminho da imagem PNG que será utilizada como portadora.

O programa apresentará as seguintes opções:

```text
=== ESTEGANOGRAFIA EM PNG ===

Caminho da imagem PNG: imagem.png

Escolha como deseja esconder os dados:
1 - Esconder texto digitado
2 - Esconder arquivo TXT

Opcao:
```

Escolha a opção desejada:

- **Opção 1:** digite a mensagem que deseja ocultar.
- **Opção 2:** informe o caminho de um arquivo TXT cujo conteúdo será armazenado.

Após a codificação, será gerada uma nova imagem no mesmo diretório da imagem original.

Exemplo:

```text
imagem.png
imagem_esteganografia.png
```

A imagem original permanece intacta.

### 2. Extrair uma mensagem

Execute o decodificador:

```bash
python ShadowMessagesDecoder.py
```

Informe o caminho da imagem que contém a mensagem.

Exemplo:

```text
=== SHADOW MESSAGES DECODER ===

Caminho da imagem PNG: imagem_esteganografia.png

=== MENSAGEM EXTRAIDA ===
Esta e uma mensagem de teste.
```

O decodificador recupera o texto armazenado na imagem, desde que ela seja compatível com o método de codificação utilizado.

## Como funciona a técnica LSB?

A técnica LSB utiliza o bit menos significativo de cada canal de cor de um pixel para armazenar dados.

Em uma imagem RGB, cada pixel possui três canais:

- **R:** vermelho.
- **G:** verde.
- **B:** azul.

Cada canal possui um valor entre 0 e 255, representado por 8 bits.

Por exemplo, para armazenar o bit `1` em um canal cujo valor original é `180`:

```text
Valor original: 180
Binário:        10110100

Bit armazenado: 1

Novo valor:     181
Binário:        10110101
```

A alteração é de apenas uma unidade no valor do canal de cor. Quando aplicada aos pixels de uma imagem, essa técnica geralmente não produz diferenças visuais perceptíveis.

### Processo de codificação

1. A mensagem é convertida em uma sequência de bytes.
2. Os bytes são representados em formato binário.
3. Os bits são inseridos nos bits menos significativos dos canais RGB.
4. A imagem modificada é salva no formato PNG.

### Processo de decodificação

1. O programa abre a imagem PNG.
2. Percorre os canais RGB na mesma ordem utilizada durante a codificação.
3. Recupera os bits menos significativos.
4. Reconstrói os bytes da mensagem.
5. Identifica o marcador de término e converte os bytes recuperados para texto UTF-8.

## Capacidade de armazenamento

A capacidade teórica de uma imagem RGB, utilizando um bit de cada canal, pode ser calculada pela fórmula:

\[
C = \frac{L \times A \times 3}{8}
\]

Onde:

- \(C\) representa a capacidade em bytes.
- \(L\) representa a largura em pixels.
- \(A\) representa a altura em pixels.
- O fator 3 corresponde aos três canais RGB.

Exemplos aproximados:

| Resolução | Capacidade teórica |
|---|---:|
| 640 × 480 | 112,5 KiB |
| 1280 × 720 | 337,5 KiB |
| 1920 × 1080 | 759,4 KiB |
| 3840 × 2160 | 2,97 MiB |

A capacidade efetiva é ligeiramente menor devido aos dados de controle utilizados pelo programa.

A capacidade depende da resolução da imagem, não do tamanho do arquivo PNG original em disco.

## Limitações

- O codificador e o decodificador precisam utilizar a mesma ordem de canais, técnica de inserção e convenção de término.
- A implementação atual trabalha com mensagens de texto e conteúdo de arquivos TXT.
- A capacidade disponível é limitada pela quantidade de pixels da imagem.
- A conversão para JPEG, o redimensionamento ou outras transformações podem destruir os dados ocultos.
- O decodificador apresentado depende de um marcador de término e pode interpretar incorretamente imagens que não tenham sido geradas pelo codificador correspondente.
- O método LSB não oferece criptografia nem garante resistência à detecção por ferramentas de análise estatística.

## Segurança e uso responsável

O ShadowMessages é um projeto educacional voltado ao estudo de esteganografia, processamento de imagens e representação binária de dados.

A esteganografia oculta a presença aparente de uma mensagem, mas não substitui a criptografia. Para proteger informações confidenciais, recomenda-se criptografar o conteúdo antes de armazená-lo na imagem.

O projeto não deve ser utilizado para ocultar ou distribuir arquivos maliciosos, contornar mecanismos de segurança ou acessar informações sem autorização.

## Possíveis melhorias

- Implementar suporte à ocultação e recuperação de arquivos binários.
- Adicionar criptografia opcional antes da codificação.
- Armazenar o tamanho original da mensagem para permitir a recuperação de conteúdos com bytes nulos.
- Desenvolver uma interface gráfica.
- Implementar testes automatizados para codificação e decodificação.
- Comparar a qualidade visual das imagens antes e depois da inserção dos dados.
- Implementar validação de integridade por meio de hashes.

## Autor

**Rian Zanini Lascasas de Gouvêia**

- GitHub: [@RianZanini](https://github.com/RianZanini)

## Licença

Este projeto pode ser distribuído sob a licença MIT. Para isso, adicione um arquivo `LICENSE` com o texto oficial da licença antes de declarar o projeto licenciado sob esses termos.
