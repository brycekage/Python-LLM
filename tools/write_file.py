from tools.write_files import write_files


def write_file(path, contents, commit_message):
    """
    Writes contents to a file, commits it, and runs doctests
    if it's a Python file.

    >>> import os
    >>> write_file('testCases/test_write.txt', 'hello world', 'test commit')
    'Files written and committed: testCases/test_write.txt'
    >>> os.path.exists('testCases/test_write.txt')
    True
    >>> write_file('/unsafe/psadasd', 'bad', 'bad commit')
    'Access denied: unsafe path'
    >>> write_file('../veryUnsafe.txt', 'bad', 'bad commit')
    'Access denied: unsafe path'
    """
    return write_files(
        [{'path': path, 'contents': contents}], commit_message
    )


SCHEMA = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Write contents to a file and commit it. "
            "Runs doctests if it's a Python file."
        ),
        "parameters": {
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
                "commit_message": {
                    "type": "string",
                    "description": "Git commit message."
                },
            },
            "required": ["path", "contents", "commit_message"],
        },
    },
}
