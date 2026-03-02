---
name: read-and-search-logseq
description: Reads a specific .md file or searches the entire Logseq graph directory for files containing specific state tags.
---
# Skill: read-and-search-logseq

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "Optional exact path to a specific Logseq markdown file to read."
    },
    "tag": {
      "type": "string",
      "description": "Optional state tag to search for across the Logseq directory (e.g., '#review-ready'). Include the hash symbol."
    },
    "directory": {
      "type": "string",
      "description": "The root directory of the Logseq graph."
    }
  },
  "anyOf": [
    {"required": ["file_path"]},
    {"required": ["tag", "directory"]}
  ]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" }
        }
      },
      "description": "List of matching files and their complete text content."
    }
  }
}
```

## Logic
1. **Direct Read Mode (if `file_path` is provided):** Read the file directly from disk and return its content in a single-item array.
2. **Search Mode (if `tag` is provided):**
   - Traverse the provided `directory` recursively (typically focusing on `pages/` and `journals/` folders).
   - Use a fast grep-like mechanism or AST-based Markdown parser to identify files that contain the specified `tag`.
   - Read the contents of all matching files.
3. Return the populated array of `results`.
