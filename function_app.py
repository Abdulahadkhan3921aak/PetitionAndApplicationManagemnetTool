# region imports

from math import e
from tempfile import template
from turtle import title
import azure.functions as func
import logging
import templates.AllTemplates as AllTemplates
import models.OpenAI as OpenAI
import helper_functions as helper
import json

# endregion


# region API Functions


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# region Basepoints


@app.route("Petitions", methods=["GET"])
async def PettitionsData(req: func.HttpRequest) -> func.HttpResponse:
    response = {
        "Petitions": [
            {"Name": "Dissolution of Marriage", "Endpoint": "DissolutionOfMarriage"},
            {
                "Name": "Pre Arrest Bail Application",
                "Endpoint": "PreArrestBailApplication",
            },
            {
                "Name": "Pre Arrest Bail Certificate",
                "Endpoint": "PreArrestBailCertificate",
            },
            {
                "Name": "Suit For Specific Performance",
                "Endpoint": "SuitForSpecificPerformance",
            },
        ]
    }
    return func.HttpResponse(
        body=json.dumps(response, indent=4),
        # mimetype="application/json",
    )


@app.route("Applications", methods=["GET"])
async def ApplicationsData(req: func.HttpRequest) -> func.HttpResponse:

    response = {
        "Applications": [
            {"Name": "Superdari", "Endpoint": "Superdari"},
            {"Name": "Legal Notice", "Endpoint": "LegalNotice"},
            {"Name": "Power of Attorney", "Endpoint": "PowerOfAttorney"},
            {"Name": "Legal Certificate", "Endpoint": "LegalCertificate"},
            {
                "Name": "Early Hearing Application",
                "Endpoint": "EarlyHearingApplication",
            },
        ]
    }

    return func.HttpResponse(
        body=json.dumps(response, indent=4),
        mimetype="application/json",
    )


# endregion


# region Applications


# region Early Hearing Application


@app.route("EarlyHearingApplication", methods=["GET"])
async def EarlyHearingApplication(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.EarlyHearingAplicationForm),
        mimetype="application/json",
    )


@app.route("EarlyHearingApplication", methods=["POST"])
async def EarlyHearingApplication_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        JudgeOf = request_data.get("JudgeOf")
        ApplicantName = request_data.get("ApplicantName")
        DefedantName = request_data.get("DefedantName")
        Subject = request_data.get("Subject")
        ApplicationInfo = request_data.get("ApplicationInfo")
        AdvocateName = request_data.get("AdvocateName")
        AdvocateOf = request_data.get("AdvocateOf")
        CourtName = request_data.get("CourtName")

        Subject = OpenAI.get_Early_Hearing_Subject(f"Subject: {Subject}")
        ApplicationInfo = OpenAI.get_Early_Hearing(
            f"Subject/Reason for Application: {Subject} Additional Information: {ApplicationInfo} , Optional Data : Applicant Name: {ApplicantName} , Defendant Name: {DefedantName}, Advocate Name: {AdvocateName}, Advocate Of: {AdvocateOf}, Court Name: {CourtName}"
        )

        html = (
            AllTemplates.EarlyHearingAplicationDocument.replace("[Judge Of]", JudgeOf)
            .replace("[Applicant]", ApplicantName)
            .replace("[Defendant]", DefedantName)
            .replace("[Subject]", Subject)
            .replace("[Application Body]", ApplicationInfo)
            .replace("[Advocate Name]", AdvocateName)
            .replace("[Advocate Of]", AdvocateOf)
            .replace("[Court Name]", CourtName)
        )

        title = f"{ApplicantName} vs {DefedantName}"

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=ApplicantName,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Superdari


@app.route("Superdari", methods=["GET"])
async def Superdari(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.SuperdariTemplateForm), mimetype="application/json"
    )


