# Note: This file cannot be called ast.py since that raises a circular dependency

import ast

expression = "x * pow(10, 4)"

print(ast.dump(ast.parse(expression, mode='eval')))