from unittest import TestCase
from aiengine.aiprocessor import process_message


class TestAIProcessor(TestCase):
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
        

    def test_process_text_summerize(cls):
        print("test_process_message")
        # Embed a sample text
        sample_text = "I wantv to summerize the below paragraph and write it a file.\n" + \
        "CHAIR POWELL. Good afternoon. Before discussing today’s meeting, let me comment " +\
        "briefly on recent developments in the banking sector. Conditions in that sector have broadly " +\
        "improved since early March, and the U.S banking system is sound and resilient. We will " +\
        "continue to monitor conditions in this sector. We are committed to learning the right lessons " +\
        "from this episode and will work to prevent events like these from happening again. As a first " +\
        "step in that process, last week we released Vice Chair for Supervision Barr’s Review of the " +\
        "Federal Reserve’s Supervision and Regulation of Silicon Valley Bank. The review’s findings " +\
        "underscore the need to address our rules and supervisory practices to make for a stronger and " +\
        "more resilient banking system, and I am confident that we will do so. " +\
        "The AI engine is a software system that is designed to simulate human behaviors and "
        process_message(sample_text)