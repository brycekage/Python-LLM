import git
from tools.safehelp import is_path_safe
from tools.doctests import doctests


import git
from tools.safehelp import is_path_safe
from tools.doctests import doctests


def write_files(files, commit_message):
    """
    Writes multiple files and commits them all in a single commit.
    Runs doctests on any Python files written, and returns failure
    output so the caller can retry if needed.

    >>> import os
    >>> write_files(
    ...     [{'path': 'tests/a.txt', 'contents': 'hello'},
    ...      {'path': 'tests/b.txt', 'contents': 'world'}],
    ...     'test multi commit')
    'Files written and committed: tests/a.txt, tests/b.txt'
    >>> os.path.exists('tests/a.txt')
    True
    >>> os.path.exists('tests/b.txt')
    True
    >>> write_files([{'path': '/etc/passwd', 'contents': 'bad'}], 'bad')
    'Access denied: unsafe path'
    >>> write_files(
    ...     [{'path': '../secret.txt', 'contents': 'bad'}], 'bad')
    'Access denied: unsafe path'
    """
    for file in files:
        if not is_path_safe(file['path']):
            return 'Access denied: unsafe path'

    for file in files:
        with open(file['path'], 'w', encoding='utf-8') as f:
            f.write(file['contents'])

    doctest_results = []
    for file in files:
        if file['path'].endswith('.py'):
            result = doctests(file['path'])
            doctest_results.append(result)

    repo = git.Repo('.')
    paths = [file['path'] for file in files]
    repo.index.add(paths)
    repo.index.commit(f'[docchat] {commit_message}')

    result = 'Files written and committed: ' + ', '.join(paths)
    if doctest_results:
        joined = '\n\n'.join(doctest_results)
        result += f'\n\nDoctest results:\n{joined}'
    return result


SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_files",
        "description": (
            "Write multiple files and commit them in a single commit. "
            "Runs doctests on any Python files."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file to write."
                            },
                            "contents": {
                                "type": "string",
                                "description": "Contents to write to the file."
                            },
                        },
                        "required": ["path", "contents"],
                    },
                    "description": "List of files to write.",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message."
                },
            },
            "required": ["files", "commit_message"],
        },
    },
}
