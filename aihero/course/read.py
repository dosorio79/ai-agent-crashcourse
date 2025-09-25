import io
import zipfile
import requests
import frontmatter

def read_repo_data(repo_owner, repo_name, prefix):
    """
    Downloads and extracts Markdown (.md, .mdx) files from a GitHub repository's main branch zip archive,
    parses their frontmatter, and returns a list of dictionaries containing the parsed data and filenames.

    Args:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        prefix (str): The URL prefix to construct the download link (e.g., "https://github.com").

    Returns:
        list: A list of dictionaries, each containing the parsed frontmatter data and filename of a Markdown file.

    Raises:
        Exception: If the repository cannot be downloaded (non-200 HTTP response).
    """

    url = f"{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/main"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to download repository: {response.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(response.content))
    # Iterate through each file in the zip
    for file_info in zf.infolist():
        filename = file_info.filename.lower()
        # Get md or mdx files only
        if not (filename.endswith('.md') or filename.endswith('.mdx')):
            continue
        try:
            # Read and parse each file
            with zf.open(file_info) as f_in:
                content = f_in.read()
                post = frontmatter.loads(content)
                data = post.to_dict()
                data['filename'] = filename
                repository_data.append(data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    zf.close()
    return repository_data
