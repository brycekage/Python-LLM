from tools.safehelp import is_path_safe
import glob


def ls(path='.'):
    # List files in directory

    """
    Returns a sorted space-separated string of 
    filenames in the given directory.

    >>> 'chat.py' in ls()
    True

    >>> ls('testCases')
    'testCases/testV1.txt'

    >>> ls('/etc')
    'Access denied: unsafe path'

    >>> ls('../outside')
    'Access denied: unsafe path'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    names = sorted(f.replace('\\', '/') for f in glob.glob(f'{path}/*'))
    return ' '.join(names)