@app.route("Superdari", methods=["POST"])
async def Superdari_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        Case_FIR_Number = request_data.get("Case_FIR_Number")
        Date = request_data.get("Date")
        Offence_US = request_data.get("Offence_US")
        Police_Station_Address = request_data.get("Police_Station_Address")
        Applicant_Name = request_data["Applicant_Name"]
        SO_DO = request_data["SO_DO"]
        Father_Name = request_data["Father_Name"]
        Applicant_Address = request_data["Applicant_Address"]
        Respondent_Name = request_data["Respondent_Name"]
        AI_Generated_Text = request_data["AI_Generated_Text"]
        Advocates_Name = request_data["Advocates_Name"]
        Office_Address = request_data["Office_Address"]
        CC_Number = request_data["CC_Number"]
        Vehicle_Company = request_data["Vehicle_Company"]
        Vehicle_Color = request_data["Vehicle_Color"]
        Model_Year = request_data["Model_Year"]
        Registration_Number = request_data["Registration_Number"]
        Chasis_Number = request_data["Chasis_Number"]
        Engine_Number = request_data["Engine_Number"]
        Court_Name = request_data["Court_Name"]
        Day = request_data["Day"]
        Month = request_data["Month"]
        Year = request_data["Year"]
        District = request_data["District"]

        html = (
            AllTemplates.SuperdariTemplateDocument.replace(
                "[Case_FIR_Number]", Case_FIR_Number
            )
            .replace("[Date]", Date)
            .replace("[Offence]", Offence_US)
            .replace("[Police_Station_Address]", Police_Station_Address)
            .replace("[Applicant_Name]", Applicant_Name)
            .replace("[S/O_D/O]", SO_DO)
            .replace("[Father_Name]", Father_Name)
            .replace("[Applicant_Address]", Applicant_Address)
            .replace("[Respondent_Name]", Respondent_Name)
            .replace("[Advocates_Name]", Advocates_Name)
            .replace("[Office_Address]", Office_Address)
            .replace("[CC_Number]", CC_Number)
            .replace("[Vehicle_Company]", Vehicle_Company)
            .replace("[Vehicle_Color]", Vehicle_Color)
            .replace("[Model_Year]", Model_Year)
            .replace("[Registration_Number]", Registration_Number)
            .replace("[Chasis_Number]", Chasis_Number)
            .replace("[Engine_Number]", Engine_Number)
            .replace("[Court_Name]", Court_Name)
            .replace("[Day]", Day)
            .replace("[Month]", Month)
            .replace("[Year]", Year)
            .replace("[District]", District)
        )

        info = (
            f"Applicant Name {Applicant_Name} {SO_DO} Father Name {Father_Name} Resident of {Applicant_Address} "
            f"Vehicle Company: {Vehicle_Company} Vehicle Color: {Vehicle_Color} "
            f"Model Year: {Model_Year} Registration Number: {Registration_Number} "
            f"Chasis Number: {Chasis_Number} Engine Number: {Engine_Number}. "
            f"Additional Information: {AI_Generated_Text}"
        )
        ai_generated_text = OpenAI.get_superdari_details(info)
        html = html.replace("[AI_generated_text]", ai_generated_text)

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        title = f"{Applicant_Name} vs {Respondent_Name}"

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=Applicant_Name,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Legal Notice


@app.route("LegalNotice", methods=["GET"])
async def LegalNotice(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.LegalNoticeTemplateForm),
        mimetype="application/json",
    )


