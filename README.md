# Google Doc Grid Decoder

This repository includes a Python utility that reads a **published Google Doc** containing rows of:

- Unicode character
- `x` coordinate
- `y` coordinate

and prints the resulting 2D grid.

## Usage

```bash
python3 decode_google_doc_grid.py "<published-google-doc-url>"
```

Example:

```bash
python3 decode_google_doc_grid.py "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
```

Screenshot 2026-05-12 at 15.50.17.png
m-bayrak/GPT/Screenshot 2026-05-12 at 15.50.17.png

The script fills unspecified positions with spaces so the printed output forms the hidden uppercase message when viewed in a fixed-width font.
