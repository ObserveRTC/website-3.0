import argparse
import json
import requests
import subprocess
from git import Repo

def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://github.com/api/v3/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))

    if not r.ok:
        print("Request Failed: {0}".format(r.text))
        raise

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-p','--project', help='The github project', required=True)
    parser.add_argument('-r','--repo', help='The github repository', required=True)
    parser.add_argument('-t','--token', help='The github token', required=True)

    args = parser.parse_args()
    
    repo = Repo("../.git")    
    new_branch = 'your_new_branch'
    current = repo.create_head(new_branch)
    current.checkout()
    
    master = repo.heads.main
    repo.git.pull('origin', master)
    #creating file
    if repo.index.diff(None) or repo.untracked_files:
        repo.git.add(A=True)
        repo.git.commit(m='msg')
        repo.git.push('--set-upstream', 'origin', current)
        print('git push')
    else:
        print('no changes')

    
    # process = subprocess.Popen(['git', 'checkout -b', head_branch], 
    #                        stdout=subprocess.PIPE,
    #                        universal_newlines=True)

    # create_pull_request(
    #     args['project'], # project_name
    #     args['repo'], # repo_name
    #     "My pull request title", # title
    #     "My pull request description", # description
    #     new_branch_name, # head_branch
    #     "main", # base_branch
    #     args['token'], # git_token
    # )

if __name__ == "__main__":
    main()