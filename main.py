import os

print("Welcome to Drew's Alpha-Numerical sorter :)")
def list_supported_text_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    supported_exts = ('.txt', '.csv', '.log', '.md', '.json')
    files = [f for f in os.listdir(script_dir) if f.lower().endswith(supported_exts)]
    return files, script_dir

def choose_file(files):
    while True:
        print("Select a text-based file to sort:\n")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
        choice = input("\nEnter the number of the file (or 'b' to go back): ").strip().lower()
        if choice == 'b':
            return 'BACK'
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        print("Choose a valid number.\n")

def get_input_with_back(prompt, valid_options):
    while True:
        choice = input(prompt).strip().lower()
        if choice == 'b':
            return 'BACK'
        if choice in valid_options:
            return choice
        print(f"Choose {', '.join(valid_options)}.\n")

def sort_lines(lines, mode, reverse=False, skip_empty=False):
    if skip_empty:
        lines = [line for line in lines if line.strip()]
    if mode == 'alphabetical':
        sorted_lines = sorted(lines, key=lambda x: x.lower() if x else '')
        return [line[0].upper() + line[1:] if line else '' for line in sorted_lines]
    elif mode == 'numerical':
        def first_digit_or_inf(line):
            if line and line[0].isdigit():
                return int(line[0])
            return float('inf')
        return sorted(lines, key=first_digit_or_inf, reverse=reverse)

def sort_txt_file(input_path, mode, reverse, skip_empty):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]
        sorted_lines = sort_lines(lines, mode, reverse, skip_empty)
        output_file = os.path.splitext(input_path)[0] + '_sorted.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in sorted_lines:
                f.write(line + '\n')
        print(f"\nFile sorted and saved to: {output_file}\n")
        return True
    except Exception as e:
        print(f"Error sorting file: {e}")
        return False

def main():
    try:
        while True:
            while True:
                text_files, folder_path = list_supported_text_files()
                if not text_files:
                    print("No supported text files found in this directory.\n")
                    return
                selected_file = choose_file(text_files)
                if selected_file == 'BACK':
                    print("You are at the first question, you can't go back further.\n")
                    continue
                break
            full_path = os.path.join(folder_path, selected_file)
            while True:
                sort_mode = get_input_with_back("Sort mode: (a)lphabetical or (n)umerical: ", ('a', 'n'))
                if sort_mode == 'BACK':
                    break
                sort_mode = 'alphabetical' if sort_mode == 'a' else 'numerical'
                while True:
                    sort_order = get_input_with_back("Sort order: (a)scending or (d)escending: ", ('a', 'd'))
                    if sort_order == 'BACK':
                        break
                    sort_reverse = sort_order == 'd'
                    while True:
                        skip_empty = get_input_with_back("Ignore empty lines? y/n: ", ('y', 'n'))
                        if skip_empty == 'BACK':
                            break
                        skip_empty = skip_empty == 'y'
                        if not sort_txt_file(full_path, sort_mode, sort_reverse, skip_empty):
                            return
                        while True:
                            again = get_input_with_back("Would you like to sort another file? y/n: ", ('y', 'n'))
                            if again == 'BACK':
                                break
                            if again != 'y':
                                print("Thank you for using my sort script :)")
                                return
                            break
                        if again == 'BACK':
                            continue
                        break
                    if skip_empty == 'BACK':
                        continue
                    break
                if sort_order == 'BACK':
                    continue
                break
            if sort_mode == 'BACK':
                continue
    except KeyboardInterrupt:
        print("\nProcess halted by you. Exiting...")

if __name__ == '__main__':
    main()
