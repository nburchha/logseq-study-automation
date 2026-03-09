---
name: manage-workflow-tags
description: Add, remove, or replace workflow tags in an entire Logseq file or in a specific block.
---

# Skill: manage-workflow-tags

Use this when you need to move notes through a Logseq workflow.

Inputs:
- `file_path`: Target Logseq file.
- `action`: `add`, `remove`, or `replace`.
- `tag`: Required for `add` and `remove`.
- `old_tag`: Required for `replace`.
- `new_tag`: Required for `replace`.
- `block_id`: Optional UUID of the target block.
- `block_content`: Optional substring to find the target block.

Behavior:
- If a block target is provided, only that block is modified.
- Otherwise the whole file is updated.
- `add` avoids duplicate tags.

Notes:
- The companion custom tool is also named `manage-workflow-tags`.
