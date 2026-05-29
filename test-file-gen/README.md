# test-file-gen

Contains `generator.py` — a helper script that generates sample `.txt` files
with random words, numbers, and mixed content for testing the sorter.

## Usage

```bash
cd test-file-gen
python generator.py
```

The generated files are written to the current directory and can be passed
directly to the sorter:

```bash
python ../main.py --file sample_words.txt --mode alpha
```
