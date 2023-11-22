import os

def count_lines_of_code(directory, script_file):
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.join(root, file) != script_file:
                if file.endswith('.py'):  
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
    return total_lines

script_file = os.path.abspath(__file__)

directory = os.path.dirname(script_file)

print(f"Total lines of code: {count_lines_of_code(directory, script_file)}")