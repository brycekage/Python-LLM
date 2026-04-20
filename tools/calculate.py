def calculate(expression) -> str:
    """
    Evaluates a given mathematical expression.
    >>> calculate("6 + 7")
    '13'

    >>> calculate("6 * 7")
    '42'

    >>> calculate("60 / 6")
    '10.0'

    >>> calculate("67 / 0")
    'Error: division by zero'
    """
    try:
        return str(eval(str(expression), {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {e}"
