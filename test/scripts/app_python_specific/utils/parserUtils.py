import ast
import json
import re
import textwrap

def extractFunctionsAsList(path, language):
    listOfFunctions = []

    with open(path, 'r') as file:
        content = file.read()
        tree = ast.parse(content, filename=path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                body = ast.get_source_segment(content, node)

                function_data = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'defaults': [ast.get_source_segment(content, arg) for arg in node.args.defaults],
                    'body': body,
                    'return': ast.get_source_segment(content, node.returns) if node.returns else None
                }

                # Collect functions' meta data
                listOfFunctions.append(function_data)

    listOfFunctionBodies = [function['body'] for function in listOfFunctions]

    return listOfFunctionBodies