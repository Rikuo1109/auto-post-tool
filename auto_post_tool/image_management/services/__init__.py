from github import Github
from django.conf import settings


def push_image(file_path, file_name, commit_message="", branch="main"):
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
    g = Github(settings.GITHUB_TOKEN)
    repo = g.get_repo(settings.GITHUB_REPO)
    repo.create_file(file_name, commit_message, bytes(image_data), branch)
