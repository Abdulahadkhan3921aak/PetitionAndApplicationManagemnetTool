from typing import List, Dict


def function_app_parser(
    filename: str,
    form,
    filename_with_underscores: str,
    replace_list: List[Dict[str, str]],
    prompt_replace_list: List[Dict[str, str]],
):

    function_app_line = []
    with open("function_app.py", "r") as f:
        function_app_line = f.readlines()

    route_name = f"/{filename}"
    function_name = f"{filename_with_underscores}_post"

    replace_text = ""

    # Generate code for extracting fields
    field_extractions = ""

    for field in form["fields"]:
        if field["type"] != "list":
            field_extractions += (
                f'        {field["name"]} = req_body.get("{field["name"]}")\n'
            )
            for keys in replace_list:
                for key, value in keys.items():
                    if field["name"] == value:
                        replace_text += f'        html_template = html_template.replace("[{value}]", {field["name"]} if {field["name"]} else "")\n'

            for keys in prompt_replace_list:
                for key, value in keys.items():
                    if field["name"] == value:
                        replace_text += f'        html_template = html_template.replace("[{value}]", {field["name"]} if {field["name"]} else "")\n'

        elif field["type"] == "list" and field["name"] == "Plaintiff":
            field_extractions += """        Plaintiff = request_data.get("Plaintiff")
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
            field_extractions += """        Defendant = request_data.get("Defendant")
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


        # Replace placeholders in the template with extracted values
        html_template = AllTemplates.{filename}Document

        # Extract form fields dynamically
{field_extractions}

        # Replace placeholders in the template with extracted values       

{replace_text}

        # if Applicant_Name != None:
        #     if DedefendantString != None:
        #         title = f"{{Applicant_Name}} vs {{DefendantString}}"
        #     else:
        #         title = f"{{Applicant_Name}} vs State"

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

    get_func = f"""
# region {filename}

 
@app.route("{filename}", methods=["GET"])
async def {filename_with_underscores}_get(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.{filename}Form),
        mimetype="application/json",
    )\n\n
"""

    function_app_line.append(get_func)
    function_app_line.append(function_code)
    function_app_line.append("\n\n# endregion\n\n")

    with open("function_app.py", "w") as f:
        f.writelines(function_app_line)
