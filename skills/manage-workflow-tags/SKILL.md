# Manage Workflow Tags

Surgically add, remove, or replace a specific workflow tag in a Logseq file or block.

## Inputs

- `file_path`: (string, required) The absolute path to the Logseq Markdown file.
- `action`: (string, required) The action to perform: `add`, `remove`, or `replace`.
- `tag`: (string) The tag to add or remove (e.g., `#todo`). Required for `add` and `remove`.
- `old_tag`: (string) The tag to be replaced. Required for `replace`.
- `new_tag`: (string) The tag to replace with. Required for `replace`.
- `block_id`: (string) Optional UUID of the block to target.
- `block_content`: (string) Optional substring to identify the block to target (searches first line of blocks).

## Usage

### Add a tag to a specific block
```json
{
  "file_path": "/path/to/page.md",
  "action": "add",
  "tag": "#active",
  "block_id": "6400..."
}
```

### Replace a tag in the whole file
```json
{
  "file_path": "/path/to/page.md",
  "action": "replace",
  "old_tag": "#anki-pending",
  "new_tag": "#anki-processed"
}
```
