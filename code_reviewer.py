import re
import os

def review_and_format_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    formatted_lines = []
    issues = []
    current_indent = 0

    for line_num, line in enumerate(lines, start=1):
        # Check for hidden characters, excluding newline and carriage return
        hidden_chars = re.findall(r'[^\S\r\n\x20-\x7E]', line)
        if hidden_chars:
            issues.append(f"Line {line_num}: Hidden characters detected: {hidden_chars}")

        # Strip whitespace and check indentation
        stripped_line = line.strip()
        if stripped_line:
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            
            # Check if indentation is a multiple of 4
            if leading_spaces % 4 != 0:
                issues.append(f"Line {line_num}: Incorrect indentation")
            
            # Adjust indentation based on opening/closing brackets
            if stripped_line[-1] in ':{':
                formatted_line = '    ' * current_indent + stripped_line + '\n'
                current_indent += 1
            elif stripped_line in [')', '}', ']']:
                current_indent = max(0, current_indent - 1)
                formatted_line = '    ' * current_indent + stripped_line + '\n'
            else:
                formatted_line = '    ' * current_indent + stripped_line + '\n'
        else:
            formatted_line = '\n'

        formatted_lines.append(formatted_line)

    # Write formatted code back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(formatted_lines)

    return issues

def main():
    while True:
        file_path = input("Enter the path to the Python file you want to review (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            print("Exiting the program.")
            break

        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' does not exist. Please try again.")
            continue

        issues = review_and_format_code(file_path)

        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(issue)
        else:
            print("\nNo issues found. Code formatting completed.")

        print(f"\nThe file '{file_path}' has been reviewed and formatted.")

if __name__ == "__main__":
    main()