@app.route("LegalNotice", methods=["POST"])
async def LegalNotice_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        Recipient_Name = request_data.get("Recipient_Name")
        Recipient_Address = request_data.get("Recipient_Address")
        Lawyer_Name = request_data.get("Lawyer_Name")
        Advocate_of = request_data.get("Advocate_of")
        Lawyer_Contact = request_data.get("Lawyer_Contact")
        Subject_of_the_Notice = request_data.get("Subject_of_the_Notice")
        Recipient_Parent_Name = request_data.get("Recipient_Parent_Name")
        Son_Daughter = request_data.get("Son_Daughter")
        AI_Genereated_Text = request_data.get("AI_Genereated_Text")

        html = (
            AllTemplates.LegalNoticeTemplateDocument.replace(
                "[Recipient Name]", Recipient_Name
            )
            .replace("[Son/Daughter]", Son_Daughter)
            .replace("[Recipient Parent Name]", Recipient_Parent_Name)
            .replace("[Recipient Address]", Recipient_Address)
            .replace("[Subject of the Notice]", Subject_of_the_Notice)
            .replace("[Lawyer Name]", Lawyer_Name)
            .replace("[Advocate of]", Advocate_of)
            .replace("[Lawyer Contact]", Lawyer_Contact)
        )

        info = (
            f"Recipient Name {Recipient_Name} {Son_Daughter} Parent Name {Recipient_Parent_Name} Resident of {Recipient_Address} "
            f"Additional Information: {AI_Genereated_Text}"
        )
        ai_generated_text = OpenAI.get_legal_notice(info)
        html = html.replace("[AI Generated Notice Body]", ai_generated_text)

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")
        title = f"{Recipient_Name} Ref: {Recipient_Parent_Name}"

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName="",
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Power Of Attorney


@app.route("PowerOfAttorney", methods=["GET"])
async def PowerOfAttorney(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.PowerOfAttornyTemplateForm),
        mimetype="application/json",
    )


@app.route("PowerOfAttorney", methods=["POST"])
async def PowerOfAttorney_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        CaseNumber = request_data.get("CaseNumber")
        Offense = request_data.get("Offence")
        Police_Station_Address = request_data.get("PoliceStationAddress")

        CourtOF = request_data.get("CourtOF")
        PlaintiffName = request_data["PlaintiffName"]
        Defendant = request_data["Defendant"]

        AdvocateName = request_data["AdvocateName"]
        AdvocateOf = request_data["AdvocateOf"]

        ApplicantName = request_data["ApplicantName"]

        Day = request_data["Day"]
        Month = request_data["Month"]
        Year = request_data["Year"]

        CourtAddress = request_data["CourtAddress"]
        CCNumber = request_data["CCNumber"]

        title = f"{PlaintiffName} vs {Defendant}"

        html = (
            AllTemplates.PowerOfAttornyTemplateDocument.replace(
                "[Case Number]", CaseNumber
            )
            .replace("[Offense]", Offense)
            .replace("[Police Station]", Police_Station_Address)
            .replace("[Court Name]", CourtOF)
            .replace("[Plaintiff Name]", PlaintiffName)
            .replace("[Defendant Name]", Defendant)
            .replace("[Advocate Name]", AdvocateName)
            .replace("[Advocate Of]", AdvocateOf)
            .replace("[Applicant Name]", ApplicantName)
            .replace("[Day]", Day)
            .replace("[Year]", Year)
            .replace("[Month]", Month)
            .replace("[Court Address]", CourtAddress)
            .replace("[CC Number]", CCNumber)
        )

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=ApplicantName,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Legal Certificate


@app.route("LegalCertificate", methods=["GET"])
async def LegalCertificate(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.legalCertificateTemplateForm),
        mimetype="application/json",
    )


@app.route("LegalCertificate", methods=["POST"])
async def LegalCertificate_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        Advocate_Name = request_data.get("Advocate_Name")
        Advocate_Of = request_data.get("Advocate_Of")
        Referance_Number = request_data.get("Referance_Number")
        Date = request_data.get("Date")
        AI_Generated_Text = request_data.get("AI_Generated_Text")

        html = (
            AllTemplates.legalCertificateTemplateDocument.replace(
                "[Advocate Name]", Advocate_Name
            )
            .replace("[Advocate Of]", Advocate_Of)
            .replace("[Ref Number]", Referance_Number)
            .replace("[Date]", Date)
        )

        info = AI_Generated_Text
        ai_generated_text = OpenAI.get_legal_cirtificate(info)
        html = html.replace("[AI Generated Text]", ai_generated_text)

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")
        title = f"{Advocate_Name} Ref: {Referance_Number}"

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=None,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Suit For Specific Performance


@app.route("SuitForSpecificPerformance", methods=["GET"])
async def SuitForSpecificPerformance(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.SuitForSpecificPerformanceForm),
        mimetype="application/json",
    )


