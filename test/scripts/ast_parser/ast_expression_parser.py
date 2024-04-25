import ast
import json


def parse_assignments(file_path):
    assignments = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        tree = ast.parse("".join(lines), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    start_line = node.lineno
                    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                    line_of_code = "".join(lines[start_line - 1:end_line])

                    # Replace consecutive spaces with a single tab character
                    line_of_code = line_of_code.replace('    ', '\t')

                    attributes = {
                        'target': target.id if isinstance(target, ast.Name) else ast.dump(target),
                        'value': ast.dump(node.value),
                        'line': node.lineno,
                        'line_of_code': line_of_code.strip()
                    }

                    assignments.append(attributes)

    return assignments


file_path = r"C:\Users\deshi\Code\whats-up-doc\test\scripts\test_response.py"
result = parse_assignments(file_path)

print(json.dumps(result, indent=2))