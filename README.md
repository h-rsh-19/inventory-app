# Inventory App

Python Tkinter inventory management app with SQLite storage and PDF bill generation.

## What It Does

- Login/dashboard based desktop workflow.
- Add and manage products.
- Track purchases and sales.
- Generate bills and reports.
- Store inventory data in SQLite.

## Tech Stack

- Python
- Tkinter
- SQLite
- Report/PDF generation utilities

## Structure

```text
main.py
gui/
modules/
utils/
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The app initializes `db/inventory.db` on first run.

## What I Learned

- Building a multi-window desktop app with Tkinter.
- Separating GUI, data models, and utility code.
- Using SQLite for local persistence.
- Generating practical business documents from app data.