@app.route("SuitForSpecificPerformance", methods=["POST"])
async def SuitForSpecificPerformance_post(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    try:
        request_data = req.get_json()

        CourtOF = request_data.get("CourtOF")

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        Plaintiff = request_data.get("Plaintiff")
        PlaintiffsNames = [x.get("PlaintiffName") for x in Plaintiff]
        PlaintiffString = "".join(
            AllTemplates.plaintiff_object.replace("[Plaintiff]", x.get("PlaintiffName"))
            .replace("[Plaintiff Son/Daughter]", x.get("PlaintiffSonDaughter"))
            .replace("[Plaintiff Father Name]", x.get("PlaintiffFatherName"))
            .replace("[Plaintiff Address]", x.get("PlaintiffAddress"))
            + "<br>"
            for x in Plaintiff
        )

        Defendant = request_data.get("Defendant")
        DefendantsNames = [x.get("DefendantName") for x in Defendant]
        DefendantString = "".join(
            AllTemplates.defendant_object.replace("[Defendant]", x.get("DefendantName"))
            .replace("[Defendant Son/Daughter]", x.get("DefendantSonDaughter"))
            .replace("[Defendant Father Name]", x.get("DefendantFatherName"))
            .replace("[Defendant Address]", x.get("DefendantAddress"))
            + "<br>"
            for x in Defendant
        )

        AiGeneratedText = request_data.get("AiGeneratedText")
        Day = request_data.get("Day")
        Month = request_data.get("Month")
        Year = request_data.get("Year")

        AdvocateName = request_data.get("AdvocateName")
        AdvocateOf = request_data.get("AdvocateOf")
        CourtName = request_data.get("CourtName")

        title = f"{Plaintiff} vs {Defendant}"

        html = (
            AllTemplates.SuitForSpecificPerformanceDocument.replace(
                "[Court OF]", CourtOF
            )
            .replace("[Plaintiff]", PlaintiffString)
            .replace("[Defendant]", DefendantString)
            .replace("[Day]", Day)
            .replace("[Month]", Month)
            .replace("[Year]", Year)
            .replace("[Advocate Name]", AdvocateName)
            .replace("[Advocate of]", AdvocateOf)
            .replace("[Court Address]", CourtName)
        )

        info = (
            "".join(
                f"Plaintiff Name {x.get('PlaintiffName')} {x.get('PlaintiffSonDaughter')} "
                f"Father Name {x.get('PlaintiffFatherName')} Resident of {x.get('PlaintiffAddress')} "
                for x in Plaintiff
            )
            + "".join(
                f"Defendant Name {x.get('DefendantName')} {x.get('DefendantSonDaughter')} "
                f"Father Name {x.get('DefendantFatherName')} Resident of {x.get('DefendantAddress')} "
                for x in Defendant
            )
            + (f"Additional Information: {AiGeneratedText}")
        )

        # AiGeneratedText = OpenAI.get_suit_for_specific_performance(info)

        html = html.replace("[AI Generated]", AiGeneratedText)

        helper.generate_petitions(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=Plaintiff,
            Title=title,
        )

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# endregion


# region Petitions


# region PreArrest Bail Application


@app.route("PreArrestBailApplication", methods=["GET"])
async def PreArrestBailApplication(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.PreArrestBailApplicationForm),
        mimetype="application/json",
    )


