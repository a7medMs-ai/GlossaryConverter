from github import Github
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)
user = g.get_user()

def create_repo_if_not_exists(repo_name):
    try:
        user.get_repo(repo_name)
    except:
        user.create_repo(repo_name, private=False)

def upload_to_github(file_path, file_name, repo_name):
    repo = user.get_repo(repo_name)
    with open(file_path, "rb") as f:
        content = f.read()
    try:
        repo.get_contents(file_name)
        repo.update_file(file_name, "تحديث الملف", content, repo.get_contents(file_name).sha)
    except:
        repo.create_file(file_name, "إضافة ملف جديد", content)
    return f"https://github.com/{user.login}/{repo_name}/blob/main/{file_name}"
