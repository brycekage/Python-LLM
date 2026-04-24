import subprocess
from tools.safety import is_path_safe


def doctests(path):
    """
    Runs doctests with verbose output on the given file and returns the result

    >>> 'calculate' in doctests('tools/calculate.py')
    True

    >>> doctests('../prettyUnsafe.py')
    'Access denied: unsafe path'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    result = subprocess.run(
        ['python', '-m', 'doctest', '-v', path],
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


SCHEMA = {
    "type": "function",
    "function": {
        "name": "doctests",
        "description": "Run doctests with verbose output on a file and return the results.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Path to the Python file to test."}
            },
            "required": ["path"],
        },
    },
}
