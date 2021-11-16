import json
import requests

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



def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-p','--project', help='The github project', required=True)
    parser.add_argument('-r','--repo', help='The github repository', required=True)
    parser.add_argument('-t','--token', help='The github token', required=True)

    args = parser.parse_args()
    head_branch = "update-schemas"
    process = subprocess.Popen(['git', 'checkout -b', head_branch], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

    create_pull_request(
        args['project'], # project_name
        args['repo'], # repo_name
        "My pull request title", # title
        "My pull request description", # description
        head_branch, # head_branch
        "main", # base_branch
        args['token'], # git_token
    )

if __name__ == "__main__":
    main()