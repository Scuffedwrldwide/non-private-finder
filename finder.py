import re
import os

# Path to the project directory to search for Java files
# Assumes this script is in a separate folder to the project directory, but in the same parent directory
project_directory = '../'

def find_non_private(java_code):
    """
    Finds non-private attributes in Java code.

    Args:
        java_code (str): The Java code to search for attributes.
    Returns:
        list: A list of tuples containing modifier, data type, attribute name, and line number.
    """
    # Regular expression to match non-private attributes
    pattern = r'(public|protected|final|static|volatile|transient)\s+(\w+)\s+(\w+)\s*;'
    lines = java_code.split('\n')

    non_private_attributes = []

    # Iterate through lines and extract attribute information
    for i, line in enumerate(lines, start=1):
        match = re.search(pattern, line)
        if match:
            modifier, data_type, attribute_name = match.groups()
            non_private_attributes.append((modifier, data_type, attribute_name, i))

    return non_private_attributes

def process_java_file(file_path):
    """
    Processes a Java file to find its class name and print non-private attributes.

    Args:
        file_path (str): The path of the Java file to process.

    Returns:
        None
    """
    with open(file_path, 'r') as file:
        java_code = file.read()
        relative_path = os.path.relpath(file_path, project_directory)

        class_name_match = re.search(r'class (\w+)', java_code)
        if class_name_match:
            class_name = class_name_match.group(1)
            non_private_attributes = find_non_private(java_code)

            print(f"Class: {class_name} @ {relative_path} ({len(non_private_attributes)})")
            for attribute in non_private_attributes:
                print(f"  Modifier: {attribute[0]}, Type: {attribute[1]}, Name: {attribute[2]}, Line: {attribute[3]}")

# Walk through project directory and process each Java file, assumes there is a .git directory to avoid
for root, dirs, files in os.walk(project_directory):
    for dir in dirs:
        if dir == '.git':
            dirs.remove(dir)
    for file in files:
        if file.endswith('.java'):
            file_path = os.path.join(root, file)
            process_java_file(file_path)