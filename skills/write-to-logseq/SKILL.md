---
name: write-to-logseq
description: Creates a new .md file in the Logseq graph or appends content to an existing one.
---
# Skill: write-to-logseq

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "The destination path for the Logseq markdown file."
    },
    "content": {
      "type": "string",
      "description": "The markdown content to write or append."
    },
    "mode": {
      "type": "string",
      "enum": ["append", "overwrite", "create"],
      "description": "The mode of file operation."
    }
  },
  "required": ["file_path", "content", "mode"]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates whether the write operation succeeded."
    },
    "path": {
      "type": "string",
      "description": "The absolute path to the modified or created file."
    }
  }
}
```

## Logic
1. Verify the directory path exists. If not, create necessary parent directories.
2. Depending on the `mode`:
   - `create`: Assert file does not exist, then write `content` to `file_path`.
   - `overwrite`: Overwrite the existing file at `file_path` with `content`.
   - `append`: Open the file at `file_path` and append `content` to the end of the file, ensuring a newline separates existing and new content.
3. Return `success: true` upon successful disk operation.
