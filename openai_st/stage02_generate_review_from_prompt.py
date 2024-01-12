from langchain_community.llms import openai
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from config import DOWNLOAD_REPO_DIRECTORY,CODE_EXTENSIONS
from langchain_core.documents import Document


load_dotenv()
key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=key)

def get_review(all_docs):
    response = []
    for doc in all_docs:
        file_name = doc["file_name"]
        folder_path = doc["folder_path"]
        content = doc["content"]

        prompt = ChatPromptTemplate.from_messages([
            ("system", f'''You are world class technical code reviewer and you are to review the code file name {file_name} present in folder: {folder_path}, the code content will be provided next As an expert code reviewer,also start with the filename and the folder the file is found please evaluate the provided code across four key areas and structure your output developer can easily understand:
         
        1. Code Improvement: Suggest enhancements for better quality and maintainability.
        2. Code Optimization: Identify and improve areas for increased efficiency.
        3. Test Case Suggestions: Propose additional test cases for comprehensive coverage.
        4. Bug Identification: Examine and suggest fixes for potential bugs.
        '''),
            ("user", "{input}")
        ])

        chain = prompt | llm

        result = chain.invoke({"input": f"Code content : {content}"}).content
        response.append(result)
        #response[f'Code Review for {file_name} found in folder:{folder_path}'] = result
        return response




