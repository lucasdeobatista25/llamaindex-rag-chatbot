import unittest
from types import SimpleNamespace

from chatbot import format_sources


class FormatSourcesTest(unittest.TestCase):
    def test_returns_unique_file_names(self):
        node1 = SimpleNamespace(node=SimpleNamespace(metadata={"file_path": "/docs/aula1.pdf"}))
        node2 = SimpleNamespace(node=SimpleNamespace(metadata={"file_path": "/docs/aula1.pdf"}))
        node3 = SimpleNamespace(node=SimpleNamespace(metadata={"file_path": "/docs/resumo.md"}))

        self.assertEqual(format_sources([node1, node2, node3]), ["aula1.pdf", "resumo.md"])

    def test_ignores_nodes_without_file_path(self):
        node1 = SimpleNamespace(node=SimpleNamespace(metadata={}))
        node2 = SimpleNamespace(node=SimpleNamespace(metadata={"file_path": "/docs/aula2.pdf"}))

        self.assertEqual(format_sources([node1, node2]), ["aula2.pdf"])


if __name__ == "__main__":
    unittest.main()
