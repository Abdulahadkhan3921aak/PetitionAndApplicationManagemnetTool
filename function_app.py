# region testing2 
@app.route("testing2", methods=["GET"])
async def testing2_get(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.testing2Form),
        mimetype="application/json",
    )



@app.route("/testing2", methods=["POST"])
async def testing2_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()


        # Replace placeholders in the template with extracted values
        html_template = AllTemplates.testing2Document

        # Extract form fields dynamically
        Applicant_Name = req_body.get("Applicant_Name")
        Plaintiff_SO_DO = req_body.get("Plaintiff_SO_DO")
        Plaintiff_Father_Name = req_body.get("Plaintiff_Father_Name")
        Applicant_Address = req_body.get("Applicant_Address")
        Respondent_Name = req_body.get("Respondent_Name")
        Son_Daughter = req_body.get("Son_Daughter")
        Defendant_Father_Name = req_body.get("Defendant_Father_Name")
        Defendant_Address = req_body.get("Defendant_Address")
        AI_Generated_Text = req_body.get("AI_Generated_Text")
        Day = req_body.get("Day")
        Month = req_body.get("Month")
        Year = req_body.get("Year")
        Advocates_Name = req_body.get("Advocates_Name")
        Office_Address = req_body.get("Office_Address")
        CourtAddress = req_body.get("CourtAddress")


        # Replace placeholders in the template with extracted values       

        html_template = html_template.replace("[Applicant_Name]", Applicant_Name if Applicant_Name else "")
        html_template = html_template.replace("[Plaintiff_SO_DO]", Plaintiff_SO_DO if Plaintiff_SO_DO else "")
        html_template = html_template.replace("[Plaintiff_Father_Name]", Plaintiff_Father_Name if Plaintiff_Father_Name else "")
        html_template = html_template.replace("[Applicant_Address]", Applicant_Address if Applicant_Address else "")
        html_template = html_template.replace("[Respondent_Name]", Respondent_Name if Respondent_Name else "")
        html_template = html_template.replace("[Son_Daughter]", Son_Daughter if Son_Daughter else "")
        html_template = html_template.replace("[Defendant_Father_Name]", Defendant_Father_Name if Defendant_Father_Name else "")
        html_template = html_template.replace("[Defendant_Address]", Defendant_Address if Defendant_Address else "")
        html_template = html_template.replace("[AI_Generated_Text]", AI_Generated_Text if AI_Generated_Text else "")
        html_template = html_template.replace("[Day]", Day if Day else "")
        html_template = html_template.replace("[Month]", Month if Month else "")
        html_template = html_template.replace("[Year]", Year if Year else "")
        html_template = html_template.replace("[Advocates_Name]", Advocates_Name if Advocates_Name else "")
        html_template = html_template.replace("[Office_Address]", Office_Address if Office_Address else "")
        html_template = html_template.replace("[CourtAddress]", CourtAddress if CourtAddress else "")


        # if Applicant_Name != None:
        #     if DedefendantString != None:
        #         title = f"{Applicant_Name} vs {DefendantString}"
        #     else:
        #         title = f"{Applicant_Name} vs State"

        helper.generate_petitions(
            user_id=req_body.get("user_id"),
            chat_id=req_body.get("chat_id"),
            timecreated=req_body.get("timecreated"),
            Data=req_body,
            Category=req_body.get("Category"),
            Document=html_template,
            ApplicantName=req_body.get("Applicant_Name"),
            Title=title,
        )

        return func.HttpResponse(body=html_template, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
# end region

