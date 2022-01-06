
def calculate(number1, number2, operator):
    if operator == '+':
        result = number1 + number2
        return result
    
    elif operator == '-':
        result = number1 - number2
        return result
    
    elif operator == '*':
        result = number1 * number2
        return result
    
    elif operator == "/":
        result = number1 / number2
        return result
    
    else:
        return None
