def ls(folder=None)
    '''
    This function behaves just like the ls pro gram in shell

    >>> ls()
    'chat.py  htmlcov  __pycache__  requirements  tools  'venv'

    >>> ls('tools')
    'tools/__pycache__ tools/ls.py'
    '''

    if folder:
        result = ''
        # folder + '/*' ==> tools/*
        for path in sorted.glob.glob(folder + '/*'):
            result += path + ' '
        return result
    else:
        #handle this case