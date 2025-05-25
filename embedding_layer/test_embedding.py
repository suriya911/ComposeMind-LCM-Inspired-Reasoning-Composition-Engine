import unittest
from app import segment_text, generate_embeddings

class TestEmbeddingService(unittest.TestCase):
    def test_segment_text(self):
        text = "First sentence. Second sentence! Third sentence?"
        sentences = segment_text(text)
        self.assertEqual(len(sentences), 3)
        
    def test_generate_embeddings(self):
        sentences = ["Test sentence one.", "Test sentence two."]
        embeddings = generate_embeddings(sentences)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(embeddings[0]), 384)  # MiniLM-L6-v2 embedding size

if __name__ == '__main__':
    unittest.main() 