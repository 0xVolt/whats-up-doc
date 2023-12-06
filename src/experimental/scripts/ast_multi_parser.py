import ast
import os


# Note: Python match-case statements are only supported in 3.10+
def parseNode(node, path):
    if isinstance(node, ast.Module):
        return parseModule(node, path)
    elif isinstance(node, ast.Expression):
        return parseModule(node, path)
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return parseFunctionOrClass(node, path)
    elif isinstance(node, ast.If):
        return parseIf(node, path)
    elif isinstance(node, ast.While):
        return parseWhile(node, path)
    elif isinstance(node, ast.Import):
        return parseImport(node, path)


def parseModule():
    pass


def parseExpression():
    pass


def parseFunctionOrClass():
    pass


def parseIf():
    pass


def parseFor():
    pass


def parseWhile():
    pass


def parseImport():
    pass