def calculate(expression):
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)  # Use safe evaluation in production
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})