---
name: read-and-search-logseq
description: Reads Logseq files or searches for specific tags/strings with block-level or file-level precision.
---
# Skill: read-and-search-logseq

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["read", "search"],
      "description": "Whether to read a specific file or search for a tag/string."
    },
    "file_path": {
      "type": "string",
      "description": "The path to the Logseq markdown file (required for 'read')."
    },
    "query": {
      "type": "string",
      "description": "The tag (e.g., '#review') or text to search for (required for 'search')."
    },
    "search_scope": {
      "type": "string",
      "enum": ["file", "block"],
      "default": "file",
      "description": "Whether to return the matching files or the specific blocks containing the match."
    }
  },
  "required": ["action"]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "success": { "type": "boolean" },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file_path": { "type": "string" },
          "content": { "type": "string" },
          "block_id": { "type": "string", "nullable": true }
        }
      },
      "description": "List of matching files or blocks."
    },
    "error": { "type": "string" }
  }
}
```

## Logic
1. **Action: read**
   - Read the file at `file_path`.
   - Return the full content in the `results` array.
2. **Action: search**
   - Use `grep` (or equivalent) to find occurrences of `query` in `pages/` and `journals/`.
   - If `search_scope` is `file`: Return unique file paths and their full content.
   - If `search_scope` is `block`: For each match, isolate the Logseq block (from bullet to next bullet at same/higher indentation) and return its content along with its `id::` if present.
3. Return the results.
