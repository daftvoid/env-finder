import os

import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {"Authorization": f"token {os.getenv("GITHUB_PAT")}"}

def search_repos(searchstring: str, page: int = 1, per_page: int = 1):
    url = f"https://api.github.com/search/repositories?q={searchstring}&page={page}&per_page={per_page}"

    return requests.get(url, headers=HEADERS).json()

def get_files(repo_name):
    print(HEADERS)

    repo_res = requests.get(f"https://api.github.com/repos/{repo_name}", headers=HEADERS)

    print(repo_res.status_code)
    print(repo_res.json())

    if repo_res.status_code != 200: return []

    repo_data = repo_res.json()
    branch = repo_data.get("default_branch", "main")
    html_url = repo_data.get("html_url")

    tree_url = f"https://api.github.com/repos/{repo_name}/git/trees/{branch}?recursive=1"
    tree_res = requests.get(tree_url, headers=HEADERS)

    print(tree_res.status_code)

    if tree_res.status_code != 200: return []

    return tree_res.json()["tree"]

    """
    links = []
    for item in tree_res.json().get("tree", []):
        path = item["path"]
        if path.endswith(".env") or ".env." in path:
            # Construct the clickable browser link
            file_link = f"{html_url}/blob/{branch}/{path}"
            links.append(file_link)
    """

