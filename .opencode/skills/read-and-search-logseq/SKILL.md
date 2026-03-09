---
name: read-and-search-logseq
description: Read Logseq pages directly or search Logseq pages and journals at file or block level.
---

# Skill: read-and-search-logseq

Use this when you need to inspect the Logseq graph.

Inputs:
- `action`: `read` or `search`.
- `file_path`: Required for `read`.
- `query`: Required for `search`.
- `search_scope`: `file` or `block`; defaults to `file`.

Behavior:
- `read`: Return the full contents of one Logseq file.
- `search`: Search `pages/` and `journals/` for the query.
- `file` scope returns matching files with full content.
- `block` scope returns matching Logseq blocks and detected `id::` values when present.

Notes:
- The companion custom tool is also named `read-and-search-logseq`.
