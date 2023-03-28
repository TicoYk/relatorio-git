import requests
import json
import os
from datetime import datetime

userName = "git config user.name"
urlGitLab = "https://rota.gitlab.com/api/v4/projects/"
apiToken = "API-TOKEN"
since = "yyyy-MM-dd"
projects = [
    {"nome": "nome-projeto", "id": "id-projeto"},
]

paramsCommit = {
    "since": since + "T00:00:00Z",
    "all" : "true",
    "per_page": "2000"
}
paramsDiff = {
    "with_stats": "true"
}
headers = {
    "PRIVATE-TOKEN": apiToken,
}

dir_path = "./relatorios"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

for project in projects:
    url = urlGitLab+project["id"]+"/repository/commits"
    response = requests.get(url, params=paramsCommit, headers=headers, verify=False)
    commits = response.json()
    artifacts = {}
    my_commits = []
    for commit in commits:
        if commit["author_name"] == userName:
            my_commits.append(commit)
    for commit in my_commits:
        response2 = requests.get(url+"/"+commit["id"]+"/diff", params=paramsDiff, headers=headers, verify=False)
        diffs = response2.json()
        for diff in diffs:
            data_datetime = datetime.fromisoformat(commit["created_at"].replace("Z", "+00:00"))
            data_formatada = data_datetime.strftime("%d-%m-%Y")
            artifact = {
                "author": commit["author_name"],
                "hash": commit["id"],
                "arquivo": project["nome"] + "/" + diff["new_path"] + "#" + commit["short_id"],
                "title": commit["title"],
                "isCreated": diff["new_file"],
                "repository": project["nome"],
                "createdAt": data_formatada
            }
            if commit["id"] in artifacts:
                artifacts[commit["id"]].append(artifact)
            else:
                artifacts[commit["id"]] = [artifact]

    with open(dir_path + "/" + project["nome"] + "-commits.json", "w", encoding="utf-8") as f:
        json.dump(artifacts, f, ensure_ascii=False, indent=4)

print("Dados salvos com sucesso!")