@app.route("PreArrestBailApplication", methods=["POST"])
async def PreArrestBailApplication_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        court_name = request_data.get("Court_Name")
        petitioner = request_data.get("Petitioner")
        son_daughter = request_data.get("Son_Daughter")
        father_name = request_data.get("Father_Name")
        resident_of = request_data.get("Resident_Of")
        fir_no = request_data.get("Fir_no")
        police_station = request_data.get("Police_Station")
        ai_generated_text = request_data.get("AI_Generated_Text")
        advocate_name = request_data.get("Advocate_Name")
        advocate_of = request_data.get("Advocate_Of")
        Date = request_data.get("Date")
        day = request_data.get("Day")
        month = request_data.get("Month")
        year = request_data.get("Year")
        ai_generated_affidavit = request_data.get("AI_Generated_Affidavit")

        title = f"{petitioner} vs The State"

        ai_generated_affidavit = (
            OpenAI.generate_affidavit(
                f"Name : {petitioner} , Father's Name {father_name}, Address {resident_of} , Statement {ai_generated_affidavit}, date of signing {Date}"
            )
            .replace("```html\n", "")
            .replace("\n```", "")
        )

        ai_generated_text = (
            OpenAI.get_pre_arrest_bail_application(
                f"Name: {petitioner}, Address {resident_of}, Statement {ai_generated_affidavit}, date of application {Date} , Fir NO {fir_no} , Police Station {police_station} Grounds {ai_generated_text}"
            )
            .replace("```html\n", "")
            .replace("\n```", "")
        )

        html = (
            AllTemplates.PreArrestBailApplicationDocument.replace(
                "[Court Name]", court_name
            )
            .replace("[Petitioner]", petitioner)
            .replace("[Son_Daughter]", son_daughter)
            .replace("[Father Name]", father_name)
            .replace("[Resident Of]", resident_of)
            .replace("[Fir_no]", fir_no)
            .replace("[Police Station]", police_station)
            .replace("[AI Generated Text]", ai_generated_text or "")
            .replace("[Advocate Name]", advocate_name)
            .replace("[Advocate Of]", advocate_of)
            .replace("[Day]", day)
            .replace("[Month]", month)
            .replace("[Year]", year)
            .replace("[AI Generated Affidavit]", ai_generated_affidavit or "")
        )

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=petitioner,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region PreArrest Bail Certificate


@app.route("PreArrestBailCertificate", methods=["GET"])
async def PreArrestBailCertificate(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.PreArrestBailCertificateForm),
        mimetype="application/json",
    )


@app.route("PreArrestBailCertificate", methods=["POST"])
async def PreArrestBailCertificate_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the JSON data from the request
        request_data = req.get_json()

        name = request_data.get("Name")
        fathers_name = request_data.get("Fathers_Name")
        address = request_data.get("Address")
        fir_no = request_data.get("Fir_No")
        date_of_fir = request_data.get("Date_Of_FIR")
        offence = request_data.get("Offence")
        order_date = request_data.get("Order_Date")
        bail_grant_date = request_data.get("Bail_Grant_Date")
        bail_expiry_date = request_data.get("Bail_Expiry_Date")
        son_daughter = request_data.get("Son_Daughter")
        judge_name = request_data.get("Judge_Name")
        AdvocateName = request_data.get("Advocate_Name")
        AdvocateOf = request_data.get("Advocate_Of")
        CourtName = request_data.get("Court_Name")

        # Replace placeholders in the template with actual data
        html = (
            AllTemplates.PreArrestBailCertificateDocument.replace("[Name]", name)
            .replace("[Son_Daughter]", son_daughter)
            .replace("[Father's Name]", fathers_name)
            .replace("[Address]", address)
            .replace("[Fir No]", fir_no)
            .replace("[Date Of FIR]", date_of_fir)
            .replace("[Offence]", offence)
            .replace("[Judge Name]", judge_name)
            .replace("[Order Date]", order_date)
            .replace("[Bail Grant Date]", bail_grant_date)
            .replace("[Bail Expiry Date]", bail_expiry_date)
            .replace("[Advocate Name]", AdvocateName)
            .replace("[Advocate Of]", AdvocateOf)
            .replace("[Court Name]", CourtName)
        )
        title = f"{name} vs The State"
        # Extract additional metadata
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        # Generate the application using the helper function
        helper.generate_applications(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=name,
            Title=title,
        )

        # Return the generated HTML as the response
        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        # Handle invalid input
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        # Log and handle unexpected errors
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Dissolution Of Marriage


@app.route("DissolutionOfMarriage", methods=["GET"])
async def DissolutionOfMarriage(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(AllTemplates.DissolutionOfMarriageForm),
        mimetype="application/json",
    )


