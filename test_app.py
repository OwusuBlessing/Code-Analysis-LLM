from fastapi import FastAPI, HTTPException, Form,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import httpx
import os
import importlib
from github_fetch.fetch_file_contents import fetch_and_save_contents
from github_fetch.fetch_repos import fetch_repo_names
from config import DOWNLOAD_REPO_DIRECTORY
from utils.common import delete_and_create_folder
from openai_st.stage01_extract_indivdual_code_file import read_code_file,create_individual_document,process_folder_for_individual_docs
from openai_st.stage02_generate_review_from_prompt import get_review
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

github_login_client_id=os.getenv("GITHUB_CLIENT_ID")
github_login_client_secret = os.getenv("GITHUB_SECRET_KEY")
token_store = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_login_client_id}', status_code=302)

@app.get("/callback", response_class=HTMLResponse)
async def callback_page(code:str,request: Request):
    params = {
        'client_id': github_login_client_id,
        'client_secret': github_login_client_secret,
        'code': code
    }
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        # Exchange code for access token
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)

    response_json = response.json()
    access_token = response_json['access_token']

    # Store the new token
    token_store['access_token'] = access_token

    # get repo names and repo owner
    repo_names, owner = await fetch_repo_names(access_token)

    token_store['owner'] = owner

    return templates.TemplateResponse("callback.html", {"request": request, "repo_names": repo_names})

@app.post("/download-repo", response_class=HTMLResponse)
async def process_selected_repo(request: Request,selected_repo: str = Form(...)):
    access_token = token_store['access_token']

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    headers = {'Authorization': f'token {access_token}'}
    repo_url = f"https://api.github.com/repos/{token_store['owner']}/{selected_repo}/contents"

    # Local directory to save files
    delete_and_create_folder(DOWNLOAD_REPO_DIRECTORY)

    await fetch_and_save_contents(repo_url, headers, save_path=DOWNLOAD_REPO_DIRECTORY)

    # Data to be passed to the template
    template_data = {"selected_repo": selected_repo, "download_directory": DOWNLOAD_REPO_DIRECTORY}

    # Render the HTML template using Jinja2
    return templates.TemplateResponse("downloaded_repo.html", {"request": request, **template_data})

@app.get("/review", response_class=HTMLResponse)
async def review(request:Request):
    docs = process_folder_for_individual_docs(DOWNLOAD_REPO_DIRECTORY)
    x = [docs[1]]
    reviews = get_review(all_docs=x)
    return templates.TemplateResponse("review.html", {"request": request, "reviews": reviews})

