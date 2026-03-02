---
name: manage-workflow-tags
description: Replaces or adds workflow state tags in a Logseq markdown file to track the progress of cognitive tasks.
---
# Skill: manage-workflow-tags

## Schema
### Inputs
```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "type": "string",
      "description": "Path to the target Logseq markdown file."
    },
    "add_tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "A list of tags to add to the file (e.g., ['#anki-pending', '#synthesis-pending'])."
    },
    "remove_tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "A list of tags to remove from the file (e.g., ['#review-ready'])."
    }
  },
  "required": ["file_path"]
}
```

### Outputs
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Indicates if the tag modifications were successful."
    },
    "updated_content": {
      "type": "string",
      "description": "The resulting markdown content after modifications."
    }
  }
}
```

## Logic
1. Read the full content of the file at `file_path`.
2. **Remove Tags:** For each tag in `remove_tags`, find all occurrences of the tag in the text and replace them with an empty string, being mindful of spacing.
3. **Add Tags:** Check if the file already contains the tags in `add_tags`. If not, append the new tags. To align with Logseq conventions, it is recommended to append them to the end of the file or to a designated 'tags::' page property block if it exists.
4. Write the modified content back to `file_path`.
5. Return the updated state.
