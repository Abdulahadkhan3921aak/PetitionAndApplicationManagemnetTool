import re
import os
import json


def create_file(directory, fName):
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Define the full path for the new file
    file_path = os.path.join(directory, f"{fName}Prompt.txt")

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
        "[AI Generated Text]",
        "[Case Details]",
        "[Case Descriptions] ",
        "[Prayers]",
        "[Grounds]",
        "[Affidavit]",
    ]

    # Find all placeholders in the HTML
    placeholders = re.findall(r"\[([^\]]+)\]", html_string)

    # For each placeholder found, map it to the corresponding field
    for placeholder in placeholders:
        field = field_mapping.get(f"[{placeholder}]", None)
        if field:
            form["fields"].append(field)

    file_names = []

    for x in prompt_tag_list:
        x = x.replace("[", "").replace("]", "")
        if x in placeholders:
            file_names.append(f"{filename}{x}")

    with open(f"templates/{filename}.py", "w") as f:
        f.write(
            f'{filename}Document = """ {html_string} """\n\n\n{filename}Form = {form}'
        )

    # Example usage
    for name in file_names:
        create_file(f"models/Prompts", f"{name}")

    OpenAI_lines = []
    with open(f"./models/OpenAI.py", "r") as f:
        OpenAI_lines = f.readlines()

    for name in file_names:
        funcName = f"get_{name}_Prompt"
        # also add _ to the name but there are no spaces in the name
        funcName = funcName.replace(" ", "_")
        OpenAI_lines.append(
            f"""
def {funcName}(info: str):
    promtEngineerd = open(f"{{prompts_folder}}{name[:-4]}.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content

    """
        )

    function_app_line = []
    with open("function_app.py", "r") as f:
        function_app_line = f.readlines()

    get_prompt_func = f"""
# region {filename} 
@app.route("{filename}", methods=["GET"])
async def {filename_with_underscores}_get(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.{filename}Form),
        mimetype="application/json",
    )\n\n
"""

    route_name = f"/{filename}"
    function_name = f"{filename_with_underscores}_post"

    # Generate code for extracting fields
    field_extractions = ""

    for field in form["fields"]:
        if field["type"] != "list":
            field_extractions += f'{field["name"]} = req_body.get("{field["name"]}")\n'
        elif field["type"] == "list" and field["name"] == "Plaintiff":
            field_extractions += """Plaintiff = request_data.get("Plaintiff")
PlaintiffsNames = [x.get("PlaintiffName") for x in Plaintiff]
PlaintiffString = "".join(
    AllTemplates.plaintiff_object.replace("[Plaintiff]", x.get("PlaintiffName"))
    .replace("[Plaintiff Son/Daughter]", x.get("PlaintiffSonDaughter"))
    .replace("[Plaintiff Father Name]", x.get("PlaintiffFatherName"))
    .replace("[Plaintiff Address]", x.get("PlaintiffAddress"))
    + "<br>"
    for x in Plaintiff
)
        """
        elif field["type"] == "list" and field["name"] == "Defendant":
            field_extractions += """Defendant = request_data.get("Defendant")
DefendantsNames = [x.get("DefendantName") for x in Defendant]
DefendantString = "".join(
    AllTemplates.defendant_object.replace("[Defendant]", x.get("DefendantName"))
    .replace("[Defendant Son/Daughter]", x.get("DefendantSonDaughter"))
    .replace("[Defendant Father Name]", x.get("DefendantFatherName"))
    .replace("[Defendant Address]", x.get("DefendantAddress"))
    + "<br>"
    for x in Defendant
        )
"""

    # Template for the function
    function_code = f"""
@app.route("{route_name}", methods=["POST"])
async def {function_name}(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Extract form fields dynamically
        {field_extractions}


        # Replace placeholders in the template with extracted values
        html_template = AllTemplates.{filename}Document)
        for key, value in req_body.items():
            placeholder = f"[{{{{key}}}}]"
            html_template = html_template.replace(placeholder, value if value else "")

        AiGeneratedText = OpenAI.get_{filename_with_underscores}(req_body.get("AiGeneratedText", ""))
        html_template = html_template.replace("[AI Generated]", AiGeneratedText)

        helper.generate_petitions(
            user_id=req_body.get("user_id"),
            chat_id=req_body.get("chat_id"),
            timecreated=req_body.get("timecreated"),
            Data=req_body,
            Category=req_body.get("Category"),
            Document=html_template,
            ApplicantName=req_body.get("{form.get('fields')[0]['name']}"),
            Title=title,
        )

        return func.HttpResponse(body=html_template, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {{e}}")
        return func.HttpResponse("Internal Server Error", status_code=500)
"""

    function_app_line.append(get_prompt_func)


    with open("function_app.py", "w") as f:
        f.writelines(function_app_line)
    
    with open("./models/OpenAI.py", "w") as f:
        f.writelines(OpenAI_lines)
