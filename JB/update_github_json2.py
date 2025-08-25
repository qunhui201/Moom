import json
import requests
import base64
import urllib.parse
import os

# GitHub configuration
GITHUB_TOKEN = os.getenv('ACTIONS_TOKEN')  # Use GITHUB_TOKEN
REPO_OWNER = 'qunhui201'
REPO_NAME = 'Moom'
FILE_PATH = 'tv/XYQHiker/黄色仓库.json'  # Verify this path
BRANCH_NAME = 'main'
COMMIT_MESSAGE = 'Update JSON links'
VALID_LINKS_FILE_PATH = 'JB/valid_links2.txt'

# URL encode file path
encoded_file_path = urllib.parse.quote(FILE_PATH)

# Download valid_links2.txt
def download_valid_links():
    url = f'https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH_NAME}/{VALID_LINKS_FILE_PATH}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading valid_links2.txt: {e}")
        return []

# Read JSON file locally
def download_json_file():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

# Replace fixed links in JSON
def replace_fixed_links_in_json(data, new_link):
    data['首页推荐链接'] = new_link
    data['首页片单链接加前缀'] = new_link
    data['分类链接'] = new_link + '/vodtype/{cateId}-{catePg}.html'
    data['分类片单链接加前缀'] = new_link
    data['搜索链接'] = new_link + '/index.php/ajax/suggest?mid=1&wd={wd}'
    data['搜索片单链接加前缀'] = new_link + '/vodplay/'
    return data

# Get file SHA
def get_file_sha(repo_owner, repo_name, file_path, branch):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    print(f"Requesting SHA for URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        file_info = response.json()
        print(f"File info: {file_info}")
        return file_info['sha']
    except requests.exceptions.RequestException as e:
        print(f"Failed to get file SHA: {e}")
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

# Update GitHub file
def update_github_file(repo_owner, repo_name, file_path, new_data, sha, branch, commit_message):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    formatted_content = json.dumps(new_data, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(formatted_content.encode('utf-8')).decode('utf-8')
    data = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha,
        "branch": branch
    }
    try:
        response = requests.put(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        print("File updated successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error updating file: {e}")

def main():
    # Download valid_links2.txt
    new_links = download_valid_links()
    if not new_links:
        print("No valid links available.")
        return

    print("=== Updated valid_links2.txt content ===")
    print("\n".join(new_links))

    # Read JSON file
    data = download_json_file()
    if data is None:
        return

    print("Original JSON data:")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    # Replace links
    updated_data = replace_fixed_links_in_json(data, new_links[0])

    print("Updated JSON data:")
    print(json.dumps(updated_data, ensure_ascii=False, indent=2))

    # Get file SHA
    sha = get_file_sha(REPO_OWNER, REPO_NAME, encoded_file_path, BRANCH_NAME)
    if sha is None:
        return

    # Update JSON file
    update_github_file(REPO_OWNER, REPO_NAME, encoded_file_path, updated_data, sha, BRANCH_NAME, COMMIT_MESSAGE)

if __name__ == "__main__":
    main()
