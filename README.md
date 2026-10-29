# llamaindex-rag-chatbot

Chatbot RAG com LlamaIndex que responde perguntas com base nas suas anotações e PDFs de aula, exibindo as fontes usadas.

## Requisitos

- Python 3.10+
- Variável `OPENAI_API_KEY` definida

## Instalação

```bash
pip install -r requirements.txt
```

## Estrutura esperada

Coloque seus arquivos de estudo em `data/` (ex.: `.pdf`, `.md`, `.txt`).

```text
data/
  aula1.pdf
  resumo.md
```

## Uso

Responder uma pergunta única:

```bash
python chatbot.py --question "Quais são os tipos de memória?"
```

Modo interativo:

```bash
python chatbot.py
```

Opções:

- `--data-dir`: diretório dos documentos (padrão: `data`)
- `--persist-dir`: diretório de persistência do índice (padrão: `.storage`)

As respostas incluem uma seção **Fontes** com os arquivos recuperados no contexto da resposta.
