class AgentManager:
    """Agent manager for managing GPT agents"""

    def __init__(self):
        self.next_key = 0
        self.agents = {}  # key, (task, full_message_history, model)

    # Create new GPT agent
    # TODO: Centralise use of create_chat_completion() to globally enforce token limit

    def create_agent(self, task: str, prompt: str, model: str) -> tuple[int, str]:
        """Create a new agent and return its key

        Args:
            task: The task to perform
            prompt: The prompt to use
            model: The model to use
        Returns:
            The key of the new agent
        """