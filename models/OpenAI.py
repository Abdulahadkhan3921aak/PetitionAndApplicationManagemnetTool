
def get_testAIGenerated_Prompt(info: str):
    promtEngineered = open(f"{prompts_folder}/testAIGenerated.txt").read()
    system_prompt = open(f"{prompts_folder}/testAIGenSystemPrompt.txt").read()
    # Create the chat prompt with system and user messages
    system_message = SystemMessagePromptTemplate.from_template(system_prompt)
    user_message = HumanMessagePromptTemplate.from_template("{promtEngineered}: {info}")

    # Combine the system and user messages
    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # Pass the variables (pretext and info)
    messages = chat_prompt.format_messages(pretext=promtEngineered, info=info)

    # Get the response from the model
    response = llm(messages)
    return response.content

    
        
def get_testingAIGenerated_Prompt(info: str):
    promtEngineered = open(f"{prompts_folder}/testingAIGenerated.txt").read()
    system_prompt = open(f"{prompts_folder}/testingAIGenSystemPrompt.txt").read()
    # Create the chat prompt with system and user messages
    system_message = SystemMessagePromptTemplate.from_template(system_prompt)
    user_message = HumanMessagePromptTemplate.from_template("{promtEngineered}: {info}")

    # Combine the system and user messages
    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # Pass the variables (pretext and info)
    messages = chat_prompt.format_messages(pretext=promtEngineered, info=info)

    # Get the response from the model
    response = llm(messages)
    return response.content

    
        
def get_testing2AIGenerated_Prompt(info: str):
    promtEngineered = open(f"{prompts_folder}/testing2AIGenerated.txt").read()
    system_prompt = open(f"{prompts_folder}/testing2AIGenSystemPrompt.txt").read()
    # Create the chat prompt with system and user messages
    system_message = SystemMessagePromptTemplate.from_template(system_prompt)
    user_message = HumanMessagePromptTemplate.from_template("{promtEngineered}: {info}")

    # Combine the system and user messages
    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # Pass the variables (pretext and info)
    messages = chat_prompt.format_messages(pretext=promtEngineered, info=info)

    # Get the response from the model
    response = llm(messages)
    return response.content

    
        