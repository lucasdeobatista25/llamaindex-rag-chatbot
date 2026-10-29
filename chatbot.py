from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Iterable


def format_sources(source_nodes: Iterable[Any]) -> list[str]:
    sources: list[str] = []
    seen: set[str] = set()

    for node in source_nodes:
        file_path = node.node.metadata.get("file_path") if node.node and node.node.metadata else None
        if not file_path:
            continue

        source = Path(file_path).name
        if source in seen:
            continue

        seen.add(source)
        sources.append(source)

    return sources


class RAGChatbot:
    def __init__(self, data_dir: str = "data", persist_dir: str = ".storage", similarity_top_k: int = 3) -> None:
        self.data_dir = Path(data_dir)
        self.persist_dir = Path(persist_dir)
        self.similarity_top_k = similarity_top_k

        self._configure_models()
        self.index = self._load_or_create_index()

    def _configure_models(self) -> None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("Defina OPENAI_API_KEY para usar o chatbot.")
        try:
            from llama_index.core import Settings
            from llama_index.embeddings.openai import OpenAIEmbedding
            from llama_index.llms.openai import OpenAI
        except ImportError as exc:
            raise ImportError("Dependências não instaladas. Execute: pip install -r requirements.txt") from exc

        Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    def _load_or_create_index(self):
        try:
            from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage
        except ImportError as exc:
            raise ImportError("Dependências não instaladas. Execute: pip install -r requirements.txt") from exc

        if self.persist_dir.exists() and any(self.persist_dir.iterdir()):
            storage_context = StorageContext.from_defaults(persist_dir=str(self.persist_dir))
            return load_index_from_storage(storage_context)

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Diretório de dados não encontrado: {self.data_dir}")

        documents = SimpleDirectoryReader(input_dir=str(self.data_dir), recursive=True).load_data()
        if not documents:
            raise ValueError(f"Nenhum documento encontrado em {self.data_dir}")

        index = VectorStoreIndex.from_documents(documents)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        index.storage_context.persist(persist_dir=str(self.persist_dir))
        return index

    def ask(self, question: str) -> str:
        query_engine = self.index.as_query_engine(similarity_top_k=self.similarity_top_k)
        response = query_engine.query(question)
        sources = format_sources(response.source_nodes)

        if not sources:
            return f"{response}\n\nFontes: não identificadas"

        formatted_sources = "\n".join(f"- {source}" for source in sources)
        return f"{response}\n\nFontes:\n{formatted_sources}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot RAG com LlamaIndex")
    parser.add_argument("--data-dir", default="data", help="Diretório com anotações e PDFs")
    parser.add_argument("--persist-dir", default=".storage", help="Diretório para persistência do índice")
    parser.add_argument("--question", help="Pergunta única para responder")
    args = parser.parse_args()

    bot = RAGChatbot(data_dir=args.data_dir, persist_dir=args.persist_dir)

    if args.question:
        print(bot.ask(args.question))
        return

    print("Chatbot pronto. Digite sua pergunta (ou 'sair').")
    while True:
        question = input("\nPergunta: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            break

        if question:
            print(bot.ask(question))


if __name__ == "__main__":
    main()