@app.route("DissolutionOfMarriage", methods=["POST"])
async def DissolutionOfMarriage_post(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_data = req.get_json()

        CourtOF = request_data.get("CourtOF")

        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        timecreated = request_data.get("timecreated")
        category = request_data.get("Category")

        Plaintiff = request_data.get("Plaintiff")
        PlaintiffSonDaughter = request_data.get("PlaintiffSonDaughter")
        PlaintiffFatherName = request_data.get("PlaintiffFatherName")
        PlaintiffAddress = request_data.get("PlaintiffAddress")
        Defendant = request_data.get("Defendant")
        DefendantSonDaughter = request_data.get("DefendantSonDaughter")
        DefendantFatherName = request_data.get("DefendantFatherName")
        DefendantAddress = request_data.get("DefendantAddress")

        AiGeneratedText = request_data.get("AiGeneratedText")
        Day = request_data.get("Day")
        Month = request_data.get("Month")
        Year = request_data.get("Year")

        AdvocateName = request_data.get("AdvocateName")
        AdvocateOf = request_data.get("AdvocateOf")
        CourtName = request_data.get("CourtName")

        title = f"{Plaintiff} vs {Defendant}"

        html = (
            AllTemplates.DissolutionOfMarriageDocument.replace("[Court OF]", CourtOF)
            .replace("[Plaintiff]", Plaintiff)
            .replace("[Plaintiff Son/Daughter]", PlaintiffSonDaughter)
            .replace("[Plaintiff Father Name]", PlaintiffFatherName)
            .replace("[Plaintiff Address]", PlaintiffAddress)
            .replace("[Defendant]", Defendant)
            .replace("[Defendant Son/Daughter]", DefendantSonDaughter)
            .replace("[Defendant Father Name]", DefendantFatherName)
            .replace("[Defendant Address]", DefendantAddress)
            .replace("[Day]", Day)
            .replace("[Month]", Month)
            .replace("[Year]", Year)
            .replace("[Advocate Name]", AdvocateName)
            .replace("[Advocate of]", AdvocateOf)
            .replace("[Court Address]", CourtName)
        )

        info = (
            f"Plaintiff Name {Plaintiff} {PlaintiffSonDaughter} Father Name {PlaintiffFatherName} Resident of {PlaintiffAddress}"
            f"Defendant Name {Defendant} {DefendantSonDaughter} Father Name {DefendantFatherName} Resident of {DefendantAddress} "
            f"Additional Information: {AiGeneratedText}"
        )

        AiGeneratedText = OpenAI.get_dissolution_of_marriage(info)
        html = html.replace("[AI Generated]", AiGeneratedText)
        helper.generate_petitions(
            user_id=user_id,
            chat_id=chat_id,
            timecreated=timecreated,
            Data=request_data,
            Category=category,
            Document=html,
            ApplicantName=Plaintiff,
            Title=title,
        )

        return func.HttpResponse(body=html, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# endregion

# endregion


# region MongoDB Functions


# region Preview Petition


@app.route("PreviewPetition", methods=["POST"])
def PreviewPetition(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        document = helper.preview_petitions(user_id, chat_id)

        if document is None:
            return func.HttpResponse("Document not found", status_code=404)
        return func.HttpResponse(body=document, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region History Petition


@app.route("HistoryPetition", methods=["POST"])
def HistoryPetition(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        data = helper.get_history_petitions(user_id)

        return func.HttpResponse(body=json.dumps(data), mimetype="application/json")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Update Petition


@app.route("UpdatePetition", methods=["POST"])
def UpdatePetition(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        document = request_data.get("Document").replace("\n", "")
        timestamp = request_data.get("Timestamp")

        helper.update_petitions(user_id, chat_id, document, timestamp)

        return func.HttpResponse(body=document, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Delete Petition


@app.route("DeletePetition", methods=["POST"])
def DeletePetition(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")

        helper.delete_history_petitions(user_id, chat_id)

        return func.HttpResponse("Document deleted successfully")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Preview Application


@app.route("PreviewApplication", methods=["POST"])
def PreviewApplication(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        document = helper.preview_applications(user_id, chat_id)

        if document is None:
            return func.HttpResponse("Document not found", status_code=404)
        return func.HttpResponse(body=document, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region History Application


@app.route("HistoryApplication", methods=["POST"])
def HistoryApplication(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        data = helper.get_history_applications(user_id)

        return func.HttpResponse(body=json.dumps(data), mimetype="application/json")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Update Application


@app.route("UpdateApplication", methods=["POST"])
def UpdateApplication(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")
        document = request_data.get("Document").replace("\n", "")
        timestamp = request_data.get("Timestamp")

        helper.update_applications(user_id, chat_id, document, timestamp)

        return func.HttpResponse(body=document, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion

# region Delete Application


@app.route("DeleteApplication", methods=["POST"])
def DeleteApplication(req: func.HttpRequest):
    try:
        request_data = req.get_json()
        user_id = request_data.get("user_id")
        chat_id = request_data.get("chat_id")

        helper.delete_history_applications(user_id, chat_id)

        return func.HttpResponse("Document deleted successfully")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion


# endregion


# region ApplicationForConsolidationOfCasesInTheSameCourt
@app.route("ApplicationForConsolidationOfCasesInTheSameCourt", methods=["GET"])
async def application_for_consolidation_of_cases_in_the_same_court_get(
    req: func.HttpRequest,
) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(
            AllTemplates.ApplicationForConsolidationOfCasesInTheSameCourtForm
        ),
        mimetype="application/json",
    )


@app.route("/ApplicationForConsolidationOfCasesInTheSameCourt", methods=["POST"])
async def application_for_consolidation_of_cases_in_the_same_court_post(
    req: func.HttpRequest,
) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        # Replace placeholders in the template with extracted values
        html_template = (
            AllTemplates.ApplicationForConsolidationOfCasesInTheSameCourtDocument
        )

        # Extract form fields dynamically
        Court_Name = req_body.get("Court_Name")
        Plaintiff = request_data.get("Plaintiff")
        PlaintiffsNames = [x.get("PlaintiffName") for x in Plaintiff]
        PlaintiffString = "".join(
            AllTemplates.plaintiff_object.replace("[Plaintiff]", x.get("PlaintiffName"))
            .replace("[Plaintiff Son/Daughter]", x.get("PlaintiffSonDaughter"))
            .replace("[Plaintiff Father Name]", x.get("PlaintiffFatherName"))
            .replace("[Plaintiff Address]", x.get("PlaintiffAddress"))
            + "<br>"
            for x in Plaintiff
        )
        Defendant = request_data.get("Defendant")
        DefendantsNames = [x.get("DefendantName") for x in Defendant]
        DefendantString = "".join(
            AllTemplates.defendant_object.replace("[Defendant]", x.get("DefendantName"))
            .replace("[Defendant Son/Daughter]", x.get("DefendantSonDaughter"))
            .replace("[Defendant Father Name]", x.get("DefendantFatherName"))
            .replace("[Defendant Address]", x.get("DefendantAddress"))
            + "<br>"
            for x in Defendant
        )
        CaseGrounds = req_body.get("CaseGrounds")
        Advocates_Name = req_body.get("Advocates_Name")
        Office_Address = req_body.get("Office_Address")
        CourtAddress = req_body.get("CourtAddress")

        # Replace placeholders in the template with extracted values

        html_template = html_template.replace(
            "[Court_Name]", Court_Name if Court_Name else ""
        )
        html_template = html_template.replace(
            "[CaseGrounds]", CaseGrounds if CaseGrounds else ""
        )
        html_template = html_template.replace(
            "[Advocates_Name]", Advocates_Name if Advocates_Name else ""
        )
        html_template = html_template.replace(
            "[Office_Address]", Office_Address if Office_Address else ""
        )
        html_template = html_template.replace(
            "[CourtAddress]", CourtAddress if CourtAddress else ""
        )

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
            ApplicantName=req_body.get("Court_Name"),
            Title=title,
        )

        return func.HttpResponse(body=html_template, mimetype="text/html")

    except ValueError:
        return func.HttpResponse("Invalid input", status_code=400)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# endregion
