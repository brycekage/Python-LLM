import os
import glob
import git
from tools.safehelp import is_path_safe


def rm(path):
    """
    Deletes files matching the given path or glob and commits the removal.

    >>> open('tests/tempRm.txt', 'w').close()
    >>> rm('tests/tempRm.txt')
    'Removed and committed: tests/tempRm.txt'
    >>> import os
    >>> os.path.exists('tests/tempRm.txt')
    False
    >>> rm('/unsafe/veryUnsafe')
    'Access denied: unsafe path'
    >>> rm('../unsafe.txt')
    'Access denied: unsafe path'
    >>> rm('tests/huh.txt')
    'No files found: tests/huh.txt'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'

    matches = [f.replace('\\', '/') for f in glob.glob(path)]
    if not matches:
        return f'No files found: {path}'

    repo = git.Repo('.')
    for filepath in matches:
        os.remove(filepath)

    try:
        repo.index.remove(matches)
    except Exception:
        pass
    repo.index.commit(f'[docchat] rm {path}')

    return 'Removed and committed: ' + ', '.join(matches)


SCHEMA = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": "Delete files matching a path or glob "
        "and commit the removal.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path or glob to delete."}
            },
            "required": ["path"],
        },
    },
}
