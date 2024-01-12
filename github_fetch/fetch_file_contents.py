import os
import httpx
from fastapi import HTTPException
from config import CODE_EXTENSIONS

async def fetch_and_save_contents(url, headers, save_path, client=None):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching repository contents")

    for item in response.json():
        path = os.path.join(save_path, item['path'])
        if item['type'] == 'dir':
            os.makedirs(path, exist_ok=True)
            # Recursively fetch and save contents for subdirectories
            await fetch_and_save_contents(item['url'], headers, path, client=client)
        elif any(item['name'].endswith(ext) for ext in CODE_EXTENSIONS):
            # Ensure the parent directories exist before writing the file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            async with httpx.AsyncClient() as new_client:
                file_response = await new_client.get(item['download_url'], headers=headers)

            # Open the file in binary mode for non-text files
            with open(path, 'wb') as file:
                file.write(file_response.content)
