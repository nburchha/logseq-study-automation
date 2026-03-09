---
name: call-anki-connect
description: Send generated flashcards to a local Anki instance through the AnkiConnect API.
---

# Skill: call-anki-connect

Use this when you want to create Anki notes programmatically.

Inputs:
- `deck_name`: Destination deck name.
- `model_name`: Anki note type, such as `Basic`.
- `cards`: Array of card objects with `front`, `back`, and optional `tags`.

Behavior:
- Sends an `addNotes` request to `http://localhost:8765`.
- Returns created note IDs on success.
- Returns structured errors when AnkiConnect rejects the request.

Notes:
- The companion custom tool is also named `call-anki-connect`.
