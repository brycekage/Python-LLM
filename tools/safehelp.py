def is_path_safe(path):
    # Helper function to check if a file path is safe

    """
    Returns True if path is relative and contains no directory traversal.

    >>> is_path_safe('.')
    True
    >>> is_path_safe('tools/ls.py')
    True
    >>> is_path_safe('/etc/passwd')
    False
    >>> is_path_safe('../secret.txt')
    False
    >>> is_path_safe('foo/../../etc/passwd')
    False
    """
    if path.startswith('/'):
        return False
    if '..' in path.split('/'):
        return False
    return True
