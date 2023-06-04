from unittest import TestCase

from aiengine.memory.pinecone import PineconeMemory
from aiengine.config import Config
import tracemalloc
tracemalloc.start()


class TestPinecone(TestCase):
    """
    Test cases for the PromptGenerator class, which is responsible for generating
    prompts for the AI with constraints, commands, resources, and performance evaluations.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the initial state for each test method by creating an instance of PromptGenerator.
        """
        print("setUpClass")
        cfg = Config()
        
        cls.pineconeMemory = PineconeMemory(cfg)

    def test_add(cls):
        print("test_add")
        # Embed a sample text
        sample_text = "This is a sample text for testing."
        cls.pineconeMemory.add(sample_text)

    def test_get(cls):
        cls.pineconeMemory.clear()
        sample_text1 = "Nuwan was born in Sri Lanka."
        cls.pineconeMemory.add(sample_text1)

        sample_text2 = "Steven was born in Belgium."
        cls.pineconeMemory.add(sample_text2)

        sample_text3 = "Nobody was born in nowhere."
        cls.pineconeMemory.add(sample_text2)

        query = "Who was born in Belgium?"
        search_results= cls.pineconeMemory.get(query)
        print('search_results: ',search_results)

        cls.assertIn(sample_text2, search_results)

    def test_get_stats(cls):
        stats= cls.pineconeMemory.get_stats()
        print('stats: ',stats)