import os
import re
import sys


def clean_path(path):
    return path.strip().strip('"').strip("'")


def natural_key(s):
    """Key for natural / human sort: 'file2' < 'file10'."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]


def list_supported_files(folder):
    supported_exts = ('.txt', '.csv', '.log', '.md')
    return sorted(
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith(supported_exts)
    )


def ask(prompt, valid):
    """Prompt until the user gives a valid answer or types 'b' to go back."""
    valid_lower = [v.lower() for v in valid]
    while True:
        ans = input(prompt).strip().lower()
        if ans == 'b':
            return None
        if ans in valid_lower:
            return ans
        print(f"  Please enter one of: {', '.join(valid)} (or 'b' to go back)")


def choose_file(files):
    print()
    for i, f in enumerate(files, 1):
        print(f"  {i:>2}. {f}")
    print()
    while True:
        raw = input("Select file number (or 'b' to quit): ").strip().lower()
        if raw == 'b':
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(files):
            return files[int(raw) - 1]
        print("  Invalid choice.")


def choose_folder():
    """Ask whether to sort from the script folder or a custom path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\n  Default folder: {script_dir}")
    use_custom = ask("  Use a different folder? y/n: ", ['y', 'n'])
    if use_custom is None:
        return None
    if use_custom == 'y':
        raw = input("  Enter folder path: ")
        folder = clean_path(raw)
        if not os.path.isdir(folder):
            print(f"  Folder not found: {folder}")
            return None
        return folder
    return script_dir


def sort_lines(lines, mode, reverse, skip_empty, dedupe):
    if skip_empty:
        lines = [l for l in lines if l.strip()]
    if dedupe:
        seen = set()
        unique = []
        for l in lines:
            key = l.strip().lower()
            if key not in seen:
                seen.add(key)
                unique.append(l)
        lines = unique

    if mode == 'alpha':
        lines = sorted(lines, key=lambda x: x.lower(), reverse=reverse)
        # Capitalise first character
        lines = [l[0].upper() + l[1:] if l.strip() else l for l in lines]

    elif mode == 'natural':
        lines = sorted(lines, key=lambda x: natural_key(x), reverse=reverse)

    elif mode == 'numeric':
        def num_key(line):
            m = re.search(r'-?\d+(\.\d+)?', line)
            return float(m.group()) if m else float('inf')
        lines = sorted(lines, key=num_key, reverse=reverse)

    elif mode == 'length':
        lines = sorted(lines, key=lambda x: len(x.rstrip()), reverse=reverse)

    return lines


def sort_file(input_path, output_path, mode, reverse, skip_empty, dedupe):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = [l.rstrip('\n') for l in f]

        original_count = len(lines)
        sorted_lines = sort_lines(lines, mode, reverse, skip_empty, dedupe)

        with open(output_path, 'w', encoding='utf-8') as f:
            for l in sorted_lines:
                f.write(l + '\n')

        removed = original_count - len(sorted_lines)
        print(f"\n  Saved → {output_path}")
        print(f"  Lines: {original_count} in, {len(sorted_lines)} out", end="")
        if removed:
            print(f" ({removed} removed by dedup/empty filter)", end="")
        print()
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


MODES = {
    'a': ('alpha',   'Alphabetical (A–Z)'),
    'n': ('natural', 'Natural / human sort  (file2 before file10)'),
    'u': ('numeric', 'Numeric  (by first number found in each line)'),
    'l': ('length',  'By line length'),
}


def main():
    print("\n  Drew's Alpha-Numerical Sorter")
    print("  " + "-" * 30)

    try:
        while True:
            # --- choose folder ---
            folder = choose_folder()
            if folder is None:
                break

            # --- list files ---
            files = list_supported_files(folder)
            if not files:
                print("  No supported files found (.txt .csv .log .md).")
                continue

            # --- choose file ---
            print(f"  Files in {folder}:")
            filename = choose_file(files)
            if filename is None:
                break
            input_path = os.path.join(folder, filename)

            # --- sort mode ---
            print("\n  Sort mode:")
            for k, (_, label) in MODES.items():
                print(f"    ({k}) {label}")
            mode_key = ask("  Choose: ", list(MODES.keys()))
            if mode_key is None:
                continue
            mode, _ = MODES[mode_key]

            # --- sort order ---
            order = ask("  Order — (a)scending or (d)escending: ", ['a', 'd'])
            if order is None:
                continue
            reverse = (order == 'd')

            # --- options ---
            skip_empty = ask("  Remove empty lines? y/n: ", ['y', 'n'])
            if skip_empty is None:
                continue
            skip_empty = (skip_empty == 'y')

            dedupe = ask("  Remove duplicate lines? y/n: ", ['y', 'n'])
            if dedupe is None:
                continue
            dedupe = (dedupe == 'y')

            # --- output path ---
            base, ext = os.path.splitext(input_path)
            default_out = base + '_sorted' + ext
            print(f"  Output file: {default_out}")
            custom = ask("  Use a custom output path? y/n: ", ['y', 'n'])
            if custom is None:
                continue
            if custom == 'y':
                raw = input("  Output path: ")
                output_path = clean_path(raw)
            else:
                output_path = default_out

            # --- run ---
            sort_file(input_path, output_path, mode, reverse, skip_empty, dedupe)

            # --- again? ---
            again = ask("\n  Sort another file? y/n: ", ['y', 'n'])
            if again != 'y':
                break

    except KeyboardInterrupt:
        print("\n  Interrupted.")

    print("  Bye!")


if __name__ == '__main__':
    main()
