import subprocess


def pip_install(library_name):
    """
    Installs a Python library using pip3.

    >>> pip_install('requests')
    'Successfully installed requests'
    >>> pip_install('this-library-does-not-exist-xyz123')  # doctest: +ELLIPSIS
    'Error: ...'
    """
    try:
        result = subprocess.run(
            ['pip3', 'install', library_name],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return f'Successfully installed {library_name}'
        return f'Error: {result.stderr.strip()}'
    except subprocess.TimeoutExpired:
        return f'Error: installation of {library_name} timed out'
    except Exception as e:
        return f'Error: {e}'


SCHEMA = {
    "type": "function",
    "function": {
        "name": "pip_install",
        "description": (
            "Install a Python library using pip3. "
            "WARNING: Only install trusted libraries, as pip packages "
            "can contain arbitrary code."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "library_name": {
                    "type": "string",
                    "description": "The name of the library to install."
                }
            },
            "required": ["library_name"],
        },
    },
}
