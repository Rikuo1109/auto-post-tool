from github import Github


def push_image(file_path, file_name, commit_message="", branch="main"):
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
    g = Github("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")
    repo = g.get_repo("tri218138/Horus-Auto-Post-Images")
    repo.create_file(file_name, commit_message, bytes(image_data), branch)
