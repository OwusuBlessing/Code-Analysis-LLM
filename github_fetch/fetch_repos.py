import httpx

async def fetch_repo_names(access_token):
    """
    Fetches the names of repositories owned by the authenticated user.

    Parameters:
    - access_token (str): The GitHub access token.

    Returns:
    - list: A list of repository names.
    """
    # Get user information
    async with httpx.AsyncClient() as client:
        user_info_headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = await client.get('https://api.github.com/user', headers=user_info_headers)

    user_info = user_info_response.json()

    # Get user repositories
    async with httpx.AsyncClient() as client:
        repos_headers = {'Authorization': f'Bearer {access_token}'}
        repos_response = await client.get(f'https://api.github.com/users/{user_info["login"]}/repos', headers=repos_headers)

    repos = repos_response.json()

    # Update repo owner username
    owner = repos[0]['owner']['login']

    # Extract repository names
    repo_names = [repo["name"] for repo in repos]

    return repo_names,owner

