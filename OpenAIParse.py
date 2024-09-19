def write_to_OpenAI(file_names: list) -> list[str]:
    OpenAI_lines = []
    with open(f"./models/OpenAI.py", "r") as f:
        OpenAI_lines = f.readlines()

    func_name_list = []

    for name in file_names:
        funcName = f"get_{name}_Prompt"
        # also add _ to the name but there are no spaces in the name
        funcName = funcName.replace(" ", "_")
        func_name_list.append({name: funcName})
        OpenAI_lines.append(
            f"""
def {funcName}(info: str):
    promtEngineered = open(f"{{prompts_folder}}/{name}.txt").read()
    system_prompt = open(f"{{prompts_folder}}/{name[:-6]}SystemPrompt.txt").read()
    # Create the chat prompt with system and user messages
    system_message = SystemMessagePromptTemplate.from_template(system_prompt)
    user_message = HumanMessagePromptTemplate.from_template("{{promtEngineered}}: {{info}}")

    # Combine the system and user messages
    chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # Pass the variables (pretext and info)
    messages = chat_prompt.format_messages(pretext=promtEngineered, info=info)

    # Get the response from the model
    response = llm(messages)
    return response.content

    
        """
        )

    with open("./models/OpenAI.py", "w") as f:
        f.writelines(OpenAI_lines)

    return func_name_list
