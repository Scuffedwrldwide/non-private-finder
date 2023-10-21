import regex
import os

# Path to the project directory to search for Java files
# Assumes this script is in a separate folder to the project directory, but in the same parent directory
project_directory = '../'
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
        found_in_file = False

        java_code = file.read()
        relative_path = os.path.relpath(file_path, project_directory)
        # Matches class declaration outright, group 1 gets the name while group 2 gets everything between curly brackets
        outer_class_code = regex.findall(r'class .*\{([\S\s]*)\}', java_code) 
        class_name = regex.findall(r'class (\w+)', java_code)
        class_code_with_inner = []

        while len(outer_class_code): # While there are possibly still internal classes to process
            class_code_with_inner += outer_class_code # Add outer class outright
            class_to_parse = outer_class_code.pop() # Get outer class code to parse
            outer_class_code += regex.findall(r'class .*\{([\S\s]*)\}', class_to_parse) # Queue any inner classes to process
            class_name += regex.findall(r'class (\w+)', class_to_parse) # Add inner classes names

        for class_code in class_code_with_inner: 
            # For each string of code pertaining to a class remove all code between curly brackets, to avoid finding attributes in methods
            class_code_no_bracket = regex.sub(r'\{(?:[^{}]*|(?R))*\}', '', class_code)

            for non_private_attributes in regex.findall(r'^\s+((?!.*(abstract|private|return).*)(?(?=.*\)).*?=.*).*;)$', class_code_no_bracket, regex.M):
                if class_name != []: current_name = class_name.pop(0)
                found = True
                if not found_in_file: 
                    print(f"File: \033[1m{relative_path}\033[0m")
                    found_in_file = True
                for attribute in non_private_attributes:
                    if attribute != '':
                        print(f"        \033[33m{attribute}\033[0m in class \033[34m{current_name}\033[0m")
        if found_in_file: print('\n')

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
