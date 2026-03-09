---
name: write-to-logseq
description: Create, overwrite, append, or append child blocks inside Logseq markdown files.
---

# Skill: write-to-logseq

Use this when you need to write structured content into the Logseq graph.

Inputs:
- `file_path`: Destination Logseq markdown file path.
- `content`: Markdown or Logseq-style content to write.
- `mode`: One of `create`, `overwrite`, `append`, or `append_child_to_block`.
- `parent_block_query`: Required when `mode` is `append_child_to_block`.

Behavior:
- `create`: Fail if the file already exists.
- `overwrite`: Replace the whole file.
- `append`: Add content to the end of the file.
- `append_child_to_block`: Find the matching parent block text and insert child bullets under it.

Notes:
- The companion custom tool is also named `write-to-logseq`.
- Content is normalized into Logseq-friendly bullet structure before writing.
