import os
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.chat_models import AzureChatOpenAI


# region Define Model

os.environ["AZURE_OPENAI_ENDPOINT"] = (
    "https://rg-lawgpt-openai-gpt4o-mini.openai.azure.com/openai/deployments/RG-LAWGPT-OPENAI-GPT4o-mini/chat/completions?api-version=2023-03-15-preview"
)

os.environ["AZURE_OPENAI_API_KEY"] = "7d4c688140aa4e588d5a62508c177e5c"

os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"


AZURE_CHAT_MODEL_DEPLOYMENT: str = "RG-LAWGPT-OPENAI-GPT4o-mini"

temperature = 0.4
max_tokens = 800

llm = AzureChatOpenAI(
    deployment_name=AZURE_CHAT_MODEL_DEPLOYMENT,
    temperature=temperature,
    max_tokens=max_tokens,
)


# endregion


prompts_folder = "./models/Prompts/"


def get_legal_notice(info: str):
    pretext = open(f"{prompts_folder}LegalNoticePrompt.txt").read()
    response = llm.invoke(pretext + ":" + info)
    return response.content


def get_legal_cirtificate(info: str):
    promtEngineerd = open(f"{prompts_folder}LegalCertificatePrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_superdari_details(info: str):
    promtEngineerd = open(f"{prompts_folder}SuperdariPrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_Early_Hearing_Subject(info: str):
    promtEngineerd = open(f"{prompts_folder}EarlyHearingSubjectPrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_Early_Hearing(info: str):
    promtEngineerd = open(f"{prompts_folder}EarlyHearingPrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_dissolution_of_marriage(info: str):
    promtEngineerd = open(f"{prompts_folder}DisolutionOfMarriagePrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def generate_affidavit(info: str):
    promtEngineerd = open(f"{prompts_folder}AffidavitPrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_pre_arrest_bail_application(info: str):
    promtEngineerd = open(f"{prompts_folder}PreArrestBailApplicationPrompt.txt").read()
    response = llm.invoke(promtEngineerd + ":" + info)
    return response.content


def get_ApplicationForConsolidationOfCasesInTheSameCourtGrounds_Prompt(info: str):
    promtEngineered = open(f"{prompts_folder}/ApplicationForConsolidationOfCasesInTheSameCourtGrounds.txt").read()
    system_prompt = open(f"{prompts_folder}/ApplicationForConsolidationOfCasesInTheSameCourtGSystemPrompt.txt").read()
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

    
        