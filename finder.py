import regex
import os

# Path to the project directory to search for Java files
# Assumes this script is in a separate folder to the project directory, but in the same parent directory
project_directory = '/home/marasenna/projeto/045/xxl-core/src/xxl/cell/'
found = False
print('\n')

def process_java_file(file_path):
    """
    Processes a Java file to find its class name and print non-private attributes.

    Args:
        file_path (str): The path of the Java file to process.

    Returns:
        None
    """
    with open(file_path, 'r') as file:
        global found

        java_code = file.read()
        relative_path = os.path.relpath(file_path, project_directory)
        # Matches all class code, group one gets everything between curly brackets
        outer_class_code = regex.findall(r'class .*\{([\S\s]*)\}', java_code) 


        class_code_with_inner = []

        while len(outer_class_code): # While there are possibly still internal classes to process
            class_code_with_inner += outer_class_code # Add outer class outright
            outer_class_code += regex.findall(r'class .*\{([\S\s]*)\}', outer_class_code.pop()) # Add inner classes to process

        for class_code in class_code_with_inner: 
            # For each string of code pertaining to a class remove all code between curly brackets, to avoid finding attributes in methods
            class_code_no_bracket = regex.sub(r'\{(?:[^{}]*|(?R))*\}', '', class_code)
            
            for non_private_attributes in regex.findall(r'^((?!.*(abstract|private).*)(?=.*=).*;)$', class_code_no_bracket, regex.M):
                found = True
                print(f"File: \033[1m{relative_path}\033[0m")
                for attribute in non_private_attributes:
                    print(f"    \033[33m{attribute}\033[0m\n")

# Walk through project directory and process each Java file, assumes there is a .git directory to avoid
for root, dirs, files in os.walk(project_directory):

    for dir in dirs:
        if dir == '.git' or dir == 'po-uilib': # Ignore .git and po-uilib directories
            dirs.remove(dir)

    for file in files:
        if file.endswith('.java'):
            file_path = os.path.join(root, file)
            process_java_file(file_path)

if not found:
    print("\033[1m \033[32m No non-private attributes found!\033[0m")