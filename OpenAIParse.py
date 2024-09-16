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
        promtEngineerd = open(f"{{prompts_folder}}{name}.txt").read()
        response = llm.invoke(promtEngineerd + ":" + info)
        return response.content

        """
        )

    with open("./models/OpenAI.py", "w") as f:
        f.writelines(OpenAI_lines)

    return func_name_list
