# Desenvolvimento de _dataset_ de laudos e imagens de Radiografia de Tórax

Este repositório contém _scripts_ utilizados na automatização do processo de desenvolvimento de uma base de dados de laudos de imagens de Radiografias de Tórax realizadas no Hospital Universitário Alcides Carneiro (HUAC).

## Estrutura de diretórios

```diff
Reports-Images-Dataset-Development
├── data
│   ├── input
│   ├── output
│   └── json
├── src
│   ├── util
│   │   ├── pdf_util.py
│   │   └── dcm_util.py
│   ├── main_normalize.py
│   ├── main_json.py
│   ├── main_dataset.py
│   └── execute.sh
├── util
│   └── requirements.txt
└── README.md
```

O diretório **util** contém o arquivo `requirements.txt`, que auxilia no gerenciamento das dependências utilizadas.

Já o diretório **src**, contém os _scripts_ responsáveis por:

 - extrair texto de PDFs;
 - converter imagens para formatos diferentes (.dcm -> .pdf);
 - construir _json_ para armazenar os dados gerados;
 - fazer _upload_ do dataset no [HuggingFace](https://huggingface.co/).

Por fim, o diretório **data** contém os dados a serem utilizados na construção do _dataset_.

## Diretório **data** e estrutura esperada

Ao clonar o repositório, você deve criar, além do diretório **data**, outros três sub-diretórios: **input**, **output** e **json**.

Para isso, clone o repositório com:

```bash
git clone https://Pibic-Pibiti-Huac/Reports-Images-Dataset-Development.git
```

Se dirija, então, à raiz do projeto:

```bash
cd ./Reports-Images-Dataset-Development/
```

Agora, crie os diretórios recomendados:

```bash
mkdir -p ./data/{input,output,json}
```

## Adicionando dados

A automatização espera que os diretórios **input** e **output** contenham vários sub-diretórios com o número da requisição dos exames. Dentro de cada um desses subdiretórios, devem estar contidos os arquivos extraídos diretamente do sistema do HUAC. Siga o exemplo abaixo.

Considere um exame com o número de requisição **12345678900987**.

```diff
input
└── 12345678900987
    ├── report.pdf
    ├── hwt832.dcm
    └── dfkjdd.dcm
```

> [!WARNING]
> Apesar do que está escrito no exemplo, o .pdf do laudo não precisa se chamar `report.pdf`. Basta apenas que ele possua a extensão .pdf. O mesmo vale para os arquivos das imagens em formato _dicom_ (.dcm).

## Executando script principal

Tendo garantindo que o diretório **input** siga os moldes, basta executar o _script bash.

Você precisará passar três informações como argumento:

 - Token do HuggingFace;
 - ID do dataset (repositório) no HuggingFace;
 - _path_ para o json que originará o dataset. (**sugiro que seja `./data/json/reports_images.json`**).

Estando na raiz do projeto, torne o script bash executável:

```bash
chmod +x ./src/execute.sh
```

Agora basta executar o script_bash:

```bash
./src/execute.sh "hfp042iomo3xjkcnwoie" "guilhermenf/dataset_teste" "./data/json/reports_images.json"
```

## Autor

**Guilherme Noronha**, graduando em Ciência da Computação na Universidade Federal de Campina Grande (UFCG).

 - [guinoronhaf](https://github.com/guinoronhaf).
 - [guilhermenf](https://huggingface.co/guilhermenf)
 - [Guilherme Fragoso](https://www.linkedin.com/in/guilherme-noronha-fragoso/)

---

Este repositório faz parte de um projeto de pesquisa PIBIC/PIBITI, desenvolvido na Universidade Federal de Campina Grande (UFCG).

 - **PIBIC**: Concepção e Avaliação de uma Ferramenta de Inteligência Artificial para a Geração de Laudos de Citologia Oncótica.

 - **PIBITI**: Desenvolvimento de um Sistema de Geração Automática de Laudos Médicos por Reconhecimento de Voz e Processamento de Linguagem Natural.
