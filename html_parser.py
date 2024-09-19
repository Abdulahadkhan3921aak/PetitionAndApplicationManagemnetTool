import re
import os
import json
from function_app_parser import function_app_parser
from OpenAIParse import write_to_OpenAI


def create_file(directory, fName):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Define the full path for the new file
    file_path = os.path.join(directory, f"{fName}Prompt.txt")

    # Create the file (open in write mode to create if not exists)
    with open(file_path, "w") as file:
        pass  # Just create the file; no content is added

    file_path = os.path.join(directory, f"{fName}SystemPrompt.txt")

    # Create the file (open in write mode to create if not exists)
    with open(file_path, "w") as file:
        pass  # Just create the file; no content is added

    print(f"File created: {file_path}")


def parse_html_to_form(html_string, filename: str):

    filename_with_underscores = ""

    for x in filename:
        if x != x.lower() and x != filename[0]:
            filename_with_underscores += "_"
            filename_with_underscores += x.lower()
        else:
            filename_with_underscores += x.lower()

    print(filename_with_underscores)

    # Define a mapping of placeholders to field details
    field_mapping = json.load(open("field_mapping.json"))

    # Initialize the form structure
    form = {"id": filename, "fields": []}

    prompt_tag_list = [
        "[Title]",
        "[AI Generated]",
        "[Ai Generated]",
        "[AI Generated Text]",
        "[Ai Generated Text]",
        "[Case Details]",
        "[Case Descriptions]",
        "[Case Description]",
        "[Prayer]",
        "[Prayers]",
        "[Grounds]",
        "[Affidavit]",
        "[Notice Body]",
        "[AI Generated Notice Body]",
    ]

    replace_list = []
    prompt_replace_list = []

    # Find all placeholders in the HTML
    placeholders = re.findall(r"\[([^\]]+)\]", html_string)

    # For each placeholder found, map it to the corresponding field
    for placeholder in placeholders:
        field = field_mapping.get(f"[{placeholder}]", None)
        if field and field not in form["fields"]:
            form["fields"].append(field)
            if f"[{placeholder}]" not in prompt_tag_list:
                replace_list.append({placeholder: field["name"]})
            else:
                prompt_replace_list.append({placeholder: field["name"]})
    file_names = []

    for x in prompt_tag_list:
        x = x.replace("[", "").replace("]", "")
        if x in placeholders:
            file_names.append(f"{filename}{x.replace(' ', '')}")

    with open(f"templates/{filename}.py", "w") as f:
        f.write(
            f'{filename}Document = """ {html_string} """.replace("\\n","")\n\n\n{filename}Form = {form}'
        )

    with open(f"templates/AllTemplates.py", "a") as f:
        f.write(
            f"from templates.{filename} import {filename}Document, {filename}Form\n"
        )

    for name in file_names:
        create_file(f"models/Prompts", f"{name}")

    write_to_OpenAI(file_names=file_names)

    function_app_parser(
        form=form,
        filename=filename,
        filename_with_underscores=filename_with_underscores,
        replace_list=replace_list,
        prompt_replace_list=prompt_replace_list,
    )
