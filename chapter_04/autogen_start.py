from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

# Load the configuration list from the config file.
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST_OLLAMA")

# Create the agent that uses the LLM.
assistant = ConversableAgent(
    "agent", 
    llm_config={"config_list": config_list},
    system_message=(
        "You are a coding assistant. "
        "When you write code, always return it in a single fenced Python code block. "
        "The first line inside the code block must be "
        "'# filename: main.py'. "
        "Only output code unless explanation is requested."
        "You should be able to save the file if requested"
    )    
)

# Create the agent that represents the user in the conversation.
user_proxy = UserProxyAgent(
    "user",
    code_execution_config={
        "work_dir": "working",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

# Start the conversation.
user_proxy.initiate_chat(assistant, message="code a classic asteroids game in Python using Pygame. Save it as main.py")
