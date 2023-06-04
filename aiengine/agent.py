from aiengine.config.config import Config
from aiengine.chat import chat_with_ai
from aiengine.json_utils.json_fix_llm import fix_json_using_multiple_techniques


class Agent:
    """Agent class for interacting with AgentX.

    Attributes:
        ai_name: The name of the agent.
        memory: The memory object to use.
        full_message_history: The full message history.
        next_action_count: The number of actions to execute.
        system_prompt: The system prompt is the initial prompt that defines everything the AI needs to know to achieve its task successfully.
        Currently, the dynamic and customizable information in the system prompt are ai_name, description and goals.

        triggering_prompt: The last sentence the AI will see before answering. For AgentX, this prompt is:
            Determine which next command to use, and respond using the format specified above:
            The triggering prompt is not part of the system prompt because between the system prompt and the triggering
            prompt we have contextual information that can distract the AI and make it forget that its goal is to find the next task to achieve.
            SYSTEM PROMPT
            CONTEXTUAL INFORMATION (memory, previous conversations, anything relevant)
            TRIGGERING PROMPT

        The triggering prompt reminds the AI about its short term meta task (defining the next task)
    """

    def __init__(
        self,
        ai_name,
        memory,
        full_message_history,
        next_action_count,
        system_prompt,
        triggering_prompt,
    ):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.system_prompt = system_prompt
        self.triggering_prompt = triggering_prompt

    def start_interaction_loop(self):
        # Interaction Loop
        cfg = Config()
        loop_count = 0
        command_name = None
        arguments = None
        user_input = ""

            # Send message to AI, get response

        assistant_reply = chat_with_ai(
            self.system_prompt,
            self.triggering_prompt,
            self.full_message_history,
            self.memory,
            cfg.fast_token_limit,
        )  # TODO: This hardcodes the model to use GPT3.5. Make this an argument

        print("assistant_reply:", assistant_reply)
        assistant_reply_json = fix_json_using_multiple_techniques(assistant_reply)
        print('assistant_reply_json:', assistant_reply_json)