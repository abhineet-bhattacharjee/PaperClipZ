# README.md
# PaperClipZ

A smart clipboard manager with intelligent ranking and pinning features.

## Features

- **Smart Sorting**: Items ranked by recency and frequency
- **Pinning**: Pin important items to keep them accessible
- **Hotkeys**: Ctrl+1-0 for quick paste, Ctrl+P to pin/unpin
- **Deduplication**: Tracks copy/paste frequency instead of creating duplicates
- **Persistent History**: All clipboard history saved across sessions

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python app.py
```

## Configuration

Edit `data/config.json`:
```json
{
    "interval": 0.1,
    "sort_mode": "smart",
    "newline": true
}
```

- `interval`: Clipboard polling interval in seconds
- `sort_mode`: "smart" (recency + frequency) or "last_copied" (chronological)
- `newline`: Add newline when pasting

## Hotkeys

- `Ctrl+1` - Paste most recent/relevant item
- `Ctrl+2` - Paste 2nd item
- ...
- `Ctrl+0` - Paste 10th item
- `Ctrl+P` - Pin/unpin current clipboard item

## License

MIT