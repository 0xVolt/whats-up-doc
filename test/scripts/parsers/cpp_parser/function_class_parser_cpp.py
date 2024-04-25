import clang.cindex

def extract_classes(cursor):
    classes = []

    for node in cursor.get_children():
        if node.kind == clang.cindex.CursorKind.CLASS_DECL:
            class_name = node.spelling
            class_body = node.extent.contents
            
            classes.append((class_name, class_body))

        classes.extend(extract_classes(node))

    return classes

def parse_cpp_file(file_path):
    index = clang.cindex.Index.create()
    tu = index.parse(file_path)

    return extract_classes(tu.cursor)

# Example usage:
if __name__ == "__main__":
    file_path = r"C:\Users\deshi\Code\whats-up-doc\src\test_doc_scripts\test_functions_advanced.cpp"
    classes = parse_cpp_file(file_path)

    if classes:
        for class_name, class_body in classes:
            print("Class Name:", class_name)
            print("Class Body:", class_body)
            print("-------------------")
    else:
        print("No classes found in the file.")
