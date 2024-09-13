SuitForSpecificPerformanceDocument = """ 
<style>
    .container-section {
        font-family: 'Times New Roman', Times, serif;
        margin: 40px;

    }

    h1 {
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
    }

    h2 {
        font-size: 18px;
        margin-bottom: 10px;
    }

    .address {
        margin-bottom: 20px;
    }

    .content {
        margin-bottom: 20px;
    }

    .content ol {
        margin: 0;
        padding-left: 40px;
    }

    .content li {
        margin-bottom: 10px;
    }

    .prayer {
        margin-top: 20px;
    }

    .verification {
        margin-top: 30px;
        font-style: italic;
    }

    .signature {
        margin-top: 40px;
        text-align: right;
    }

    .signature p {
        margin: 5px 0;
    }
</style>

<div class="container-section">
    <h1 style="margin-bottom: 60px;">
        IN THE COURT OF SENIOR CIVIL JUDGE, LAHORE
    </h1>

    <p style="text-align: center; font-size: 14pt; margin-bottom: 30px; margin-top: 15px;">Civil Suit
        No.[Civil Suit] </p>
    <div class="section">
        <div class="address">
            [Plaintiff]
            <p style="text-align: right;"><strong>Plaintiff</strong></p>
        </div>

        <div class="address">
            <p style="text-align: center;"><strong>Versus</strong></p>
        </div>

        <div class="address">
            [Defendant]
            <p style="text-align: right;"><strong>Defendant</strong></p>
        </div>
    </div>

    <div class="section">
        <p style="margin-left: 40px; margin-right: 40px;"><strong>[Title].</strong></p>

        <p><strong>Respectfully Sheweth:</strong></p>

        [Grounds]
    </div>

    <div class="prayer">
        PRAYER:
    </div>

    [Prayers]

    <div class="signature">
        <p style="text-align: right;"><strong>Plaintiff</strong></p>
        <h3 style="text-align: center;">Through:</h3>
        <p><strong>[Advocate Name]</strong></p>
        <p>[Advocate of]</p>
        <p>[Court Address]</p>
    </div>
</div>


 """


SuitForSpecificPerformanceForm = {'id': 'SuitForSpecificPerformance', 'fields': [{'label': 'Civil Suit Number', 'id': 'CivilSuitNumber', 'name': 'CivilSuitNumber', 'type': 'text', 'required': True}, {'label': 'Plaintiff Information', 'id': 'Plaintiff', 'name': 'Plaintiff', 'type': 'list', 'required': True, 'fields': [{'label': "Plaintiff's Full Name", 'id': 'PlaintiffName', 'name': 'PlaintiffName', 'type': 'text', 'required': True}, {'label': "Plaintiff's Gender", 'id': 'PlaintiffGender', 'name': 'PlaintiffGender', 'type': 'radio', 'options': [{'label': 'Son', 'value': 'Son'}, {'label': 'Daughter', 'value': 'Daughter'}], 'required': True}, {'label': "Plaintiff's Father's Name", 'id': 'PlaintiffFatherName', 'name': 'PlaintiffFatherName', 'type': 'text', 'required': False}, {'label': "Plaintiff's Address", 'id': 'PlaintiffAddress', 'name': 'PlaintiffAddress', 'type': 'textarea', 'required': False}]}, {'label': 'Defendant Information', 'id': 'Defendant', 'name': 'Defendant', 'type': 'list', 'required': True, 'fields': [{'label': "Defendant's Full Name", 'id': 'DefendantName', 'name': 'DefendantName', 'type': 'text', 'required': True}, {'label': "Defendant's Gender", 'id': 'DefendantGender', 'name': 'DefendantGender', 'type': 'radio', 'options': [{'label': 'Son', 'value': 'Son'}, {'label': 'Daughter', 'value': 'Daughter'}], 'required': True}, {'label': "Defendant's Father's Name", 'id': 'DefendantFatherName', 'name': 'DefendantFatherName', 'type': 'text', 'required': False}, {'label': "Defendant's Address", 'id': 'DefendantAddress', 'name': 'DefendantAddress', 'type': 'textarea', 'required': False}]}, {'label': 'Case Title', 'id': 'CaseTitle', 'name': 'CaseTitle', 'type': 'text', 'required': True}, {'label': 'Grounds of the Case', 'id': 'CaseGrounds', 'name': 'CaseGrounds', 'type': 'textarea', 'required': True}, {'label': 'Prayers/Reliefs Sought', 'id': 'CasePrayers', 'name': 'CasePrayers', 'type': 'textarea', 'required': True}, {'label': "Advocate's Full Name", 'id': 'AdvocateName', 'name': 'AdvocateName', 'type': 'text', 'required': True}, {'label': 'Court Address', 'id': 'CourtAddress', 'name': 'CourtAddress', 'type': 'text', 'required': False}]}