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

SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": (
            "Evaluate a mathematical expression. "
            "Always pass the raw expression as a string (e.g. '6 * 7'), "
            "never a pre-computed number."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "The math expression to evaluate as a string, "
                        "e.g. '6 * 7'."
                    )
                }
            },
            "required": ["expression"],
        },
    },
},