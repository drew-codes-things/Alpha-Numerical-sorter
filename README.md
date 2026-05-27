# Alpha-Numerical Sorter

A Python command-line tool that sorts the lines of any text-based file — alphabetically, numerically, by natural order, or by line length.

No dependencies. Pure Python standard library.

---

## Usage

```bash
python main.py
```

The script walks you through everything interactively:

1. **Choose a folder** — uses the script's folder by default, or enter a custom path
2. **Choose a file** — lists all `.txt`, `.csv`, `.log`, and `.md` files in the folder
3. **Choose a sort mode** (see below)
4. **Choose order** — ascending or descending
5. **Remove empty lines?** — yes/no
6. **Remove duplicate lines?** — yes/no
7. **Output path** — defaults to `filename_sorted.ext` next to the original

Type `b` at any prompt to go back one step.

---

## Sort modes

| Key | Mode | Description |
|-----|------|-------------|
| `a` | Alphabetical | Case-insensitive A–Z sort, first letter capitalised |
| `n` | Natural | Human sort — `file2` comes before `file10` |
| `u` | Numeric | Sorts by the first number found in each line |
| `l` | Length | Sorts lines shortest to longest (or reverse) |

---

## Example

Input (`names.txt`):
```
zara
alice
bob
alice
```

Run with: alphabetical, ascending, remove duplicates → `names_sorted.txt`:
```
Alice
Bob
Zara
```

---

## Supported file types

`.txt` `.csv` `.log` `.md`

---

## Test file generator

The `test-file-gen/` folder contains a helper script to generate sample files for testing the sorter.

---

## License

MIT
