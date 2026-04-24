from tools.safehelp import is_path_safe


def cat(path):
    """
    Reads and returns content of file
    >>> # Normal Read
    >>> cat('tests/testV1.txt')
    'This is a doctest for the cat tool'

    >>> # File Not Found
    >>> cat('nonexistentFile.txt')
    'Error: file not found'

    >>> # Unsafe Path
    >>> cat('/unsafe/veryUnsafe.txt')
    'Access denied: unsafe path'

    >>> # Unsafe Path with Traversal
    >>> cat('../superDuperUnsafe.txt')
    'Access denied: unsafe path'

    >>> # UTF-16 File
    >>> import os
    >>> with open('tests/_tmp.bin', 'wb') as f:
    ...     _ = f.write(bytes([0x80, 0x81]))
    >>> cat('tests/_tmp.bin')
    'Error: could not decode file'
    >>> os.unlink('tests/_tmp.bin')
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'Error: file not found'
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-16') as f:
                return f.read()
        except Exception:
            return 'Error: could not decode file'

SCHEMA = {
    "type": "function",
    "function": {
        "name": "cat",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File to read."}
            },
            "required": ["path"],
        },
    },
},